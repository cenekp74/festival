from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, IntegerField, ValidationError, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
# from app.db_classes import User
# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed

VALID_LANGUAGE_VALUES = ['cz', 'en', 'cz tit']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit')

class FilmForm(FlaskForm):
    name = StringField('Název filmu', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = StringField('Třída', validators=[DataRequired()])
    language = SelectField('Jazyk', choices=VALID_LANGUAGE_VALUES, validators=[DataRequired()])
    submit = SubmitField('Potvrdit')

    # PRIDAT overeni jestli uz film neexistuje
    # def validate_name(self, name):
    #     if name 

class WorkshopForm(FlaskForm):
    name = StringField('Název workshopu', validators=[DataRequired()])
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = StringField('Třída', validators=[DataRequired()])
    picture = FileField('Obrázek', validators=[FileAllowed(['jpg', 'png'])])
    author = StringField('Autor', validators=[DataRequired()])
    description = TextAreaField('Popis')
    submit = SubmitField('Potvrdit')

class BesedaForm(FlaskForm):
    name = StringField('Název besedy', validators=[DataRequired()])
    beseda_type = SelectField('Typ besedy', choices=[('f', 'k filmu'), ('h', 's hostem')], validators=[DataRequired()])
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = StringField('Třída', validators=[DataRequired()])
    submit = SubmitField('Potvrdit')

class HostForm(FlaskForm):
    name = StringField('Jméno hosta', validators=[DataRequired()])
    description = TextAreaField('Popis')
    picture = FileField('Obrázek', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Potvrdit')