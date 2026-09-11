try:
    from ..database import get_db_connection
except ImportError:
    from database import get_db_connection


class ProductRepository:

    def get_all(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.ProductID,
                p.ProductName,
                p.SubCategoryID,
                sc.SubCategoryName
            FROM Products p
            INNER JOIN SubCategories sc
                ON p.SubCategoryID = sc.SubCategoryID
            ORDER BY p.ProductName
        """)

        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return products

    def get_by_id(self, product_id):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                ProductID,
                ProductName,
                SubCategoryID
            FROM Products
            WHERE ProductID = %s
        """, (product_id,))

        product = cursor.fetchone()

        cursor.close()
        connection.close()

        return product

    def create(self, product_id, product_name, subcategory_id):

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Products
            (
                ProductID,
                ProductName,
                SubCategoryID
            )
            VALUES (%s, %s, %s)
        """, (
            product_id,
            product_name,
            subcategory_id
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return True

    def delete(self, product_id):

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM Products
            WHERE ProductID = %s
        """, (product_id,))

        connection.commit()

        rows_deleted = cursor.rowcount

        cursor.close()
        connection.close()

        return rows_deleted

    def update(self, product_id, product_name, subcategory_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Products
            SET
                ProductName = %s,
                SubCategoryID = %s
            WHERE ProductID = %s
        """, (
            product_name,
            subcategory_id,
            product_id
        ))

        connection.commit()

        rows_updated = cursor.rowcount

        cursor.close()
        connection.close()

        return rows_updated

    def get_subcategories(self):

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                SubCategoryID,
                SubCategoryName
            FROM SubCategories
            ORDER BY SubCategoryName
        """)

        subcategories = cursor.fetchall()

        cursor.close()
        connection.close()

        return subcategories

    def is_product_used(self, product_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM OrderDetails
            WHERE ProductID = %s
        """, (product_id,))

        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count > 0