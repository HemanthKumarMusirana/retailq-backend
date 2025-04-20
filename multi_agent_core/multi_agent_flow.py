import pandas as pd
import numpy as np

from agents.demand_forecasting_agent import DemandForecastingAgent
from agents.inventory_monitoring_agent import InventoryMonitoringAgent
from agents.pricing_agent import PricingAgent

class MultiAgentCoordinator:
    def __init__(self):
        self.forecast_file = 'data/demand_forecasting.csv'
        self.inventory_file = 'data/inventory_monitoring.csv'
        self.pricing_file = 'data/pricing_optimization.csv'

    def run_pipeline(self):
        print("✅ Multi-Agent Flow is running with updated logic!")

        # Step 1: Run Demand Forecasting Agent
        forecast_agent = DemandForecastingAgent(self.forecast_file)
        forecast_data = forecast_agent.predict_demand()
        forecast_df = pd.DataFrame(forecast_data)

        # Step 2: Inventory Agent reacts to forecast
        inventory_agent = InventoryMonitoringAgent(self.inventory_file)
        inventory_result = inventory_agent.run_full_check(forecasted_demand=forecast_data)

        # Step 3: Pricing Agent uses forecast to suggest changes
        pricing_agent = PricingAgent(self.pricing_file)
        pricing_result = pricing_agent.analyze_prices()

        # 🧠 Agent Interaction Logic: Cross-agent awareness
        high_demand_threshold = 250
        high_demand_products = set(
            forecast_df[forecast_df['Predicted Sales Quantity'] > high_demand_threshold]['Product ID']
        )

        # 1. Enrich pricing suggestions based on forecast demand
        if isinstance(pricing_result, list):
            for item in pricing_result:
                pid = item.get('Product ID')
                item['Demand Tag'] = '🔥 High Demand' if pid in high_demand_products else 'Normal'

        # 2. Update inventory alerts using forecast context
        expiring_soon = inventory_result.get("expiring_soon", [])
        if isinstance(expiring_soon, list):
            for alert in expiring_soon:
                pid = alert.get("Product ID")
                if pid in high_demand_products:
                    alert["Forecast Flag"] = "⚠️ High Demand"
                    alert["Reorder Point"] = int(alert["Reorder Point"] * 1.2)
                else:
                    alert["Forecast Flag"] = "✅ Stable"

        # Ensure all parts are JSON-serializable
        if isinstance(forecast_df, pd.DataFrame):
            forecast_data = forecast_df.to_dict(orient="records")

        return {
            "forecast": forecast_data,
            "inventory": {
                "expiring_soon": expiring_soon
            },
            "pricing": pricing_result
        }

def run_multi_agent_flow():
    coordinator = MultiAgentCoordinator()
    return coordinator.run_pipeline()
