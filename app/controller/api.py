from flask import Flask
from app.routes import routes


def Start():
    app = Flask(__name__)

    routes.register_routes(app)

    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
