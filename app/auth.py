from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, CurrencyForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirection si déjà connecté
        return redirect(url_for('admin.dashboard') if current_user.is_admin else url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            print(f"Utilisateur {user.username}, is_admin: {user.is_admin}")
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard')) 
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('auth.register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie ! Veuillez compléter votre profil.', 'success')
        login_user(user)   # Connecte automatiquement
        return redirect(url_for('auth.profile'))
    return render_template('auth/register.html', form=form)


from flask_login import login_required, current_user
from app import db

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = CurrencyForm()
    if form.validate_on_submit():
        # Vérifier le mot de passe actuel
        if not current_user.check_password(form.current_password.data):
            flash('Mot de passe actuel incorrect.', 'danger')
            return redirect(url_for('auth.profile'))

        # Mettre à jour les informations
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.currency = form.currency.data

        # Changer le mot de passe si un nouveau est fourni
        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('auth.profile'))

    # Pré-remplir le formulaire avec les données actuelles
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.currency.data = current_user.currency
    return render_template('auth/profile.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))