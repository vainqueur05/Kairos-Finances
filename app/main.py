from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Transaction, Category
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Toutes les transactions de l'utilisateur
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    # Solde total
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    # Mois en cours
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1)
    if now.month == 12:
        last_day = datetime(now.year+1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(now.year, now.month+1, 1) - timedelta(days=1)

    month_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= first_day,
        Transaction.date <= last_day
    ).all()
    month_income = sum(t.amount for t in month_transactions if t.type == 'income')
    month_expense = sum(t.amount for t in month_transactions if t.type == 'expense')
    month_balance = month_income - month_expense

    # Répartition par catégorie (dépenses)
    categories = Category.query.filter_by(user_id=current_user.id).all()
    cat_expenses = []
    cat_labels = []
    for cat in categories:
        total = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == cat.id,
            Transaction.type == 'expense'
        ).scalar() or 0
        if total > 0:
            cat_expenses.append(total)
            cat_labels.append(cat.name)

    # Évolution mensuelle (12 derniers mois)
    months = []
    income_data = []
    expense_data = []
    for i in range(11, -1, -1):
        date = now - timedelta(days=30*i)
        month_start = datetime(date.year, date.month, 1)
        if date.month == 12:
            month_end = datetime(date.year+1, 1, 1) - timedelta(days=1)
        else:
            month_end = datetime(date.year, date.month+1, 1) - timedelta(days=1)
        month_trans = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= month_start,
            Transaction.date <= month_end
        ).all()
        month_inc = sum(t.amount for t in month_trans if t.type == 'income')
        month_exp = sum(t.amount for t in month_trans if t.type == 'expense')
        months.append(month_start.strftime('%b %Y'))
        income_data.append(month_inc)
        expense_data.append(month_exp)

    # 5 dernières transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
                                   .order_by(Transaction.date.desc()).limit(5).all()

    return render_template('dashboard.html',
                           balance=balance,
                           month_income=month_income,
                           month_expense=month_expense,
                           month_balance=month_balance,
                           cat_labels=cat_labels,
                           cat_expenses=cat_expenses,
                           months=months,
                           income_data=income_data,
                           expense_data=expense_data,
                           recent_transactions=recent_transactions)  # ← variable ajoutée