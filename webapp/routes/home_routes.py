from flask import Blueprint, render_template

try:
    from ..services.dashboard_service import DashboardService
except ImportError:
    from services.dashboard_service import DashboardService

import plotly.graph_objects as go
import plotly.io as pio


home_bp = Blueprint(
    "home",
    __name__
)

dashboard_service = DashboardService()

@home_bp.route("/")
def dashboard():

    kpis = dashboard_service.get_dashboard_kpis()

    # -------------------------
    # MONTHLY SALES
    # -------------------------

    monthly_sales = dashboard_service.get_monthly_sales()

    months = [
        row["month"]
        for row in monthly_sales
    ]

    sales = [
        float(row["total_sales"])
        for row in monthly_sales
    ]

    monthly_sales_chart = go.Figure()

    monthly_sales_chart.add_trace(
        go.Scatter(
            x=months,
            y=sales,
            mode="lines+markers",
            name="Sales"
        )
    )

    monthly_sales_chart.update_layout(
        title="Monthly Sales Trend",
        xaxis_title="Month",
        yaxis_title="Total Sales",
        template="plotly_white"
    )

    monthly_sales_chart = pio.to_html(
        monthly_sales_chart,
        full_html=False,
        config={"responsive": True}
    )


    # -------------------------
    # SALES BY CATEGORY
    # -------------------------

    sales_by_category = dashboard_service.get_sales_by_category()

    categories = [
        row["category"]
        for row in sales_by_category
    ]

    category_sales = [
        float(row["total_sales"])
        for row in sales_by_category
    ]

    category_chart = go.Figure()

    category_chart.add_trace(
        go.Bar(
            x=categories,
            y=category_sales,
            name="Sales"
        )
    )

    category_chart.update_layout(
        title="Sales by Product Category",
        xaxis_title="Category",
        yaxis_title="Total Sales",
        template="plotly_white"
    )

    category_chart = pio.to_html(
        category_chart,
        full_html=False,
        config={"responsive": True}
    )

    # -------------------------
    # PROFIT BY CATEGORY
    # -------------------------

    profit_by_category = dashboard_service.get_profit_by_category()

    categories_profit = [
        row["category"]
        for row in profit_by_category
    ]

    category_profit = [
        float(row["total_profit"])
        for row in profit_by_category
    ]

    profit_chart = go.Figure()

    profit_chart.add_trace(
        go.Bar(
            x=categories_profit,
            y=category_profit,
            name="Profit"
        )
    )

    profit_chart.update_layout(
        title="Profit by Product Category",
        xaxis_title="Category",
        yaxis_title="Total Profit",
        template="plotly_white"
    )

    profit_chart = pio.to_html(
        profit_chart,
        full_html=False,
        config={"responsive": True}
    )

    # -------------------------
    # SALES BY REGION
    # -------------------------

    sales_by_region = dashboard_service.get_sales_by_region()

    regions = [
        row["region"]
        for row in sales_by_region
    ]

    region_sales = [
        float(row["total_sales"])
        for row in sales_by_region
    ]

    region_chart = go.Figure()

    region_chart.add_trace(
        go.Bar(
            x=regions,
            y=region_sales,
            name="Sales"
        )
    )

    region_chart.update_layout(
        title="Sales by Region",
        xaxis_title="Region",
        yaxis_title="Total Sales",
        template="plotly_white"
    )

    region_chart = pio.to_html(
        region_chart,
        full_html=False,
        config={"responsive": True}
    )

    # -------------------------
    # PROFIT BY REGION
    # -------------------------

    profit_by_region = dashboard_service.get_profit_by_region()

    regions_profit = [
        row["region"]
        for row in profit_by_region
    ]

    region_profit = [
        float(row["total_profit"])
        for row in profit_by_region
    ]

    profit_region_chart = go.Figure()

    profit_region_chart.add_trace(
        go.Bar(
            x=regions_profit,
            y=region_profit,
            name="Profit"
        )
    )

    profit_region_chart.update_layout(
        title="Profit by Region",
        xaxis_title="Region",
        yaxis_title="Total Profit",
        template="plotly_white"
    )

    profit_region_chart = pio.to_html(
        profit_region_chart,
        full_html=False,
        config={"responsive": True}
    )

    # -------------------------
    # TOP 10 PRODUCTS
    # -------------------------

    top_10_products = dashboard_service.get_top_10_products()

    products = [
        row["product"]
        for row in top_10_products
    ]

    product_sales = [
        float(row["total_sales"])
        for row in top_10_products
    ]

    top_products_chart = go.Figure()

    top_products_chart.add_trace(
        go.Bar(
            x=product_sales,
            y=products,
            orientation="h",
            name="Sales",
            text=[
                f"${value:,.0f}"
                for value in product_sales
            ],
            textposition="outside"
        )
    )

    top_products_chart.update_layout(
        title="Top 10 Products by Sales",
        xaxis_title="Total Sales",
        yaxis_title="",
        template="plotly_white",
        height=600,
        margin=dict(
            l=20,
            r=80,
            t=70,
            b=50
        )
    )

    top_products_chart.update_yaxes(
        autorange="reversed"
    )

    top_products_chart = pio.to_html(
        top_products_chart,
        full_html=False,
        config={"responsive": True}
    )

    
    # -------------------------
    # DISCOUNT VS PROFIT
    # -------------------------

    discount_vs_profit = dashboard_service.get_discount_vs_profit()

    discounts = [
        float(row["Discount"])
        for row in discount_vs_profit
    ]

    avg_profits = [
        float(row["avg_profit"])
        for row in discount_vs_profit
    ]

    discount_profit_chart = go.Figure()

    discount_profit_chart.add_trace(
        go.Scatter(
            x=discounts,
            y=avg_profits,
            mode="markers+lines",
            name="Avg Profit"
        )
    )

    discount_profit_chart.update_layout(
        title="Discount vs Average Profit",
        xaxis_title="Discount",
        yaxis_title="Average Profit",
        template="plotly_white"
    )

    discount_profit_chart = pio.to_html(
        discount_profit_chart,
        full_html=False,
        config={"responsive": True}
    )


    # -------------------------
    # MODEL EVALUATION
    # -------------------------

    model_evaluation_chart = (
        dashboard_service.get_model_evaluation_chart()
    )


    return render_template(
        "dashboard.html",
        kpis=kpis,
        monthly_sales_chart=monthly_sales_chart,
        category_chart=category_chart,
        profit_chart=profit_chart,
        region_chart=region_chart,
        profit_region_chart=profit_region_chart,
        top_products_chart=top_products_chart,
        discount_profit_chart=discount_profit_chart,
        model_evaluation_chart=model_evaluation_chart
    )