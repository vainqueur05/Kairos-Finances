from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Category
from app.forms import CategoryForm
from flask import Blueprint
from app.forms import TransactionForm
from app.models import Transaction, Category
from datetime import datetime

bp = Blueprint('transactions', __name__)

@bp.route('/transactions')
@login_required
def list_transactions():
    """Affiche la liste des transactions de l'utilisateur connecté."""
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions/list.html', transactions=transactions)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    # Remplir le champ category_id avec les catégories de l'utilisateur
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            date=form.date.data,
            type=form.type.data,
            user_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction ajoutée avec succès.', 'success')
        return redirect(url_for('transactions.list_transactions'))
    return render_template('transactions/form.html', form=form, title='Ajouter une transaction')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    # Vérifier que la transaction appartient à l'utilisateur
    if transaction.user_id != current_user.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('transactions.list_transactions'))
    form = TransactionForm(obj=transaction)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.date = form.date.data
        transaction.type = form.type.data
        transaction.category_id = form.category_id.data
        db.session.commit()
        flash('Transaction modifiée avec succès.', 'success')
        return redirect(url_for('transactions.list_transactions'))
    return render_template('transactions/form.html', form=form, title='Modifier une transaction')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('transactions.list_transactions'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction supprimée avec succès.', 'success')
    return redirect(url_for('transactions.list_transactions'))

@bp.route('/categories')
@login_required
def list_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions/categories.html', categories=categories)

@bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        existing = Category.query.filter_by(user_id=current_user.id, name=form.name.data).first()
        if existing:
            flash('Vous avez déjà une catégorie avec ce nom.', 'danger')
            return redirect(url_for('transactions.add_category'))
        category = Category(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Catégorie ajoutée avec succès.', 'success')
        return redirect(url_for('transactions.list_categories'))
    return render_template('transactions/category_form.html', form=form, title='Ajouter une catégorie')

@bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('transactions.list_categories'))
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        if form.name.data != category.name:
            existing = Category.query.filter_by(user_id=current_user.id, name=form.name.data).first()
            if existing:
                flash('Vous avez déjà une catégorie avec ce nom.', 'danger')
                return redirect(url_for('transactions.edit_category', id=id))
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Catégorie modifiée avec succès.', 'success')
        return redirect(url_for('transactions.list_categories'))
    return render_template('transactions/category_form.html', form=form, title='Modifier une catégorie')

@bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('transactions.list_categories'))
    db.session.delete(category)
    db.session.commit()
    flash('Catégorie supprimée avec succès.', 'success')
    return redirect(url_for('transactions.list_categories'))