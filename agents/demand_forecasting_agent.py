import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DemandForecastingAgent:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def preprocess_data(self, df):
        df = df.copy()
        
        # Drop rows with missing values
        df.dropna(inplace=True)

        # Convert Date to datetime and extract features
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.month
        df['Weekday'] = df['Date'].dt.weekday

        # Encode categorical columns
        categorical_cols = ['Promotions', 'Seasonality Factors', 'External Factors', 'Demand Trend', 'Customer Segments']
        label_encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

        # Drop the original Date column
        df.drop(columns=['Date'], inplace=True)

        return df

    def predict_demand(self):
        # Load data
        df = pd.read_csv(self.csv_path)

        # Preprocess
        df = self.preprocess_data(df)

        # Features and target
        X = df.drop(columns=['Sales Quantity'])
        y = df['Sales Quantity']

        # Train/test split (just for safety, we train on all here)
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict (here we just re-predict on the input data for simplicity)
        df['Predicted Sales Quantity'] = model.predict(X)

        # Format for output
        output = df[['Product ID', 'Store ID', 'Price', 'Predicted Sales Quantity']].to_dict(orient="records")
        return output
