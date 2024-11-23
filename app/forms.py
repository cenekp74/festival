from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange
from app.db_classes import Host
from app import app

VALID_LANGUAGE_VALUES = ['cz', 'en', 'en + cz tit', 'en + sk tit', 'sk + cz tit','de + cz tit', 'cz + en tit', 'de + en tit', 'fr + cz tit']

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember = BooleanField('Pamatuj si mě')
    submit = SubmitField('Přihlásit')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Heslo')
    admin = BooleanField('admin')
    perm_shop = BooleanField('perm_shop')
    perm_program_edit = BooleanField('perm_program_edit')
    submit = SubmitField('Potvrdit')

    def __init__(self, require_password=True, *args, **kwargs): # tohle je kvuli tomu, ze pri editovani usera nechci aby byl password field required
        super(UserForm, self).__init__(*args, **kwargs)
        
        if require_password:
            self.password.validators.append(DataRequired())

class FilmForm(FlaskForm):
    name = StringField('Název filmu', validators=[DataRequired()])
    link = StringField('Odkaz', validators=[DataRequired()])
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = SelectField('Místnost', choices=app.config['ROOMS'], validators=[DataRequired()])
    picture = FileField('Obrázek', validators=[FileAllowed(['jpg', 'png'])])
    language = SelectField('Jazyk', choices=VALID_LANGUAGE_VALUES, validators=[DataRequired()])
    description = TextAreaField('Popis')
    short_description = StringField('Krátký popis', render_kw={"list": "short-description-suggestions"})
    filename = StringField('Filename', render_kw={"placeholder": "filename souboru filmu na serveru (pokud nevis nech prazdny)"})
    vg = BooleanField('Jen pro vyšší gymnázium')
    recommended = BooleanField('Doporučeno')
    submit = SubmitField('Potvrdit')

class WorkshopForm(FlaskForm):
    name = StringField('Název workshopu', validators=[DataRequired()])
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = SelectField('Místnost', choices=app.config['ROOMS'], validators=[DataRequired()])
    picture = FileField('Obrázek', validators=[FileAllowed(['jpg', 'png'])])
    author = StringField('Autor', validators=[DataRequired()])
    description = TextAreaField('Popis')
    vg = BooleanField('Jen pro vyšší gymnázium')
    recommended = BooleanField('Doporučeno')
    submit = SubmitField('Potvrdit')

class BesedaForm(FlaskForm):
    name = StringField('Název besedy', validators=[DataRequired()])
    host = QuerySelectField('Host', query_factory=lambda: Host.query.all(), get_label=lambda host:host.name, allow_blank=True, blank_text='---')
    time_from = TimeField('Od', validators=[DataRequired()])
    time_to = TimeField('Do', validators=[DataRequired()])
    day = IntegerField('Den', validators=[DataRequired(), NumberRange(min=1, max=3)])
    room = SelectField('Místnost', choices=app.config['ROOMS'], validators=[DataRequired()])
    vg = BooleanField('Jen pro vyšší gymnázium')
    recommended = BooleanField('Doporučeno')
    submit = SubmitField('Potvrdit')

class HostForm(FlaskForm):
    name = StringField('Jméno hosta', validators=[DataRequired()])
    description = TextAreaField('Popis')
    short_description = StringField('Krátký popis')
    picture = FileField('Obrázek', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Potvrdit')

class ShopForm(FlaskForm):
    name = StringField('Název položky', validators=[DataRequired()])
    item_type = SelectField('Typ', choices=[('kavarna', 'Kavárna'), ('cajovna', 'Čajovna')])
    price = IntegerField('Cena', validators=[DataRequired(), NumberRange(min=1, max=9999)])
    submit = SubmitField('Potvrdit')