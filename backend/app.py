from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import agents after sys.path update
from agents.inventory_monitoring_agent import InventoryMonitoringAgent
from agents.pricing_agent import PricingAgent
from agents.demand_forecasting_agent import DemandForecastingAgent
from multi_agent_core.multi_agent_flow import run_multi_agent_flow

app = Flask(__name__)

# ✅ Full CORS setup to avoid browser block
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ------------------------ ROUTES ------------------------

@app.route("/")
def home():
    return jsonify({"message": "Retail_AI backend is live 🚀"})

@app.route("/inventory", methods=["GET"])
def inventory_check():
    agent = InventoryMonitoringAgent("data/inventory_monitoring.csv")
    result = agent.run_full_check()
    return jsonify(result)

@app.route("/pricing", methods=["GET"])
def pricing_analysis():
    agent = PricingAgent("data/pricing_optimization.csv")
    result = agent.analyze_prices()
    return jsonify(result)

@app.route("/forecast", methods=["GET"])
def forecast():
    df = pd.read_csv("data/demand_forecasting.csv")
    df['Predicted Sales Quantity'] = np.random.randint(200, 300, size=len(df))
    output = df[['Product ID', 'Store ID', 'Date', 'Predicted Sales Quantity']].head(10)
    return jsonify(output.to_dict(orient='records'))

@app.route("/maf", methods=["GET"])
def multi_agent_flow():
    try:
        result = run_multi_agent_flow()

        # ✅ Convert any DataFrames to JSON-serializable format
        if 'inventory' in result and isinstance(result['inventory'], dict):
            if 'expiring_soon' in result['inventory'] and hasattr(result['inventory']['expiring_soon'], 'to_dict'):
                result['inventory']['expiring_soon'] = result['inventory']['expiring_soon'].to_dict(orient="records")

        if 'pricing' in result and hasattr(result['pricing'], 'to_dict'):
            result['pricing'] = result['pricing'].to_dict(orient="records")

        if 'forecast' in result and hasattr(result['forecast'], 'to_dict'):
            result['forecast'] = result['forecast'].to_dict(orient="records")

        return jsonify(result)
    except Exception as e:
        print("🔥 Error in run_multi_agent_flow():", e)
        return jsonify({"error": str(e)}), 500


# ------------------------ MAIN ------------------------

if __name__ == "__main__":
    app.run(debug=True)
