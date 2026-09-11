-- ============================================================
-- AI SALES PREDICTION SYSTEM
-- DATABASE SCHEMA
-- ============================================================

CREATE DATABASE IF NOT EXISTS ai_sales_prediction;

USE ai_sales_prediction;


-- ============================================================
-- 1. CATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);


-- ============================================================
-- 2. SUBCATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS SubCategories (
    SubCategoryID INT AUTO_INCREMENT PRIMARY KEY,
    SubCategoryName VARCHAR(100) NOT NULL,
    CategoryID INT NOT NULL,

    CONSTRAINT fk_subcategory_category
        FOREIGN KEY (CategoryID)
        REFERENCES Categories(CategoryID)
);


-- ============================================================
-- 3. PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS Products (
    ProductID VARCHAR(50) PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    SubCategoryID INT NOT NULL,

    CONSTRAINT fk_product_subcategory
        FOREIGN KEY (SubCategoryID)
        REFERENCES SubCategories(SubCategoryID)
);


-- ============================================================
-- 4. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS Customers (
    CustomerID VARCHAR(50) PRIMARY KEY,
    CustomerName VARCHAR(150) NOT NULL,
    Segment VARCHAR(50) NOT NULL
);


-- ============================================================
-- 5. SHIP MODES
-- ============================================================

CREATE TABLE IF NOT EXISTS ShipModes (
    ShipModeID INT AUTO_INCREMENT PRIMARY KEY,
    ShipMode VARCHAR(50) NOT NULL UNIQUE
);


-- ============================================================
-- 6. LOCATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS Locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    Country VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    PostalCode INT NULL,
    Region VARCHAR(50) NOT NULL
);


-- ============================================================
-- 7. ORDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS Orders (
    OrderID VARCHAR(50) PRIMARY KEY,
    OrderDate DATE NOT NULL,
    ShipDate DATE NOT NULL,
    CustomerID VARCHAR(50) NOT NULL,
    ShipModeID INT NOT NULL,

    CONSTRAINT fk_order_customer
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID),

    CONSTRAINT fk_order_shipmode
        FOREIGN KEY (ShipModeID)
        REFERENCES ShipModes(ShipModeID)
);


-- ============================================================
-- 8. ORDER DETAILS
-- ============================================================

CREATE TABLE IF NOT EXISTS OrderDetails (
    RowID INT PRIMARY KEY,
    OrderID VARCHAR(50) NOT NULL,
    ProductID VARCHAR(50) NOT NULL,
    LocationID INT NOT NULL,
    Sales DECIMAL(12,2) NOT NULL,
    Quantity INT NOT NULL,
    Discount DECIMAL(5,2) NOT NULL,
    Profit DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_orderdetails_order
        FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    CONSTRAINT fk_orderdetails_product
        FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID),

    CONSTRAINT fk_orderdetails_location
        FOREIGN KEY (LocationID)
        REFERENCES Locations(LocationID)
);


-- ============================================================
-- 9. PREDICTION HISTORY
-- ============================================================

CREATE TABLE IF NOT EXISTS PredictionHistory (
    PredictionID INT AUTO_INCREMENT PRIMARY KEY,
    Product VARCHAR(255) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    SubCategory VARCHAR(100) NOT NULL,
    Segment VARCHAR(50) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    ShipMode VARCHAR(50) NOT NULL,
    Quantity INT NOT NULL,
    Discount DECIMAL(5,2) NOT NULL,
    OrderDate DATE NOT NULL,
    ShipDate DATE NOT NULL,
    PredictedSales DECIMAL(12,2) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- END OF DATABASE SCHEMA
-- ============================================================