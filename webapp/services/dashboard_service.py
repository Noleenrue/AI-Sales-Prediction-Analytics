import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

try:
    from ..repositories.dashboard_repository import DashboardRepository
except ImportError:
    from repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self):

        self.repository = DashboardRepository()


    def get_dashboard_kpis(self):

        return self.repository.get_dashboard_kpis()


    def get_monthly_sales(self):

        return self.repository.get_monthly_sales()


    def get_sales_by_category(self):

        return self.repository.get_sales_by_category()


    def get_profit_by_category(self):

        return self.repository.get_profit_by_category()

    def get_sales_by_region(self):

        return self.repository.get_sales_by_region()

    def get_profit_by_region(self):

        return self.repository.get_profit_by_region()

    def get_top_10_products(self):

        return self.repository.get_top_10_products()

    def get_discount_vs_profit(self):

        return self.repository.get_discount_vs_profit()

    def get_model_evaluation_chart(self):

        evaluation_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "ml",
                "models",
                "model_evaluation.csv"
            )
        )

        df = pd.read_csv(evaluation_path)

        minimum_value = min(
            df["ActualSales"].min(),
            df["PredictedSales"].min()
        )

        maximum_value = max(
            df["ActualSales"].max(),
            df["PredictedSales"].max()
        )

        figure = go.Figure()

        # Actual vs predicted points
        figure.add_trace(
            go.Scatter(
                x=df["ActualSales"],
                y=df["PredictedSales"],
                mode="markers",
                name="Predictions",
                marker=dict(
                    size=7,
                    opacity=0.6
                )
            )
        )

        # Perfect prediction line
        figure.add_trace(
            go.Scatter(
                x=[minimum_value, maximum_value],
                y=[minimum_value, maximum_value],
                mode="lines",
                name="Perfect Prediction"
            )
        )

        figure.update_layout(
            title="Actual vs Predicted Sales",
            xaxis_title="Actual Sales",
            yaxis_title="Predicted Sales",
            template="plotly_white",
            height=550,
            legend=dict(
                orientation="h",
                y=1.1
            )
        )

        chart_html = pio.to_html(
            figure,
            full_html=False,
            config={
                "responsive": True
            }
        )

        return chart_html