from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash
)

try:
    from ..services.product_service import ProductService
except ImportError:
    from services.product_service import ProductService


# =========================================================
# BLUEPRINTS
# =========================================================

product_api_bp = Blueprint(
    "product_api",
    __name__,
    url_prefix="/api/products"
)

product_bp = Blueprint(
    "products",
    __name__
)


product_service = ProductService()


# =========================================================
# API ROUTES
# =========================================================

@product_api_bp.route("/", methods=["GET"])
def get_products():

    products = product_service.get_all_products()

    return jsonify(products)


@product_api_bp.route("/<product_id>", methods=["GET"])
def get_product(product_id):

    product = product_service.get_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


@product_api_bp.route("/", methods=["POST"])
def create_product():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    product_id = data.get("ProductID")
    product_name = data.get("ProductName")
    subcategory_id = data.get("SubCategoryID")

    if not product_id or not product_name or not subcategory_id:
        return jsonify({
            "error":
            "ProductID, ProductName and SubCategoryID are required"
        }), 400

    try:

        product_service.create_product(
            product_id,
            product_name,
            subcategory_id
        )

        return jsonify({
            "message": "Product created successfully"
        }), 201

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 409


@product_api_bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):

    try:

        product_service.delete_product(product_id)

        return jsonify({
            "message": "Product deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404


@product_api_bp.route("/<product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    product_name = data.get("ProductName")
    subcategory_id = data.get("SubCategoryID")

    if not product_name or not subcategory_id:
        return jsonify({
            "error":
            "ProductName and SubCategoryID are required"
        }), 400

    try:

        product_service.update_product(
            product_id,
            product_name,
            subcategory_id
        )

        return jsonify({
            "message": "Product updated successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404


# =========================================================
# GUI ROUTES
# =========================================================

@product_bp.route("/products")
def products_page():

    products = product_service.get_all_products()

    return render_template(
        "products.html",
        products=products
    )


@product_bp.route(
    "/products/add",
    methods=["GET", "POST"]
)
def create_product_page():

    subcategories = (
        product_service.get_subcategories()
    )

    if request.method == "POST":

        product_id = request.form.get(
            "product_id",
            ""
        )

        product_name = request.form.get(
            "product_name",
            ""
        )

        subcategory_id = request.form.get(
            "subcategory_id"
        )

        try:

            product_service.create_product(
                product_id,
                product_name,
                subcategory_id
            )

            flash(
                "Product created successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "products.products_page"
                )
            )

        except ValueError as error:

            flash(
                str(error),
                "error"
            )

    return render_template(
        "product_form.html",
        mode="add",
        product=None,
        subcategories=subcategories
    )


@product_bp.route(
    "/products/edit/<product_id>",
    methods=["GET", "POST"]
)
def edit_product_page(product_id):

    product = (
        product_service.get_product(
            product_id
        )
    )

    if product is None:

        flash(
            "Product not found.",
            "error"
        )

        return redirect(
            url_for(
                "products.products_page"
            )
        )

    subcategories = (
        product_service.get_subcategories()
    )

    if request.method == "POST":

        product_name = request.form.get(
            "product_name",
            ""
        )

        subcategory_id = request.form.get(
            "subcategory_id"
        )

        try:

            product_service.update_product(
                product_id,
                product_name,
                subcategory_id
            )

            flash(
                "Product updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "products.products_page"
                )
            )

        except ValueError as error:

            flash(
                str(error),
                "error"
            )

    return render_template(
        "product_form.html",
        mode="edit",
        product=product,
        subcategories=subcategories
    )


@product_bp.route(
    "/products/delete/<product_id>",
    methods=["POST"]
)
def delete_product_page(product_id):

    try:

        product_service.delete_product(
            product_id
        )

        flash(
            "Product deleted successfully.",
            "success"
        )

    except ValueError as error:

        flash(
            str(error),
            "error"
        )

    return redirect(
        url_for(
            "products.products_page"
        )
    )