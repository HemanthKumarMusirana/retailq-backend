import pandas as pd
from datetime import datetime, timedelta

class InventoryMonitoringAgent:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, parse_dates=["Expiry Date"])

    def check_restock_needed(self):
        restock_df = self.df[self.df["Stock Levels"] < self.df["Reorder Point"]]
        return restock_df.to_dict(orient="records")

    def check_expiring_soon(self, days=30):
        today = datetime.today()
        cutoff = today + timedelta(days=days)
        expiring_df = self.df[self.df["Expiry Date"] <= cutoff]
        return expiring_df.to_dict(orient="records")

    def run_full_check(self, forecasted_demand=None):
        # Step 1: Adjust reorder point if high forecast is present
        if forecasted_demand:
            forecast_df = pd.DataFrame(forecasted_demand)
            high_demand = forecast_df[forecast_df["Predicted Sales Quantity"] > 250]["Product ID"].unique()
            self.df.loc[self.df["Product ID"].isin(high_demand), "Reorder Point"] *= 1.2  # +20%
            self.df.loc[self.df["Product ID"].isin(high_demand), "Forecast Flag"] = "⚠️ High Demand"
            self.df["Forecast Flag"].fillna("✅ Stable", inplace=True)

        return {
            "restock_needed": self.check_restock_needed(),
            "expiring_soon": self.check_expiring_soon()
        }
