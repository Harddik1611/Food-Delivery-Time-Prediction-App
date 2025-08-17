🍔 Food Delivery Time Predictions Analysis
  
Welcome to the Food Delivery Time Predictions Analysis project! 🚀 This project leverages machine learning to predict food delivery times with high accuracy, addressing the challenge of inaccurate delivery estimates in the food delivery industry. By analyzing historical data, this project aims to enhance customer satisfaction 😊, optimize resource planning 📅, and streamline operations ⚙️.

🧾 Project Overview
In the fast-paced food delivery industry, timely and accurate deliveries are crucial for customer satisfaction and operational efficiency. However, factors like 🚦 traffic, ☔ weather, 📍 delivery distance, 🧑‍🍳 restaurant preparation times, and 🚴‍♂️ delivery personnel performance often lead to unpredictable delivery times.
Current platforms rely on basic heuristics, resulting in inaccurate predictions, frustrated customers, and logistical inefficiencies. This project develops a machine learning model to predict delivery times using historical data, incorporating features like:

Delivery Personnel: Age, ratings, experience, and vehicle type (🚲 bike, 🛵 scooter, 🚗 car).
Geospatial Data: Order and delivery locations, distance, urban vs. rural settings.
Time-Based Factors: Order time, peak hours, day of the week, holidays.
Restaurant Metrics: Preparation time, order volume, cuisine type.
External Variables: Real-time traffic, weather, and road closures.

🎯 Goals

📅 Provide precise delivery time estimates tailored to customer locations.
📈 Optimize resource allocation and delivery scheduling.
😊 Boost customer satisfaction and trust.
⚙️ Enhance operational efficiency and scalability.
🌐 Enable real-time adaptability to dynamic conditions.

🔍 Key Features

Interactive Visualizations: 📊 Dynamic charts and maps to explore delivery patterns.
Real-Time Integration: 🌐 Incorporate live traffic and weather APIs.
Scalable Model: 🛠️ Handles large datasets and adapts to new regions.
Explainable AI: 🔍 Uses SHAP values to interpret predictions.
Customer-Centric: 😊 Personalized delivery estimates for better user experience.


📂 Project Structure
food-delivery-prediction/
├── data/
│   └── food_delivery.db        # SQLite database with raw data
├── media/                     # Visualizations (charts, plots)
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
📦 Required Python packages (listed in requirements.txt)

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


Download the Dataset:

Place the food_delivery.db SQLite database in the data/ folder or update the path in the script to point to your database location.


Install Quarto (Optional):

To render the Food_Delivery_Analysis.qmd document, install Quarto:wget https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb

Or follow Quarto installation instructions for your OS.




🚀 Usage
Running the Analysis

Open the Quarto Document:

Use the Food_Delivery_Analysis.qmd file to explore the full analysis, including data cleaning, feature engineering, exploratory data analysis (EDA), and model building.
Render the Quarto document to HTML:quarto render Food_Delivery_Analysis.qmd




Run the Python Code:

Execute the Python code embedded in the Quarto document or extract it to a .py file to run independently:python analysis.py




Load the Trained Model:

Use the saved model.pkl and scaler.pkl to make predictions:import pickle
import pandas as pd

# Load model and scaler
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Example: Predict delivery time for new data
new_data = pd.DataFrame(...)  # Your input data
new_data_scaled = scaler.transform(new_data)
predictions = model.predict(new_data_scaled)
print(predictions)




Publish to Posit Cloud:

To share the rendered HTML on Posit Cloud:quarto publish posit-cloud Food_Delivery_Analysis.qmd


Authenticate with your Posit Cloud Token and Token Secret (from posit.cloud).
This generates a public URL (e.g., https://posit.cloud/content/<content-id>).




📊 Key Analysis Steps
1. Data Loading & Cleaning 🧹

Data Source: Loaded from food_delivery.db (SQLite) with 45,593 records and 20 columns.
Cleaning:
Removed duplicates and irrelevant columns (ID, Delivery_person_ID).
Handled missing values (e.g., Delivery_person_Age, Weather_conditions) using median/mode imputation.
Standardized data types (e.g., Delivery_person_Age to Int64, Order_Date to datetime).
Extracted features like City_code and cleaned Time_taken(min).



2. Feature Engineering ⚙️

Date Features: Extracted day, month, quarter, day_of_week, is_weekend, etc., from Order_Date.
Time Difference: Calculated order_prepare_time (difference between order and pickup times).
Distance Calculation: Computed geodesic distance between restaurant and delivery locations using geopy.
Categorical Encoding: Applied LabelEncoder to categorical columns (e.g., Weather_conditions, City).

3. Exploratory Data Analysis (EDA) 📈

Visualizations:
Age & Ratings: Younger delivery personnel (18–28) are faster (23 min) than older groups (38–48, 29.6 min). Higher ratings (4–5) correlate with consistent delivery times.
Traffic Density: Traffic jams increase delivery times (~40 min in jams vs. ~20 min in low traffic).
City: Urban areas have the fastest deliveries (23 min), while semi-urban areas are slowest (49.7 min).
Vehicle Condition: Condition 0 vehicles show higher delivery times; festivals increase delays.
Multiple Deliveries: More deliveries increase time, especially on weekends.
Distance: Minimal impact on delivery time, with most deliveries under 50 min regardless of distance.
Weather & Traffic: Cloudy/foggy weather with jams causes the longest delays (~36.7–36.8 min).



4. Model Building 🤖

Models Tested: Linear Regression, Decision Tree, Random Forest, XGBoost.
Cross-Validation: Used GridSearchCV to tune hyperparameters.
Best Model: XGBoost (n_estimators=20, max_depth=9) with an R² score of 0.82.
Evaluation Metrics:
Mean Absolute Error (MAE): 3.17 min
Mean Squared Error (MSE): 15.98
Root Mean Squared Error (RMSE): 4.0 min
R-squared (R²): 0.82



5. Model Saving 💾

Saved the trained XGBoost model as model.pkl and the StandardScaler as scaler.pkl for future predictions.


📈 Insights

Demographics: Younger delivery personnel (18–28) and those with high ratings (4–5) deliver faster.
Traffic & Weather: Traffic jams and adverse weather (cloudy, foggy) significantly increase delivery times.
City Impact: Urban areas are fastest; semi-urban areas are slowest due to low order frequency (0.4%).
Vehicle Condition: Poor vehicle condition (0) leads to longer delivery times.
Distance: Surprisingly, distance has a minimal effect on delivery time, indicating other factors dominate.


🌟 Future Enhancements

Feature Selection: Identify the most impactful features using techniques like SHAP values.
Advanced Feature Engineering: Incorporate real-time traffic/weather APIs and customer feedback sentiment.
Model Optimization: Explore neural networks or ensemble methods for better accuracy.
Dynamic Routing: Integrate reinforcement learning for real-time route optimization.
Scalability: Deploy the model as an API for real-time predictions (see xAI API).


📚 Dependencies

Python libraries: pandas, numpy, matplotlib, seaborn, geopy, scikit-learn, xgboost
Quarto (for rendering the analysis document)
SQLite (for database access)


📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙌 Contributing
Contributions are welcome! 🙏 Please fork the repository, create a new branch, and submit a pull request with your changes. For major updates, open an issue to discuss your ideas.

📬 Contact
For questions or feedback, reach out via GitHub Issues or contact the author at [your-email@example.com].

🍕 Happy Predicting! 🚀