import pandas as pd

class PricingAgent:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    def analyze_prices(self):
        suggestions = []

        for _, row in self.df.iterrows():
            price_gap = row["Price"] - row["Competitor Prices"]
            low_sales = row["Sales Volume"] < 50
            high_return = row["Return Rate (%)"] > 10
            sensitive = row["Elasticity Index"] > 1.5

            if price_gap > 10 and low_sales and sensitive:
                suggestions.append({
                    "Product ID": row["Product ID"],
                    "Store ID": row["Store ID"],
                    "Current Price": row["Price"],
                    "Competitor Price": row["Competitor Prices"],
                    "Sales Volume": row["Sales Volume"],
                    "Suggestion": "Consider reducing price by 10–15% to improve competitiveness."
                })

        return suggestions
