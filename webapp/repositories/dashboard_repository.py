try:
    from ..database import get_db_connection
except ImportError:
    from database import get_db_connection


class DashboardRepository:

    def get_dashboard_kpis(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                SUM(od.Sales) AS total_sales,
                SUM(od.Profit) AS total_profit,
                SUM(od.Quantity) AS total_quantity,
                COUNT(DISTINCT o.OrderID) AS total_orders
            FROM OrderDetails od
            INNER JOIN Orders o
                ON od.OrderID = o.OrderID
        """)

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result

    def get_monthly_sales(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                DATE_FORMAT(o.OrderDate, '%Y-%m') AS month,
                SUM(od.Sales) AS total_sales
            FROM Orders o
            INNER JOIN OrderDetails od
                ON o.OrderID = od.OrderID
            GROUP BY DATE_FORMAT(o.OrderDate, '%Y-%m')
            ORDER BY month
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_sales_by_category(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                c.CategoryName AS category,
                SUM(od.Sales) AS total_sales
            FROM OrderDetails od

            INNER JOIN Products p
                ON od.ProductID = p.ProductID

            INNER JOIN SubCategories sc
                ON p.SubCategoryID = sc.SubCategoryID

            INNER JOIN Categories c
                ON sc.CategoryID = c.CategoryID

            GROUP BY c.CategoryID, c.CategoryName

            ORDER BY total_sales DESC
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_profit_by_category(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                c.CategoryName AS category,
                SUM(od.Profit) AS total_profit
            FROM OrderDetails od

            INNER JOIN Products p
                ON od.ProductID = p.ProductID

            INNER JOIN SubCategories sc
                ON p.SubCategoryID = sc.SubCategoryID

            INNER JOIN Categories c
                ON sc.CategoryID = c.CategoryID

            GROUP BY c.CategoryID, c.CategoryName

            ORDER BY total_profit DESC
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_sales_by_region(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                l.Region AS region,
                SUM(od.Sales) AS total_sales
            FROM OrderDetails od

            INNER JOIN Locations l
                ON od.LocationID = l.LocationID

            GROUP BY l.Region

            ORDER BY total_sales DESC
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_profit_by_region(self):

        connection = get_db_connection()
        
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                l.Region AS region,
                SUM(od.Profit) AS total_profit
            FROM OrderDetails od

            INNER JOIN Locations l
                ON od.LocationID = l.LocationID

            GROUP BY l.Region

            ORDER BY total_profit DESC
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_top_10_products(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.ProductName AS product,
                SUM(od.Sales) AS total_sales
            FROM OrderDetails od

            INNER JOIN Products p
                ON od.ProductID = p.ProductID

            GROUP BY p.ProductID, p.ProductName

            ORDER BY total_sales DESC

            LIMIT 10
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results

    def get_discount_vs_profit(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                Discount,
                AVG(Profit) AS avg_profit,
                COUNT(*) AS transaction_count
            FROM OrderDetails

            GROUP BY Discount

            ORDER BY Discount
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results