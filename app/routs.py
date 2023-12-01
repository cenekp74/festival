from app.db_classes import User
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from app.forms import LoginForm# , UpdateaccForm, RegistrationForm
from app import app, db, bcrypt
from app.json_db import load_db as load_json_db
from flask_login import login_required, login_user, logout_user, current_user

try:
    json_db = load_json_db()
except Exception as e:
    print(e)
    json_db = {}

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('uvod'))

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/img', 'favicon.ico')

@app.route('/uvod')
def uvod():
    return render_template('uvod.html')

@app.route('/program')
def program():
    return render_template('program.html')

@app.route('/hoste')
def hoste():
    return render_template('hoste.html')

@app.route('/workshopy')
def workshopy():
    return render_template('workshopy.html')

@app.route('/historie')
def historie():
    return render_template('historie.html')

@app.route('/tym')
def tym():
    return render_template('tym.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte email a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reload_db')
@login_required
def reload_db():
    if not current_user.admin:
        return '403'
    json_db = load_json_db()
    return redirect(url_for('uvod'))
