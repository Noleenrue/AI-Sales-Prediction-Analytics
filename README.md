# AI Sales Prediction & Analytics System

## Project Overview

The **AI Sales Prediction & Analytics System** is an end-to-end data science and machine learning application developed using **Python, Flask, MySQL, Pandas, Scikit-learn, and Plotly**.

The system analyzes historical sales data from the Sample Superstore dataset and provides interactive business analytics dashboards, machine learning sales predictions, prediction history, and product management functionality.

The project demonstrates the integration of:

- Data preprocessing
- Exploratory Data Analysis (EDA)
- Feature engineering
- Relational database design
- SQL
- Machine learning
- Data visualization
- REST API development
- CRUD operations
- Web application development

---

## Main Features

### 1. Sales Dashboard

The interactive dashboard provides an overview of business sales performance.

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

---

### 2. Machine Learning Sales Prediction

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

Additional features are automatically derived from the supplied dates, including:

- Order Month
- Order Quarter
- Order Year
- Day of Week
- Shipping Days

---

## Machine Learning

### Models Evaluated

The following regression models were evaluated:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

The **Random Forest Regressor** was the best-performing model among the models evaluated and was selected as the final prediction model.

### Model Performance

| Metric | Test Result |
|---|---:|
| MAE | 110.03 |
| RMSE | 549.98 |
| R² | 0.351 |

The trained machine learning pipeline is stored at:

```text
ml/models/sales_prediction_model.pkl
```

> **Note:** The R² score indicates that there is still substantial unexplained variation in sales. The model therefore serves as a baseline predictive solution and provides opportunities for further feature engineering and model optimization.

---

## Model Evaluation

The application includes an **Actual vs Predicted Sales** visualization for evaluating model predictions.

The visualization compares:

- Actual sales values
- Predicted sales values
- Perfect prediction reference line

This provides a visual assessment of how closely the model's predictions correspond to observed sales values.

---

## Prediction History

Every successful sales prediction is stored in the **MySQL database**.

The Prediction History page displays information including:

- Product
- Category
- Region
- Quantity
- Discount
- Predicted Sales
- Prediction date and time

This provides a record of predictions generated through the application.

---

## Product Management

The Product Management module implements **CRUD (Create, Read, Update, Delete)** operations.

Users can:

- View products
- Add products
- Edit products
- Delete products

Products referenced by existing order records cannot be deleted, helping protect relational database integrity.

---

## REST API

The application provides REST API endpoints for product management.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | Retrieve all products |
| GET | `/api/products/<product_id>` | Retrieve a specific product |
| POST | `/api/products/` | Create a product |
| PUT | `/api/products/<product_id>` | Update a product |
| DELETE | `/api/products/<product_id>` | Delete a product |

---

## Dataset

The project uses the **Sample Superstore** dataset.

Important dataset fields include:

- Order ID
- Order Date
- Ship Date
- Ship Mode
- Customer ID
- Customer Name
- Segment
- Country
- City
- State
- Region
- Product ID
- Category
- Sub-Category
- Product Name
- Sales
- Quantity
- Discount
- Profit

---

## Database Design

The original dataset was normalized into multiple relational database tables.

### Main Tables

- Categories
- Customers
- Locations
- Orders
- OrderDetails
- Products
- ShipModes
- SubCategories
- PredictionHistory

### Main Relationships

```text
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
```

The database schema is available in:

```text
database/schema.sql
```

---

## Application Architecture

The Flask application follows a layered architecture:

```text
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
```

### Repository Layer

Responsible for database access and SQL queries.

### Service Layer

Responsible for business logic and machine learning operations.

### Route Layer

Responsible for handling HTTP requests and communication between services and templates.

### Template Layer

Responsible for presenting application data to the user through the web interface.

---

## Project Structure

```text
AI_Sales_Prediction/
│
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── processed/
│       ├── forecast_df.csv
│       └── model_validation.csv
│
├── database/
│   └── schema.sql
│
├── etl/
│   └── import_data.py
│
├── ml/
│   ├── train_model.py
│   ├── test_prediction.py
│   └── models/
│       ├── sales_prediction_model.pkl
│       └── model_evaluation.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda.ipynb
│   └── 05_sales_forecasting.ipynb
│
├── tests/
│   └── test_database.py
│
├── webapp/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── repositories/
│   │   ├── dashboard_repository.py
│   │   ├── prediction_repository.py
│   │   └── product_repository.py
│   │
│   ├── routes/
│   │   ├── home_routes.py
│   │   ├── prediction_routes.py
│   │   └── product_routes.py
│   │
│   ├── services/
│   │   ├── dashboard_service.py
│   │   ├── prediction_service.py
│   │   └── product_service.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── prediction.html
│       ├── prediction_history.html
│       ├── product_form.html
│       └── products.html
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

> The `.env` file is intentionally excluded from version control because it contains local configuration and credentials.

---

## Technologies Used

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| ML Models | Linear Regression, Random Forest, Gradient Boosting |
| Database | MySQL |
| Backend | Flask |
| Data Visualization | Plotly, Matplotlib |
| Frontend | HTML, CSS, Jinja2 |
| Development | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-Sales-Prediction-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as a template:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
FLASK_SECRET_KEY=your_secret_key
```

**Never commit the real `.env` file or database credentials to GitHub.**

---

## Database Setup

Create the database structure using:

```text
database/schema.sql
```

Then run the ETL script to load the Sample Superstore dataset into MySQL:

```bash
python etl/import_data.py
```

---

## Running the Application

From the project root, run:

```bash
python webapp/app.py
```

The Flask development server will normally be available locally at:

```text
http://127.0.0.1:5000
```

### Application Pages

| Page | Local Route |
|---|---|
| Dashboard | `/` |
| Sales Prediction | `/predict` |
| Prediction History | `/prediction-history` |
| Product Management | `/products` |
| Products API | `/api/products/` |

---

## Validation and Error Handling

The application includes validation for:

- Missing form fields
- Invalid products
- Invalid quantities
- Invalid discounts
- Invalid dates
- Ship dates before order dates
- Duplicate Product IDs
- Missing products
- Product deletion conflicts
- Invalid API requests

User-friendly flash messages are displayed instead of exposing internal application errors.

---

## Future Improvements

Potential extensions include:

- User authentication
- Role-based access control
- Hyperparameter optimization
- Additional feature engineering
- Advanced machine learning models
- Dashboard filters
- Product search and pagination
- CSV/PDF report export
- Cloud deployment
- Scheduled model retraining
- Expanded automated testing

---

## Conclusion

The **AI Sales Prediction & Analytics System** demonstrates an end-to-end data science workflow that combines data preprocessing, exploratory analysis, feature engineering, relational database design, machine learning, visualization, REST APIs, and web application development.

The project provides both **descriptive analytics** through the interactive sales dashboard and **predictive analytics** through the machine learning sales prediction module.