from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.db_classes import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


# class RegistrationForm(FlaskForm):
#     username = StringField('Přihlašovací jméno', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Heslo', validators=[DataRequired()])
#     confirm_password = PasswordField('Heslo znovu', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Registrovat')

#     def validate_email(self, email):
#         email = User.query.filter_by(email=email.data).first()
#         if email:
#             raise ValidationError('Email je už použit')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit')

# class UpdateaccForm(FlaskForm):
#     username = StringField('Jméno', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     pp = FileField('Profilovka', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
#     submit = SubmitField('Uložit')

#     # def validate_username(self, username):
#     #     if username.data != current_user.username:
#     #         user = User.query.filter_by(username=username.data).first()
#     #         if user:
#     #             raise ValidationError('That username is already taken. Please choose some other.')
#     def validate_email(self, email):
#         if email.data != current_user.email:
#             email = User.query.filter_by(email=email.data).first()
#             if email:
#                 raise ValidationError('Email už je použit')
