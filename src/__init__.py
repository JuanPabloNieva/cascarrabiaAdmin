from flask import Flask, render_template
from flask_session import Session
from src.resources import product, category, authentication, pay
from src.helpers import handlers
from flask_cors import CORS
import os

def create_app(environment="development"):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.secret_key = os.environ.get('SECRET_KEY')

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    app.register_blueprint(authentication.auth)
    app.register_blueprint(product.prod)
    app.register_blueprint(category.cat)
    app.register_blueprint(pay.pay)

    @app.route('/',)
    def home():
        return render_template('home.html')

    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(401, handlers.unauthorized_error)
    app.register_error_handler(405, handlers.method_not_allowed)
    app.register_error_handler(500, handlers.internal_server_error)
    return app
