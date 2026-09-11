try:
    from ..repositories.product_repository import ProductRepository
except ImportError:
    from repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()


    def get_all_products(self):
        return self.repository.get_all()


    def get_product(self, product_id):
        return self.repository.get_by_id(product_id)


    def get_subcategories(self):
        return self.repository.get_subcategories()


    def create_product(
        self,
        product_id,
        product_name,
        subcategory_id
    ):

        product_id = product_id.strip()
        product_name = product_name.strip()

        if not product_id:
            raise ValueError("Product ID is required.")

        if not product_name:
            raise ValueError("Product name is required.")

        if not subcategory_id:
            raise ValueError("Subcategory is required.")

        existing_product = (
            self.repository.get_by_id(product_id)
        )

        if existing_product:
            raise ValueError(
                "A product with this Product ID already exists."
            )

        return self.repository.create(
            product_id,
            product_name,
            subcategory_id
        )


    def update_product(
        self,
        product_id,
        product_name,
        subcategory_id
    ):

        product_name = product_name.strip()

        if not product_name:
            raise ValueError("Product name is required.")

        if not subcategory_id:
            raise ValueError("Subcategory is required.")

        existing_product = (
            self.repository.get_by_id(product_id)
        )

        if existing_product is None:
            raise ValueError("Product not found.")

        return self.repository.update(
            product_id,
            product_name,
            subcategory_id
        )


    def delete_product(self, product_id):

        existing_product = (
            self.repository.get_by_id(product_id)
        )

        if existing_product is None:
            raise ValueError("Product not found.")

        if self.repository.is_product_used(product_id):
            raise ValueError(
                "This product cannot be deleted because "
                "it is already used in existing order records."
            )

        return self.repository.delete(product_id)