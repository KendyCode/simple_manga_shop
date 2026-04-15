from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import Author

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
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class AuthorForm(FlaskForm):
    name = StringField('Nom de l\'auteur', validators=[DataRequired()])
    bio = TextAreaField('Biographie')
    submit = SubmitField('Enregistrer l\'auteur')

class MangaForm(FlaskForm):
    title = StringField('Titre du Manga', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Prix (€)', validators=[DataRequired()])
    stock = IntegerField('Stock disponible', validators=[DataRequired()])
    cover_url = StringField('URL de la pochette/couverture')
    # Le champ magique :
    author = QuerySelectField(
        'Auteur',
        query_factory=lambda: Author.query.all(),
        allow_blank=True,
        blank_text='--- Aucun auteur ---',
        get_label='name'
    )
    submit = SubmitField('Enregistrer le Manga')
