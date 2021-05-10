from flask import Flask, render_template
from flask_session import Session
from src.resources import product, category, authentication
import os

def create_app(environment="development"):
    app = Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY')

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    app.register_blueprint(authentication.auth)
    app.register_blueprint(product.prod)
    app.register_blueprint(category.cat)

    @app.route('/',)
    def home():
        return render_template('home.html')
    return app
