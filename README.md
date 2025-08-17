🍔 Food Delivery Time Predictions Analysis
  
Welcome to the Food Delivery Time Predictions Analysis project! 🚀 This project develops a machine learning model to predict food delivery times with high accuracy, addressing the challenge of inaccurate delivery estimates in the food delivery industry. By leveraging historical data and advanced regression techniques, the project aims to enhance customer satisfaction 😊, optimize resource planning 📅, and streamline operations ⚙️.

🧾 Project Overview
In the fast-paced food delivery industry, timely and accurate deliveries are critical for maintaining customer satisfaction and operational efficiency. Delivery times vary due to dynamic factors such as 🚦 traffic conditions, ☔ weather, 📍 delivery distance, 🧑‍🍳 restaurant preparation times, and 🚴‍♂️ delivery personnel characteristics. Current platforms often rely on rough heuristics, leading to inaccurate predictions, poor customer experiences, and logistical inefficiencies.
This project builds a machine learning model to predict delivery times using a dataset of 45,593 records from a SQLite database (food_delivery.db). The model incorporates features like:

Delivery Personnel: Age, ratings, and vehicle type (🚲 bike, 🛵 scooter, 🚗 car).
Geospatial Data: Restaurant and delivery locations, calculated distances.
Time-Based Factors: Order time, day of the week, holidays.
Environmental Factors: Weather conditions and traffic density.
Restaurant Metrics: Order type and preparation time.

🎯 Objectives

📅 Provide accurate delivery time estimates tailored to customer locations.
📈 Improve resource allocation and delivery scheduling.
😊 Enhance customer satisfaction and trust.
⚙️ Streamline operations for cost efficiency and scalability.

🔍 Key Features

Data Cleaning: Handles missing values, duplicates, and data type inconsistencies.
Feature Engineering: Extracts temporal features (e.g., day, month, weekend) and calculates geodesic distances.
Exploratory Data Analysis (EDA): Visualizes trends using histograms, box plots, violin plots, and heatmaps.
Machine Learning: Uses XGBoost with an R² score of 0.82 for robust predictions.
Scalability: Saves trained model (model.pkl) and scaler (scaler.pkl) for future use.


📂 Project Structure
food-delivery-prediction/
├── data/
│   └── food_delivery.db        # SQLite database with raw data
├── media/                     # Visualization images (e.g., rId38.png, rId50.png)
├── cleaned_dataset.csv        # Cleaned dataset
├── model.pkl                  # Trained XGBoost model
├── scaler.pkl                 # StandardScaler for preprocessing
├── Food_Delivery_Analysis.qmd # Quarto document with analysis
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies


🛠️ Setup Instructions
Prerequisites

🐍 Python 3.8+
🗄️ SQLite
📦 Python packages listed in requirements.txt
📝 Quarto (optional, for rendering the analysis document)

Installation

Clone the Repository:
git clone https://github.com/your-username/food-delivery-prediction.git
cd food-delivery-prediction


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Example requirements.txt:
pandas
numpy
matplotlib
seaborn
geopy
scikit-learn
xgboost


Prepare the Dataset:

Place the food_delivery.db SQLite database in the data/ folder.
Update the database path in the script if necessary (e.g., replace D:\\Grow Data Skill\\food_delivery.db with your path).


Install Quarto (Optional):

To render the Food_Delivery_Analysis.qmd document, install Quarto:wget https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb

Or follow Quarto installation instructions for your operating system.




🚀 Usage
Running the Analysis

Render the Quarto Document:

Use the Food_Delivery_Analysis.qmd file to explore the full analysis, including data cleaning, feature engineering, EDA, and model building.
Render to HTML:quarto render Food_Delivery_Analysis.qmd


This generates an HTML file with interactive visualizations and code outputs.


Run the Python Code:

Extract the Python code from Food_Delivery_Analysis.qmd or use it directly in a Python environment:python analysis.py




Make Predictions with the Trained Model:

Use the saved model.pkl and scaler.pkl for predictions:import pickle
import pandas as pd

# Load model and scaler
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Example: Predict delivery time
new_data = pd.DataFrame({
    'Delivery_person_Age': [30], 'Delivery_person_Ratings': [4.8], 
    'Restaurant_latitude': [26.902328], 'Restaurant_longitude': [75.794257],
    'Delivery_location_latitude': [26.912328], 'Delivery_location_longitude': [75.804257],
    'Weather_conditions': [4], 'Road_traffic_density': [0], 'Vehicle_condition': [1],
    'Type_of_order': [3], 'Type_of_vehicle': [1], 'multiple_deliveries': [0],
    'Festival': [0], 'City': [0], 'City_code': [5], 'multi_deliveries': [0.0],
    'day': [24], 'month': [3], 'quarter': [1], 'year': [2022], 'day_of_week': [3],
    'is_month_start': [0], 'is_month_end': [0], 'is_quarter_start': [0],
    'is_quarter_end': [0], 'is_year_start': [0], 'is_year_end': [0], 'is_weekend': [0],
    'order_prepare_time': [10.0], 'distance': [3], 'Rating_category': [2], 'Distance_km': [3.02]
})
new_data_scaled = scaler.transform(new_data)
prediction = model.predict(new_data_scaled)
print(f"Predicted Delivery Time: {prediction[0]:.2f} minutes")




Publish to Posit Cloud:

Share the rendered HTML on Posit Cloud:quarto publish posit-cloud Food_Delivery_Analysis.qmd


Authenticate with your Posit Cloud Token and Token Secret (from posit.cloud).
This generates a public URL (e.g., https://posit.cloud/content/<content-id>).




📊 Analysis Workflow
1. Data Loading & Cleaning 🧹

Dataset: Loaded from food_delivery.db with 45,593 records and 20 columns.
Cleaning Steps:
Removed duplicates (none found).
Dropped irrelevant columns (ID, Delivery_person_ID).
Handled missing values in Delivery_person_Age, Delivery_person_Ratings, Weather_conditions, Road_traffic_density, multiple_deliveries, Festival, and City using median/mode imputation.
Fixed formatting for Time_taken(min) (extracted numeric values) and Weather_conditions (removed prefix).
Converted data types: Delivery_person_Age to Int64, Order_Date to datetime, Delivery_person_Ratings to float.
Extracted City_code from Delivery_person_ID.



2. Feature Engineering ⚙️

Temporal Features:
Extracted day, month, quarter, year, day_of_week, is_month_start, is_month_end, is_quarter_start, is_quarter_end, is_year_start, is_year_end, and is_weekend from Order_Date.
Calculated order_prepare_time (difference between Time_Orderd and Time_Order_picked in minutes).


Distance Calculation:
Computed geodesic distance between restaurant and delivery locations using geopy.geodesic.
Created Distance_km and binned into Distance_Range (e.g., 0–2 km, 2–5 km).


Categorical Features:
Encoded categorical columns (Weather_conditions, Road_traffic_density, Type_of_order, Type_of_vehicle, Festival, City, City_code) using LabelEncoder.
Created Age_Group (bins: <18, 18–28, 28–38, 38–48, 48+) and Rating_category (bins: ≤2, 2–3, 3–4, 4–5, >5).



3. Exploratory Data Analysis (EDA) 📈

Visualizations:
Histograms & Box Plots: Analyzed distributions and outliers for numerical features (e.g., Delivery_person_Age, Time_taken(min), Distance_km).
Demographics & Ratings:
Younger delivery personnel (18–28) deliver faster (23.0 min) than older groups (38–48, 29.6 min).
High ratings (4–5) show consistent delivery times, while low ratings (<2) have high variability.


Traffic Density:
Traffic jams increase delivery times (40 min) compared to low traffic (20 min).
Medium traffic shows the most consistent delivery times.


City:
Urban areas: Fastest deliveries (23.0 min), 22.2% of orders.
Metropolitan areas: Moderate (27.1 min), 77.4% of orders.
Semi-urban areas: Slowest (49.7 min), only 0.4% of orders.


Vehicle Condition:
Condition 0 vehicles have the highest median delivery times.
Festivals increase delays across all vehicle conditions.


Multiple Deliveries:
More deliveries (e.g., 3) increase delivery times, especially on weekends.


Distance vs. Time:
Distance has minimal impact on delivery time, with most deliveries under 50 min.
Median times increase slightly for distances >12 km (29.7 min).


Weather & Traffic:
Cloudy/foggy weather with traffic jams causes the longest delays (36.7–36.8 min).
Sunny weather with low/medium traffic is fastest (20–21 min).


City & Traffic:
Semi-urban areas have the highest delivery times across all traffic densities (~48–50 min).
Urban areas are fastest in low traffic (~19 min).





4. Data Preprocessing 🛠️

Train-Test Split: Split data into 80% training (36,474 rows) and 20% testing (9,119 rows).
Standardization: Applied StandardScaler to numerical features for consistent scaling.
Dropped Categorical Bins: Removed Age_Group and Distance_Range to avoid redundancy after encoding.

5. Model Building & Evaluation 🤖

Models Tested:
Linear Regression: R² = 0.43
Decision Tree Regressor (max_depth=7): R² = 0.73
Random Forest Regressor (n_estimators=300): R² = 0.81
XGBoost Regressor (n_estimators=20, max_depth=9): R² = 0.81


Best Model: XGBoost Regressor (n_estimators=20, max_depth=9).
Evaluation Metrics (on test set):
Mean Absolute Error (MAE): 3.17 min
Mean Squared Error (MSE): 15.98
Root Mean Squared Error (RMSE): 4.0 min
R-squared (R²): 0.82


Model Saving: Saved the trained model as model.pkl and scaler as scaler.pkl using pickle.


📈 Key Insights

Demographics & Ratings:
Younger delivery personnel (18–28) are the fastest (23.0 min), while older groups (38–48) are slowest (29.6 min).
High ratings (4–5) correlate with consistent delivery times; low ratings (<2) show high variability.


Traffic Density:
Traffic jams significantly increase delivery times (~40 min vs. ~20 min for low traffic).
Medium traffic is the most consistent.


City Impact:
Urban areas have the fastest deliveries (23.0 min), followed by metropolitan (27.1 min).
Semi-urban areas are slowest (49.7 min) due to low order frequency (0.4%).


Vehicle Condition:
Poor vehicle condition (0) leads to longer delivery times.
Festivals exacerbate delays across all conditions.


Multiple Deliveries:
More deliveries increase times, with weekends showing higher delays.


Distance:
Distance has minimal impact, with most deliveries under 50 min regardless of range.


Weather & Traffic:
Cloudy/foggy weather with traffic jams causes the longest delays (36.7–36.8 min).
Sunny/low traffic conditions are fastest (20–21 min).


City & Traffic:
Semi-urban areas consistently have the highest delivery times across all traffic levels.




🌟 Future Enhancements

Feature Selection: Use SHAP values to identify the most impactful features.
Advanced Feature Engineering: Integrate real-time traffic/weather APIs and customer feedback sentiment analysis.
Model Optimization: Explore neural networks or ensemble methods for improved accuracy.
Dynamic Routing: Implement reinforcement learning for real-time route optimization.
API Deployment: Deploy the model as an API for real-time predictions (see xAI API).
Interactive Dashboards: Create a web-based dashboard using Plotly Dash or Streamlit for interactive EDA.


📚 Dependencies

Python Libraries:
pandas: Data manipulation
numpy: Numerical operations
matplotlib, seaborn: Visualizations
geopy: Geodesic distance calculations
scikit-learn: Machine learning and preprocessing
xgboost: XGBoost model


Quarto: For rendering the analysis document
SQLite: For database access


📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙌 Contributing
Contributions are welcome! 🙏 To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

For major changes, please open an issue first to discuss your ideas.

📬 Contact
For questions or feedback, reach out via GitHub Issues or contact the author at [your-email@example.com].

🏆 Acknowledgments

Thanks to the open-source community for tools like pandas, scikit-learn, and xgboost.
Inspired by the need to improve food delivery efficiency and customer satisfaction.

🍕 Happy Predicting! 🚀
