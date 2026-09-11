import os
import joblib
import pandas as pd
import mysql.connector

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD123",
    database="ai_sales_prediction"
)


# ---------------------------------------------------------
# SQL QUERY
# ---------------------------------------------------------

query = """
SELECT
    od.Sales,
    od.Quantity,
    od.Discount,

    p.ProductName AS Product,

    c.CategoryName AS Category,
    sc.SubCategoryName AS SubCategory,

    cu.Segment,
    l.Region,
    sm.ShipMode AS ShipMode,

    MONTH(o.OrderDate) AS OrderMonth,
    QUARTER(o.OrderDate) AS OrderQuarter,
    YEAR(o.OrderDate) AS OrderYear,

    DAYOFWEEK(o.OrderDate) AS OrderDayOfWeek,

    DATEDIFF(
        o.ShipDate,
        o.OrderDate
    ) AS ShippingDays

FROM OrderDetails od

INNER JOIN Orders o
    ON od.OrderID = o.OrderID

INNER JOIN Products p
    ON od.ProductID = p.ProductID

INNER JOIN SubCategories sc
    ON p.SubCategoryID = sc.SubCategoryID

INNER JOIN Categories c
    ON sc.CategoryID = c.CategoryID

INNER JOIN Customers cu
    ON o.CustomerID = cu.CustomerID

INNER JOIN Locations l
    ON od.LocationID = l.LocationID

INNER JOIN ShipModes sm
    ON o.ShipModeID = sm.ShipModeID
"""


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_sql(query, connection)

connection.close()

print("Dataset loaded successfully.")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())


# ---------------------------------------------------------
# FEATURES AND TARGET
# ---------------------------------------------------------

X = df.drop(columns=["Sales"])
y = df["Sales"]


# ---------------------------------------------------------
# DEFINE FEATURE TYPES
# ---------------------------------------------------------

numeric_features = [
    "Quantity",
    "Discount",
    "OrderMonth",
    "OrderQuarter",
    "OrderYear",
    "OrderDayOfWeek",
    "ShippingDays"
]

categorical_features = [
    "Product",
    "Category",
    "SubCategory",
    "Segment",
    "Region",
    "ShipMode"
]


# ---------------------------------------------------------
# PREPROCESSING
# ---------------------------------------------------------

numeric_transformer = Pipeline(
    steps=[
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


# ---------------------------------------------------------
# CREATE PIPELINE
# ---------------------------------------------------------

# Select the model you want to use
model_name = "Linear Regression"  # Change this to "Linear Regression" or "Gradient Boosting" as needed
model = models[model_name]

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ---------------------------------------------------------
# PREDICTIONS
# ---------------------------------------------------------

y_pred = pipeline.predict(X_test)


# ---------------------------------------------------------
# EVALUATION
# ---------------------------------------------------------

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)

print("\nMODEL PERFORMANCE")
print("-----------------------------")

print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²:   {r2:.4f}")


# ---------------------------------------------------------
# SHOW SAMPLE PREDICTIONS
# ---------------------------------------------------------

results = []

best_model = None
best_model_name = None
best_r2 = float("-inf")

for model_name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    print(f"\nTraining {model_name}...")

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    mse = mean_squared_error(
        y_test,
        y_pred
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        y_pred
    )

    results.append({
        "Model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.4f}")

    # Select best model
    if r2 > best_r2:
        best_r2 = r2
        best_model = pipeline
        best_model_name = model_name

results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON")
print("---------------------------------------------")
print(results_df)


# ---------------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------------

model_directory = os.path.join(
    os.path.dirname(__file__),
    "models"
)

os.makedirs(
    model_directory,
    exist_ok=True
)

model_path = os.path.join(
    model_directory,
    "sales_prediction_model.pkl"
)

joblib.dump(
    best_model,
    model_path
)

print("\nBest Model:", best_model_name)
print(f"Best R²: {best_r2:.4f}")

print(
    "Best model saved to:",
    model_path
)



evaluation_df = pd.DataFrame({
    "ActualSales": y_test.values,
    "PredictedSales": best_model.predict(X_test)
})

evaluation_path = os.path.join(
    model_directory,
    "model_evaluation.csv"
)

evaluation_df.to_csv(
    evaluation_path,
    index=False
)

print(
    "Evaluation data saved to:",
    evaluation_path
)