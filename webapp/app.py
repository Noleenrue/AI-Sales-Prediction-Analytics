from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from .routes.product_routes import (
    product_bp,
    product_api_bp
    )
    from .routes.home_routes import home_bp
    from .routes.prediction_routes import prediction_bp
except ImportError:
    from routes.product_routes import (
        product_bp,
        product_api_bp
    )
    from routes.home_routes import home_bp
    from routes.prediction_routes import prediction_bp


def create_app():

    app = Flask(__name__)

    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    if not app.secret_key:
        raise RuntimeError(
            "FLASK_SECRET_KEY is not configured."
        )

    try:
        app.config.from_object(
            "webapp.config.Config"
        )
    except ImportError:
        app.config.from_object(
            "config.Config"
        )

    app.register_blueprint(home_bp)
    app.register_blueprint(product_api_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(prediction_bp)

    return app


app = create_app()


# Show registered Flask routes
print("\nREGISTERED ROUTES")
print("----------------------------")
print(app.url_map)


if __name__ == "__main__":
    app.run(debug=True)