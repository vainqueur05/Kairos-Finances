from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Nom de la catégorie', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Description (optionnelle)', validators=[Length(max=200)])
    submit = SubmitField('Enregistrer')

from wtforms import SelectField, FloatField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class TransactionForm(FlaskForm):
    amount = FloatField('Montant', validators=[DataRequired(), NumberRange(min=0.01, message="Le montant doit être positif.")])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    type = SelectField('Type', choices=[('income', 'Revenu'), ('expense', 'Dépense')], validators=[DataRequired()])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

from wtforms import SelectField
class CurrencyForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[Optional(), Length(min=6)])
    confirm_new_password = PasswordField('Confirmer le nouveau mot de passe', validators=[EqualTo('new_password', message='Les mots de passe ne correspondent pas.')])
    currency = SelectField('Devise', choices=[
        ('EUR', 'Euro (€)'),
        ('USD', 'Dollar ($)'),
        ('GBP', 'Livre sterling (£)'),
        ('CHF', 'Franc suisse (CHF)'),
        ('JPY', 'Yen (¥)'),
        ('CAD', 'Dollar canadien (C$)'),
        ('AUD', 'Dollar australien (A$)'),
        ('CNY', 'Yuan (¥)'),
        ('INR', 'Roupie indienne (₹)'),
        ('BRL', 'Real brésilien (R$)'),
        ('XOF', 'Franc CFA (CFA)'),
        ('FC', 'Franc congolais(FC)'),
    ])
    submit = SubmitField('Enregistrer')