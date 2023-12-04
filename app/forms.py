from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, IntegerField, ValidationError
from wtforms.validators import DataRequired, NumberRange
# from app.db_classes import User
# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit')

class FilmForm(FlaskForm):
    name = StringField('Název filmu', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    from_ = TimeField('Od', validators=[DataRequired()])
    to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = StringField('Třída', validators=[DataRequired()])
    submit = SubmitField('Přidat film')

    # PRIDAT overeni jestli uz film neexistuje
    # def validate_name(self, name):
    #     if name 