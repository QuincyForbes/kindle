from flask import Flask
from app.routes import routes


def Start():
    # Initialize the Flask app
    app = Flask(__name__)

    # Register routes
    routes.register_routes(app)

    # For debugging locally
    # app.run(debug=True, host='0.0.0.0',port=5000)

    # For production
    app.run(host="0.0.0.0", port=5000)
