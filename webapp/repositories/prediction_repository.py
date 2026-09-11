try:
    from ..database import get_db_connection
except ImportError:
    from database import get_db_connection


def get_products_for_prediction():

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        p.ProductName AS Product,
        c.CategoryName AS Category,
        sc.SubCategoryName AS SubCategory
    FROM Products p
    INNER JOIN SubCategories sc
        ON p.SubCategoryID = sc.SubCategoryID
    INNER JOIN Categories c
        ON sc.CategoryID = c.CategoryID
    ORDER BY p.ProductName
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products

def save_prediction_history(data):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO PredictionHistory (
        Product,
        Category,
        SubCategory,
        Segment,
        Region,
        ShipMode,
        Quantity,
        Discount,
        OrderDate,
        ShipDate,
        PredictedSales
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    """

    values = (
        data["Product"],
        data["Category"],
        data["SubCategory"],
        data["Segment"],
        data["Region"],
        data["ShipMode"],
        data["Quantity"],
        data["Discount"],
        data["OrderDate"],
        data["ShipDate"],
        data["PredictedSales"]
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return True

def get_prediction_history():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        PredictionID,
        Product,
        Category,
        SubCategory,
        Segment,
        Region,
        ShipMode,
        Quantity,
        Discount,
        OrderDate,
        ShipDate,
        PredictedSales,
        CreatedAt
    FROM PredictionHistory
    ORDER BY PredictionID DESC
    """

    cursor.execute(query)

    history = cursor.fetchall()

    cursor.close()
    connection.close()

    return history