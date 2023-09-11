from flask import Flask
from app.routes import routes


def start():
    # Initialize the Flask app
    app = Flask(__name__)

    # Register routes
    routes.register_routes(app)

    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
