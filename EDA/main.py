import os
import hashlib
from datetime import datetime, time, date

import numpy as np
import pandas as pd
import requests
import streamlit as st
from geopy.distance import geodesic
from sklearn.preprocessing import LabelEncoder
import pickle

# =========================================================
# 🔑 API KEY (tries import, then st.secrets, then env var)
# =========================================================
def get_api_key():
    # 1) Try local module, if present
    api_key = None
    try:
        from Location_Finder_api_copy import api_key as _k
        api_key = _k
    except Exception:
        pass
    # 2) Try Streamlit secrets
    if api_key is None:
        try:
            api_key = st.secrets["OPENCAGE_API_KEY"]
        except Exception:
            pass
    # 3) Try environment variable
    if api_key is None:
        api_key = os.getenv("OPENCAGE_API_KEY")
    return api_key

# =========================
# 🎨 BACKGROUND & STYLES
# =========================
def set_cool_modern_background():
    st.markdown(
        f"""
        <style>
        /* App Background */
        .stApp {{
            background: linear-gradient(135deg, #E0F7FA 0%, #FFFFFF 100%);
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
        }}

        /* Main header box */
        .main-header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}

        /* Header text colors */
        h1, h2, h3 {{
            color: #00796B !important; /* Teal-ish for freshness */
            font-weight: bold;
        }}

        /* Buttons style */
        div.stButton > button:first-child {{
            background: linear-gradient(90deg, #26A69A 0%, #80CBC4 100%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            transition: all 0.3s ease;
        }}
        div.stButton > button:first-child:hover {{
            background: linear-gradient(90deg, #00796B 0%, #26A69A 100%);
            transform: scale(1.05);
            box-shadow: 0 6px 18px rgba(0,0,0,0.2);
        }}

        /* Inputs & text area */
        .stTextInput>div>input, .stTextArea>div>textarea {{
            border-radius: 10px;
            border: 1px solid #26A69A;
            padding: 8px;
        }}

        /* Select boxes */
        div.stSelectbox>div>div>div {{
            border-radius: 10px;
            border: 1px solid #26A69A;
        }}

        /* Sliders */
        .stSlider>div>div>div>div {{
            color: #00796B;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply modern cool theme
set_cool_modern_background()

# ===================
# 📦 LOAD ARTIFACTS
# ===================
@st.cache_resource
def load_model_and_scaler():
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model, scaler
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please place `model.pkl` and `scaler.pkl` next to this app.")
        return None, None

@st.cache_data
def load_delivery_person_data(uploaded_file):
    # If a user CSV is provided, prefer IDs from it
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Delivery_person_ID' in df.columns:
                ids = sorted(df['Delivery_person_ID'].dropna().unique().tolist())
                if ids:
                    return ids
        except Exception:
            pass
    # Fallback synthetic IDs
    delivery_persons = []
    cities = ['BANG', 'DEL', 'MUM', 'CHE', 'HYD', 'KOL', 'PUN', 'AHM']
    regions = ['RES', 'COM', 'IND']
    for city in cities:
        for region in regions:
            for i in range(1, 21):
                delivery_persons.append(f"{city}{region}{i:02d}DEL{i:02d}")
    return sorted(delivery_persons)

@st.cache_data
def get_delivery_person_details(person_id, uploaded_file):
    # Try user data first
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Delivery_person_ID' in df.columns:
                row = df[df['Delivery_person_ID'] == person_id]
                if not row.empty:
                    age = int(row['Delivery_person_Age'].iloc[0]) if 'Delivery_person_Age' in row else 30
                    ratings = float(row['Delivery_person_Ratings'].iloc[0]) if 'Delivery_person_Ratings' in row else 4.5
                    return {'age': age, 'ratings': round(ratings, 1)}
        except Exception:
            pass
    # Fallback deterministic pseudo-values from hash
    hv = int(hashlib.md5(person_id.encode()).hexdigest()[:8], 16)
    age = 22 + (hv % 24)
    rating = 3.5 + (hv % 150) / 100
    return {'age': age, 'ratings': round(rating, 1)}

# =========================
# 🧰 FEATURE ENGINEERING
# =========================
def extract_city_code(df: pd.DataFrame):
    # Safer extraction: take consecutive uppercase letters from start
    # e.g., "BANGRES01DEL01" -> "BANG"
    df['City_code'] = df['Delivery_person_ID'].str.extract(r'^([A-Z]+)', expand=False).fillna('NA')

def extract_date_features(data: pd.DataFrame):
    data["day"] = data.Order_Date.dt.day
    data["month"] = data.Order_Date.dt.month
    data["quarter"] = data.Order_Date.dt.quarter
    data["year"] = data.Order_Date.dt.year
    data['day_of_week'] = data.Order_Date.dt.day_of_week.astype(int)
    data["is_month_start"] = data.Order_Date.dt.is_month_start.astype(int)
    data["is_month_end"] = data.Order_Date.dt.is_month_end.astype(int)
    data["is_quarter_start"] = data.Order_Date.dt.is_quarter_start.astype(int)
    data["is_quarter_end"] = data.Order_Date.dt.is_quarter_end.astype(int)
    data["is_year_start"] = data.Order_Date.dt.is_year_start.astype(int)
    data["is_year_end"] = data.Order_Date.dt.is_year_end.astype(int)
    data['is_weekend'] = np.where(data['day_of_week'].isin([5, 6]), 1, 0)

def calculate_time_diff(df: pd.DataFrame):
    # Ensure string -> timedelta
    df['Time_Orderd'] = pd.to_timedelta(df['Time_Orderd'].astype(str))
    df['Time_Order_picked'] = pd.to_timedelta(df['Time_Order_picked'].astype(str))
    # If picked before ordered, assume after midnight
    df['Time_Order_picked_formatted'] = df['Order_Date'] + np.where(
        df['Time_Order_picked'] < df['Time_Orderd'],
        pd.DateOffset(days=1),
        pd.DateOffset(days=0)
    ) + df['Time_Order_picked']
    df['Time_Ordered_formatted'] = df['Order_Date'] + df['Time_Orderd']
    df['Time_Order_picked_formatted'] = pd.to_datetime(df['Time_Order_picked_formatted'])
    # Minutes
    df['order_prepare_time'] = (
        df['Time_Order_picked_formatted'] - df['Time_Ordered_formatted']
    ).dt.total_seconds() / 60.0
    df['order_prepare_time'] = df['order_prepare_time'].fillna(df['order_prepare_time'].median())
    # Drop temp cols no longer needed (Order_Date included only after we derived features)
    df.drop(
        ['Time_Orderd', 'Time_Order_picked', 'Time_Ordered_formatted', 'Time_Order_picked_formatted', 'Order_Date'],
        axis=1,
        inplace=True
    )

def ensure_numeric_distance(df: pd.DataFrame):
    # Compute distance as float km (no strings)
    df['distance'] = df.apply(
        lambda r: geodesic(
            (float(r['Restaurant_latitude']), float(r['Restaurant_longitude'])),
            (float(r['Delivery_location_latitude']), float(r['Delivery_location_longitude']))
        ).km,
        axis=1
    )

def add_rating_category_numeric(df: pd.DataFrame):
    # Create 0/1/2 numeric category (no strings to break scaler)
    # Low: 0-2, Medium: >2-4, High: >4-5
    cut = pd.cut(
        df['Delivery_person_Ratings'].astype(float),
        bins=[-np.inf, 2.0, 4.0, np.inf],
        labels=[0, 1, 2]
    ).astype(int)
    df['Rating_category'] = cut

def safe_label_encode_all_objects(df: pd.DataFrame):
    # Convert 'category' dtype to string first so LabelEncoder sees them
    for col in df.columns:
        if str(df[col].dtype) == 'category':
            df[col] = df[col].astype(str)
    obj_cols = df.select_dtypes(include=['object']).columns.tolist()
    le = LabelEncoder()
    for col in obj_cols:
        try:
            df[col] = le.fit_transform(df[col].astype(str))
        except Exception:
            # If something goes wrong, fallback to hash-based encoding (stable)
            df[col] = df[col].astype(str).apply(lambda s: abs(hash(s)) % 10_000)

# =========================
# 📍 GEOCODING
# =========================
@st.cache_data(show_spinner=False)
def get_lat_long_opencage(address: str, api_key: str):
    if not api_key:
        return None, None
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('results'):
                lat = data['results'][0]['geometry']['lat']
                lng = data['results'][0]['geometry']['lng']
                return lat, lng
    except Exception:
        pass
    return None, None

# =========================
# 🧠 APP LAYOUT
# =========================
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title('🚚 AI-Powered Delivery Time Prediction')
st.markdown("Get accurate delivery time estimates using machine learning")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar: data upload
st.sidebar.header("📂 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your delivery data CSV (optional)", type=['csv'])

# Load model + scaler
model, scaler = load_model_and_scaler()

# Prepare IDs
delivery_person_ids = load_delivery_person_data(uploaded_file)

# Order inputs
col1, col2 = st.columns(2)
with col1:
    order_date = st.date_input('📅 Order Date', value=date.today())
    time_ordered = st.time_input('🕐 Time Ordered', value=time(12, 0))
    time_order_picked = st.time_input('⏰ Time Order Picked', value=time(12, 30))
    order_type = st.selectbox('🍽️ Type of Order', ['Meal', 'Snack', 'Drinks', 'Buffet'])
    multiple_deliveries = st.number_input('📦 Multiple Deliveries', min_value=0, max_value=5, value=0)
    festival = st.selectbox('🎉 Festival', ['No', 'Yes'])

with col2:
    delivery_person_id = st.selectbox('🆔 Delivery Person ID', delivery_person_ids)
    det = get_delivery_person_details(delivery_person_id, uploaded_file)
    age = st.number_input('👶 Delivery Person Age', min_value=18, max_value=65, value=int(det['age']))
    ratings = st.number_input('⭐ Delivery Person Ratings', min_value=1.0, max_value=5.0, value=float(det['ratings']), step=0.1)

# Env & vehicle
col3, col4 = st.columns(2)
with col3:
    weather = st.selectbox('🌦️ Weather Conditions', ['Sunny', 'Cloudy', 'Rainy', 'Foggy'])
    traffic = st.selectbox('🚦 Road Traffic Density', ['Low', 'Medium', 'High', 'Jam'])
    city = st.selectbox('🏙️ City Type', ['Metropolitan', 'Urban', 'Semi-Urban'])
with col4:
    vehicle_type = st.selectbox('🚲 Type of Vehicle', ['Bike', 'Scooter', 'Car', 'Truck'])
    vehicle_condition = st.slider('🔧 Vehicle Condition', min_value=0, max_value=10, value=7)

# Addresses
st.subheader("📍 Delivery Locations")
restaurant_options = ["Domino's Pizza - MG Road", "Burger King - Connaught Place", "Subway - Andheri", "KFC - Park Street"]
delivery_options = ["DLF Cyber City, Gurugram", "Powai, Mumbai", "Banjara Hills, Hyderabad", "Salt Lake, Kolkata"]

col5, col6 = st.columns(2)
with col5:
    rest_choice = st.selectbox('🏪 Choose Restaurant (or select "Other")', restaurant_options + ["Other"])
    restaurant_address = st.text_area('🏪 Restaurant Address', placeholder="Enter complete restaurant address...") if rest_choice == "Other" else rest_choice
with col6:
    del_choice = st.selectbox('🏠 Choose Delivery Location (or select "Other")', delivery_options + ["Other"])
    delivery_address = st.text_area('🏠 Delivery Address', placeholder="Enter complete delivery address...") if del_choice == "Other" else del_choice

# Optional debug
show_debug = st.checkbox("🔎 Show debug info", value=False)

# =========================
# 🔮 PREDICTION
# =========================
if st.button('🔮 Predict Delivery Time with AI', use_container_width=True):
    if model is None or scaler is None:
        st.error("❌ Model not loaded.")
    elif not restaurant_address or not delivery_address:
        st.error("❌ Please enter both addresses.")
    else:
        key = get_api_key()
        if not key:
            st.error("❌ OpenCage API key not found. Add it in `Location_Finder_api_copy.py` as `api_key`, "
                     "or set `st.secrets['OPENCAGE_API_KEY']`, or env var `OPENCAGE_API_KEY`.")
        else:
            rest_lat, rest_long = get_lat_long_opencage(restaurant_address, key)
            del_lat, del_long = get_lat_long_opencage(delivery_address, key)

            if rest_lat is None or del_lat is None:
                st.error("❌ Could not fetch coordinates for one or both addresses.")
            else:
                # Build raw row
                input_data = pd.DataFrame({
                    'Delivery_person_ID': [delivery_person_id],
                    'Delivery_person_Age': [age],
                    'Delivery_person_Ratings': [ratings],
                    'Restaurant_latitude': [rest_lat],
                    'Restaurant_longitude': [rest_long],
                    'Delivery_location_latitude': [del_lat],
                    'Delivery_location_longitude': [del_long],
                    'Order_Date': [pd.to_datetime(order_date)],
                    'Time_Orderd': [time_ordered],
                    'Time_Order_picked': [time_order_picked],
                    'Weather_conditions': [weather],
                    'Road_traffic_density': [traffic],
                    'Vehicle_condition': [vehicle_condition],
                    'Type_of_order': [order_type],
                    'Type_of_vehicle': [vehicle_type],
                    'multiple_deliveries': [multiple_deliveries],
                    'Festival': [festival],
                    'City': [city]
                })

                # Extra features expected by many training setups
                extract_city_code(input_data)
                add_rating_category_numeric(input_data)
                ensure_numeric_distance(input_data)

                # Harmonize field names the trainer might have expected
                input_data['multi_deliveries'] = input_data['multiple_deliveries']  # alias if used

                # Date/time derivations and cleanup
                extract_date_features(input_data)
                calculate_time_diff(input_data)

                # Drop ID if not in training
                # (We’ll re-add as zero if scaler expects it — alignment step handles that)
                if 'Delivery_person_ID' in input_data.columns:
                    pass  # keep for now, encode if necessary

                # Encode categoricals (ensure category dtype also gets encoded)
                safe_label_encode_all_objects(input_data)

                # Now drop Delivery_person_ID if still present (encoded now numeric; keep only if scaler expects it)
                # Alignment step below will handle presence/absence precisely.

                # ===== Alignment to training features =====
                expected = list(getattr(scaler, "feature_names_in_", []))
                if not expected:
                    st.error("❌ Your scaler is missing `feature_names_in_`. Please fit it with named columns.")
                else:
                    # Add any missing expected columns as 0
                    for col in expected:
                        if col not in input_data.columns:
                            input_data[col] = 0

                    # Keep only expected columns, in the exact order
                    input_data = input_data[expected]

                    if show_debug:
                        st.write("Expected features count:", len(expected))
                        st.write("Input columns count:", input_data.shape[1])
                        st.write("First few columns:", input_data.columns[:10].tolist())
                        st.write(input_data.head())

                    # Final numeric dtype enforcement
                    for c in input_data.columns:
                        if not np.issubdtype(input_data[c].dtype, np.number):
                            input_data[c] = pd.to_numeric(input_data[c], errors='coerce').fillna(0)

                    # Scale & predict
                    try:
                        Xs = scaler.transform(input_data)
                        yhat = model.predict(Xs)
                        predicted_time = round(float(yhat[0]), 1)
                        est_delivery = (
                            datetime.combine(order_date, time_order_picked) +
                            pd.Timedelta(minutes=predicted_time)
                        )
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #FF8A65 0%, #FF7043 100%);
                                        padding: 30px; border-radius: 15px; text-align: center;
                                        color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                                <h2>🤖 AI Prediction Result</h2>
                                <h1 style="font-size: 4em;">{predicted_time} minutes</h1>
                                <p>⏰ Expected delivery by: <strong>{est_delivery.strftime('%I:%M %p')}</strong></p>
                            </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {e}")
