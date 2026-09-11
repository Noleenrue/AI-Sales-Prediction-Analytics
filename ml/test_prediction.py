import os
import joblib
import pandas as pd


# Locate saved model
model_path = os.path.join(
    os.path.dirname(__file__),
    "models",
    "sales_prediction_model.pkl"
)

# Load model
model = joblib.load(model_path)


# Example new transaction
new_data = pd.DataFrame([
    {
        "Quantity": 4,
        "Discount": 0.15,
        "Product": "Sauder Camden County Barrister Bookcase, Planked Cherry Finish",
        "Category": "Furniture",
        "SubCategory": "Bookcases",
        "Segment": "Consumer",
        "Region": "West",
        "ShipMode": "Standard Class",
        "OrderMonth": 9,
        "OrderQuarter": 3,
        "OrderYear": 2015,
        "OrderDayOfWeek": 7,
        "ShippingDays": 4
    }
])


prediction = model.predict(new_data)

print("-----------------------------")
print("SALES PREDICTION")
print("-----------------------------")
print(f"Predicted Sales: ${prediction[0]:,.2f}")