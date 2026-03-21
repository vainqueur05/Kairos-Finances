from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def format_currency(amount, currency):
        symbols = {
            'EUR': '€',
            'USD': '$',
            'GBP': '£',
            'CHF': 'CHF',
            'JPY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CNY': '¥',
            'INR': '₹',
            'BRL': 'R$',
            'XOF': 'CFA',
            'RDC': 'FC',
        }
        symbol = symbols.get(currency, currency)
        return f"{amount:.2f} {symbol}"
    app.jinja_env.filters['currency'] = format_currency

    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.transactions import bp as transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp)

    return app