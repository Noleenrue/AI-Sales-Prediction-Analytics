from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for
)

from datetime import datetime, date

try:
    from ..services.prediction_service import PredictionService
    from ..repositories.prediction_repository import (
    get_products_for_prediction,
    save_prediction_history,
    get_prediction_history
)

except ImportError:
    from services.prediction_service import PredictionService
    from repositories.prediction_repository import (
        get_products_for_prediction,
        save_prediction_history,
        get_prediction_history
    )


prediction_bp = Blueprint(
    "prediction",
    __name__
)

prediction_service = PredictionService()


@prediction_bp.route("/predict", methods=["GET", "POST"])
def predict():

    predicted_sales = None
    products = get_products_for_prediction()

    if request.method == "POST":

        try:
            # ---------------------------------
            # GET FORM VALUES
            # ---------------------------------

            product_name = request.form.get(
                "product", ""
            ).strip()

            segment = request.form.get(
                "segment", ""
            ).strip()

            region = request.form.get(
                "region", ""
            ).strip()

            ship_mode = request.form.get(
                "shipmode", ""
            ).strip()

            quantity_text = request.form.get(
                "quantity", ""
            ).strip()

            discount_text = request.form.get(
                "discount", ""
            ).strip()

            order_date_text = request.form.get(
                "order_date", ""
            ).strip()

            ship_date_text = request.form.get(
                "ship_date", ""
            ).strip()


            # ---------------------------------
            # REQUIRED FIELDS
            # ---------------------------------

            if not product_name:
                raise ValueError(
                    "Please select a product."
                )

            if not segment:
                raise ValueError(
                    "Please select a customer segment."
                )

            if not region:
                raise ValueError(
                    "Please select a region."
                )

            if not ship_mode:
                raise ValueError(
                    "Please select a ship mode."
                )

            if not quantity_text:
                raise ValueError(
                    "Quantity is required."
                )

            if not discount_text:
                raise ValueError(
                    "Discount is required."
                )

            if not order_date_text:
                raise ValueError(
                    "Order date is required."
                )

            if not ship_date_text:
                raise ValueError(
                    "Ship date is required."
                )


            # ---------------------------------
            # PRODUCT VALIDATION
            # ---------------------------------

            selected_product = next(
                (
                    product
                    for product in products
                    if product["Product"]
                    == product_name
                ),
                None
            )

            if selected_product is None:
                raise ValueError(
                    "The selected product is invalid."
                )


            # ---------------------------------
            # QUANTITY VALIDATION
            # ---------------------------------

            try:
                quantity = int(quantity_text)
            except ValueError:
                raise ValueError(
                    "Quantity must be a whole number."
                )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )


            # ---------------------------------
            # DISCOUNT VALIDATION
            # ---------------------------------

            try:
                discount = float(discount_text)
            except ValueError:
                raise ValueError(
                    "Discount must be a valid number."
                )

            if discount < 0 or discount > 1:
                raise ValueError(
                    "Discount must be between 0 and 1."
                )


            # ---------------------------------
            # DATE VALIDATION
            # ---------------------------------

            try:
                order_date = datetime.strptime(
                    order_date_text,
                    "%Y-%m-%d"
                )

                ship_date = datetime.strptime(
                    ship_date_text,
                    "%Y-%m-%d"
                )

            except ValueError:
                raise ValueError(
                    "Please enter valid order and ship dates."
                )


            shipping_days = (
                ship_date - order_date
            ).days

            if shipping_days < 0:
                raise ValueError(
                    "Ship date cannot be before order date."
                )


            # ---------------------------------
            # FEATURE ENGINEERING
            # ---------------------------------

            order_month = order_date.month

            order_quarter = (
                (order_date.month - 1) // 3
            ) + 1

            order_year = order_date.year

            order_day_of_week = (
                (order_date.weekday() + 1) % 7
            ) + 1


            # ---------------------------------
            # MODEL INPUT
            # ---------------------------------

            input_data = {

                "Quantity": quantity,

                "Discount": discount,

                "Product":
                    selected_product["Product"],

                "Category":
                    selected_product["Category"],

                "SubCategory":
                    selected_product["SubCategory"],

                "Segment": segment,

                "Region": region,

                "ShipMode": ship_mode,

                "OrderMonth": order_month,

                "OrderQuarter": order_quarter,

                "OrderYear": order_year,

                "OrderDayOfWeek":
                    order_day_of_week,

                "ShippingDays":
                    shipping_days
            }


            # ---------------------------------
            # PREDICTION
            # ---------------------------------

            predicted_sales = (
                prediction_service.predict_sales(
                    input_data
                )
            )


            # ---------------------------------
            # SAVE PREDICTION HISTORY
            # ---------------------------------

            history_data = {

                "Product":
                    selected_product["Product"],

                "Category":
                    selected_product["Category"],

                "SubCategory":
                    selected_product["SubCategory"],

                "Segment": segment,

                "Region": region,

                "ShipMode": ship_mode,

                "Quantity": quantity,

                "Discount": discount,

                "OrderDate":
                    order_date.date(),

                "ShipDate":
                    ship_date.date(),

                "PredictedSales":
                    predicted_sales
            }

            save_prediction_history(
                history_data
            )


            flash(
                "Sales prediction generated successfully.",
                "success"
            )


        except ValueError as error:

            flash(
                str(error),
                "error"
            )


        except Exception:

            flash(
                "An unexpected error occurred while "
                "generating the prediction. "
                "Please try again.",
                "error"
            )


    return render_template(
        "prediction.html",
        predicted_sales=predicted_sales,
        products=products
    )

    

@prediction_bp.route("/prediction-history")
def prediction_history():

    history = get_prediction_history()

    return render_template(
        "prediction_history.html",
        history=history
    )