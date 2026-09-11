import pandas as pd
import mysql.connector

# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PASSWORD123",
    database="ai_sales_prediction"
)

cursor = connection.cursor()

print("Successfully connected to MySQL!")

# ==========================================
# LOAD CLEANED DATA
# ==========================================

df = pd.read_csv(
    "data/raw/superstore.csv",
    encoding="cp1252"
)

print("Dataset loaded successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

#==========================================
# CONVERT DATE COLUMNS
#==========================================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ==========================================
# INSERT CATEGORIES
# ==========================================

cursor.execute("SELECT CategoryName FROM Categories")
existing_categories = {name for (name,) in cursor.fetchall()}

for category in df["Category"].drop_duplicates():
    if category in existing_categories:
        continue

    cursor.execute(
        """
        INSERT INTO Categories (CategoryName)
        VALUES (%s)
        """,
        (category,)
    )
    existing_categories.add(category)

connection.commit()

print("Categories inserted.")

# ==========================================
# INSERT CATEGORY ID
# ==========================================

cursor.execute(
    "SELECT CategoryID, CategoryName FROM Categories"
)

category_map = {
    name: category_id
    for category_id, name in cursor.fetchall()
}

print(category_map)

# ==========================================
# INSERT SUB-CATEGORIES
# ==========================================

cursor.execute(
    "SELECT SubCategoryID, SubCategoryName, CategoryID FROM SubCategories"
)
existing_subcategories = {
    (subcategory_name, category_id)
    for _, subcategory_name, category_id in cursor.fetchall()
}

subcategories = (
    df[["Sub-Category", "Category"]]
    .drop_duplicates()
)

for _, row in subcategories.iterrows():
    subcategory = row["Sub-Category"]
    category = row["Category"]

    category_id = category_map[category]
    subcategory_key = (subcategory, category_id)

    if subcategory_key in existing_subcategories:
        continue

    cursor.execute(
        """
        INSERT INTO SubCategories
        (SubCategoryName, CategoryID)
        VALUES (%s, %s)
        """,
        (subcategory, category_id)
    )
    existing_subcategories.add(subcategory_key)

connection.commit()

print("SubCategories inserted.")

# ==========================================
# RETRIEVE SUBCATEGORY IDS
# ==========================================
cursor.execute(
    """
    SELECT SubCategoryID, SubCategoryName
    FROM SubCategories
    """
)

subcategory_map = {
    name: subcategory_id
    for subcategory_id, name in cursor.fetchall()
}

print(subcategory_map)

# ==========================================
# INSERT PRODUCTS
# ==========================================

cursor.execute("SELECT ProductID FROM Products")
existing_products = {product_id for (product_id,) in cursor.fetchall()}

products = (
    df[
        [
            "Product ID",
            "Product Name",
            "Sub-Category"
        ]
    ]
    .drop_duplicates()
)

for _, row in products.iterrows():

    product_id = row["Product ID"]
    if product_id in existing_products:
        continue

    product_name = row["Product Name"]
    subcategory = row["Sub-Category"]

    subcategory_id = subcategory_map[subcategory]

    cursor.execute(
        """
        INSERT INTO Products
        (
            ProductID,
            ProductName,
            SubCategoryID
        )
        VALUES (%s, %s, %s)
        """,
        (
            product_id,
            product_name,
            subcategory_id
        )
    )
    existing_products.add(product_id)

connection.commit()

print("Products inserted.")

# ==========================================
# INSERTING SHIPMODES
# ==========================================

cursor.execute("SELECT ShipMode FROM ShipModes")
existing_ship_modes = {ship_mode for (ship_mode,) in cursor.fetchall()}

ship_modes = df["Ship Mode"].drop_duplicates()

for ship_mode in ship_modes:
    if ship_mode in existing_ship_modes:
        continue

    cursor.execute(
        """
        INSERT INTO ShipModes (ShipMode)
        VALUES (%s)
        """,
        (ship_mode,)
    )
    existing_ship_modes.add(ship_mode)

connection.commit()

print("Ship modes inserted.")

#==========================================
# RETRIEVING ID FOR SHIPMODES
# ==========================================

cursor.execute(
    "SELECT ShipModeID, ShipMode FROM ShipModes"
)

ship_mode_map = {
    name: ship_mode_id
    for ship_mode_id, name in cursor.fetchall()
}

print(ship_mode_map)

# ==========================================
# INSERTING CUSTOMERS
# ==========================================

cursor.execute("SELECT CustomerID FROM Customers")
existing_customers = {customer_id for (customer_id,) in cursor.fetchall()}

customers = (
    df[
        [
            "Customer ID",
            "Customer Name",
            "Segment"
        ]
    ]
    .drop_duplicates()
)

for _, row in customers.iterrows():
    customer_id = row["Customer ID"]
    if customer_id in existing_customers:
        continue

    cursor.execute(
        """
        INSERT INTO Customers
        (
            CustomerID,
            CustomerName,
            Segment
        )
        VALUES (%s, %s, %s)
        """,
        (
            row["Customer ID"],
            row["Customer Name"],
            row["Segment"]
        )
    )
    existing_customers.add(customer_id)

connection.commit()

print("Customers inserted.")

# ==========================================
# INSERTING LOCATIONS
# ==========================================

cursor.execute(
    "SELECT Country, City, State, PostalCode, Region FROM Locations"
)
existing_locations = {(
    country, city, state, postal_code, region
) for country, city, state, postal_code, region in cursor.fetchall()}

locations = (
    df[
        [
            "Country",
            "City",
            "State",
            "Postal Code",
            "Region"
        ]
    ]
    .drop_duplicates()
)

for _, row in locations.iterrows():
    location_key = (
        row["Country"],
        row["City"],
        row["State"],
        row["Postal Code"],
        row["Region"]
    )

    if location_key in existing_locations:
        continue

    cursor.execute(
        """
        INSERT INTO Locations
        (
            Country,
            City,
            State,
            PostalCode,
            Region
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            row["Country"],
            row["City"],
            row["State"],
            row["Postal Code"],
            row["Region"]
        )
    )
    existing_locations.add(location_key)

connection.commit()

print("Locations inserted.")

# ==========================================
# CREATING A LOCATION LOOKUP
# ==========================================
cursor.execute(
    """
    SELECT
        LocationID,
        Country,
        City,
        State,
        PostalCode,
        Region
    FROM Locations
    """
)

location_map = {
    (
        country,
        city,
        state,
        postal_code,
        region
    ): location_id

    for (
        location_id,
        country,
        city,
        state,
        postal_code,
        region
    ) in cursor.fetchall()
}

# ==========================================
# INSERTING ORDERS
# ==========================================

cursor.execute("SELECT OrderID FROM Orders")
existing_orders = {order_id for (order_id,) in cursor.fetchall()}

orders = (
    df[
        [
            "Order ID",
            "Order Date",
            "Ship Date",
            "Customer ID",
            "Ship Mode"
        ]
    ]
    .drop_duplicates(subset=["Order ID"])
)

for _, row in orders.iterrows():
    order_id = row["Order ID"]
    if order_id in existing_orders:
        continue

    ship_mode_id = ship_mode_map[
        row["Ship Mode"]
    ]

    cursor.execute(
        """
        INSERT INTO Orders
        (
            OrderID,
            OrderDate,
            ShipDate,
            CustomerID,
            ShipModeID
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            row["Order ID"],
            row["Order Date"].date(),
            row["Ship Date"].date(),
            row["Customer ID"],
            ship_mode_id
        )
    )
    existing_orders.add(order_id)

connection.commit()

print("Orders inserted.")

# ==========================================
# INSERT ORDER DETAILS
# ==========================================

cursor.execute("SELECT RowID FROM OrderDetails")
existing_order_details = {int(row_id) for (row_id,) in cursor.fetchall()}

for _, row in df.iterrows():
    row_id = int(row["Row ID"])
    if row_id in existing_order_details:
        continue

    location_key = (
        row["Country"],
        row["City"],
        row["State"],
        row["Postal Code"],
        row["Region"]
    )

    location_id = location_map[location_key]

    cursor.execute(
        """
        INSERT INTO OrderDetails
        (
            RowID,
            OrderID,
            ProductID,
            LocationID,
            Sales,
            Quantity,
            Discount,
            Profit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            row_id,
            row["Order ID"],
            row["Product ID"],
            location_id,
            float(row["Sales"]),
            int(row["Quantity"]),
            float(row["Discount"]),
            float(row["Profit"])
        )
    )
    existing_order_details.add(row_id)

connection.commit()

print("Order details inserted.")

# ==========================================
# CLOSE DATABASE CONNECTION
# ==========================================

cursor.close()
connection.close()

print("Database connection closed.")
print("ETL process completed successfully!")