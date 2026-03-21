from flask import Blueprint

# Création des blueprints
auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
transactions_bp = Blueprint('transactions', __name__)

# On pourra importer les routes plus tard
from . import auth, main, transactions