# AI Sales Prediction System

## Project Overview

The AI Sales Prediction System is a web-based data analytics and machine learning application developed using Python, Flask, MySQL, Plotly, Pandas, and Scikit-learn.

The system analyzes historical sales data from the Sample Superstore dataset and provides interactive sales dashboards, machine learning sales predictions, prediction history, and product management functionality.

The application demonstrates the integration of:

- Data preprocessing
- Exploratory data analysis
- Relational database design
- SQL
- Machine learning
- Data visualization
- REST API development
- CRUD operations
- Web application development


## Main Features

### 1. Sales Dashboard

The dashboard provides an overview of business sales performance.

It includes:

- Total Sales
- Total Profit
- Total Orders
- Total Quantity
- Monthly Sales Trend
- Sales by Product Category
- Profit by Product Category
- Sales by Region
- Profit by Region
- Top 10 Products by Sales
- Discount vs Average Profit


## 2. Machine Learning Sales Prediction

The system uses a trained machine learning model to predict expected sales for a transaction.

The user provides:

- Product
- Customer Segment
- Region
- Ship Mode
- Quantity
- Discount
- Order Date
- Ship Date

Additional features are automatically calculated from the supplied dates.

These include:

- Order Month
- Order Quarter
- Order Year
- Day of Week
- Shipping Days


## 3. Machine Learning Models

The following regression models were evaluated:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Random Forest Regressor achieved the best performance and was selected as the final model.

Approximate test performance:

- MAE: 110.03
- RMSE: 549.98
- R²: 0.351

The trained machine learning pipeline is stored as:

```text
ml/models/sales_prediction_model.pkl

## 4. Model Evaluation

The dashboard contains an Actual vs Predicted Sales visualization.

It compares:

Actual sales values
Model predictions
Perfect prediction reference line

This visualization helps evaluate how closely predicted sales values correspond to the real values.

## 5. Prediction History

Every successful sales prediction is stored in the MySQL database.

The Prediction History page displays information including:

Product
Category
Region
Quantity
Discount
Predicted Sales
Prediction date/time

## 6. Product Management

The Product Management module implements CRUD operations.

The system allows users to:

View products
Add products
Edit products
Delete products

Products already referenced by existing order records cannot be deleted, protecting relational database integrity.

## 7. REST API

The application also provides REST API endpoints for product management.

Examples:

GET    /api/products/
GET    /api/products/<product_id>
POST   /api/products/
PUT    /api/products/<product_id>
DELETE /api/products/<product_id>


##Dataset

The project uses the Sample Superstore dataset.

Important dataset fields include:

Order ID
Order Date
Ship Date
Ship Mode
Customer ID
Customer Name
Segment
Country
City
State
Region
Product ID
Category
Sub-Category
Product Name
Sales
Quantity
Discount
Profit
Database Design

The original dataset was normalized into several relational database tables.

##Main tables:

Categories
Customers
Locations
Orders
OrderDetails
Products
ShipModes
SubCategories
PredictionHistory

##Main relationships:

Categories
    ↓
SubCategories
    ↓
Products
    ↓
OrderDetails



Customers
    ↓
Orders
    ↓
OrderDetails


ShipModes
    ↓
Orders


Locations
    ↓
OrderDetails


##Application Architecture

The application follows a layered architecture.

MySQL Database
      ↓
Repository Layer
      ↓
Service Layer
      ↓
Flask Routes
      ↓
Jinja Templates
      ↓
Browser

##Repository Layer

Responsible for database queries and database access.

##Service Layer

Responsible for business logic and machine learning operations.

##Route Layer

Responsible for HTTP requests and communication between the browser, services, and templates.

##Template Layer

Responsible for presenting information to the user.

##Project Structure

AI_Sales_Prediction
│
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── ml
│   ├── train_model.py
│   ├── test_prediction.py
│   │
│   └── models
│       ├── sales_prediction_model.pkl
│       └── model_evaluation.csv
│
└── webapp
    │
    ├── app.py
    ├── database.py
    │
    ├── routes
    │   ├── home_routes.py
    │   ├── product_routes.py
    │   └── prediction_routes.py
    │
    ├── services
    │   ├── dashboard_service.py
    │   ├── product_service.py
    │   └── prediction_service.py
    │
    ├── repositories
    │   ├── dashboard_repository.py
    │   ├── product_repository.py
    │   └── prediction_repository.py
    │
    ├── templates
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── prediction.html
    │   ├── prediction_history.html
    │   ├── products.html
    │   └── product_form.html
    │
    └── static
        ├── css
        │   └── style.css
        │
        └── js
            └── app.js


##Technologies Used

Backend
Python
Flask

Database
MySQL
MySQL Connector/Python

Machine Learning
Scikit-learn
Random Forest Regressor
Linear Regression
Gradient Boosting Regressor

Data Analysis
Pandas
NumPy

Data Visualization
Plotly

Frontend
HTML
CSS
Jinja2

##Installation

Install the required Python packages:

pip install flask
pip install mysql-connector-python
pip install pandas
pip install numpy
pip install scikit-learn
pip install joblib
pip install plotly
pip install python-dotenv

##Environment Configuration

Create a .env file in the project root.

Example:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name

FLASK_SECRET_KEY=your_secret_key

##Running the Application

Open PowerShell and navigate to the project directory:

cd C:\Users\nolee\Desktop\AI_Sales_Prediction

Run:

python webapp/app.py

The Flask application should start on:

http://127.0.0.1:5000

Open this address in a web browser.

Main Application Pages
Dashboard
http://127.0.0.1:5000/

Sales Prediction
http://127.0.0.1:5000/predict

Prediction History
http://127.0.0.1:5000/prediction-history

Product Management
http://127.0.0.1:5000/products

Products API
http://127.0.0.1:5000/api/products/


##Validation and Error Handling

The application includes validation for:

Missing form fields
Invalid products
Invalid quantities
Invalid discounts
Invalid dates
Ship dates before order dates
Duplicate Product IDs
Missing products
Product deletion conflicts
Invalid API requests

User-friendly flash messages are displayed rather than exposing internal application errors.

##Future Improvements

Possible extensions include:

User authentication
Role-based access control
More advanced machine learning models
Hyperparameter optimization
Additional dashboard filters
Product search and pagination
CSV/PDF report export
Cloud deployment
Scheduled model retraining
Automated testing


##Conclusion

The AI Sales Prediction System demonstrates how data engineering, relational databases, machine learning, visualization, REST APIs, and web development can be combined into a complete data-driven application.

The project provides both descriptive analytics through the sales dashboard and predictive analytics through the machine learning sales prediction module.


