import os
import joblib
import pandas as pd


class PredictionService:

    def __init__(self):

        model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "ml",
            "models",
            "sales_prediction_model.pkl"
        )

        model_path = os.path.abspath(model_path)

        self.model = joblib.load(model_path)


    def predict_sales(self, input_data):

        df = pd.DataFrame([
            input_data
        ])

        prediction = self.model.predict(df)

        return float(prediction[0])