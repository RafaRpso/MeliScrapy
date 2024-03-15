# run.py
from flask import Flask
from app.routes.routes import api_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])
app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
