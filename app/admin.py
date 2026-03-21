from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import User
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

from app.models import User, Transaction, Category
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users_count = User.query.count()
    transactions_count = Transaction.query.count()
    categories_count = Category.query.count()
    today = datetime.now().date()
    visitors_today = 0  # À implémenter avec un compteur de visites (optionnel)
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                           users_count=users_count,
                           transactions_count=transactions_count,
                           categories_count=categories_count,
                           visitors_today=visitors_today,
                           recent_users=recent_users)


@bp.route('/users')
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/user/<int:user_id>/reset-password', methods=['GET', 'POST'])
@login_required
@admin_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
            db.session.commit()
            flash(f"Mot de passe de {user.username} réinitialisé avec succès.", "success")
            return redirect(url_for('admin.list_users'))
        else:
            flash("Veuillez fournir un nouveau mot de passe.", "danger")
    return render_template('admin/reset_password.html', user=user)

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Empêcher l'admin de se supprimer lui-même
    if user.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "danger")
        return redirect(url_for('admin.list_users'))
    db.session.delete(user)
    db.session.commit()
    flash(f"Utilisateur {user.username} supprimé.", "success")
    return redirect(url_for('admin.list_users'))