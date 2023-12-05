from app.db_classes import User
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from app.forms import LoginForm, FilmForm
from app import app, db, bcrypt
from app.json_db import load_db as load_json_db, get_new_film_id, commit_db as commit_json_db
from flask_login import login_required, login_user, logout_user, current_user

try:
    json_db = load_json_db()
except Exception as e:
    print(e)
    quit()
films_by_id = {d['id']: d for d in json_db["films"]}

#region routs
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

@app.route('/program/all')
def program_all():
    return render_template('program_all.html', db=json_db)
@app.route('/film/<id>')
def film(id):
    if not id.isdigit(): return '404'
    id = int(id)
    return render_template('film.html', film=films_by_id[id])

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
#endregion routs


#region login
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
#endregion login

#region admin
@app.route('/reload_db')
@login_required
def reload_db():
    if not current_user.admin:
        return '403'
    global json_db
    json_db = load_json_db()
    global films_by_id
    films_by_id = {d['id']: d for d in json_db["films"]}
    return redirect(url_for('uvod'))

@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    if not current_user.admin:
        return '403'
    form = FilmForm()
    if form.validate_on_submit():
        film = {}
        film["id"] = get_new_film_id(db=json_db)
        film["name"] = form.name.data
        film["link"] = form.link.data
        film["from"] = form.from_.data.strftime('%H:%M')
        film["to"] = form.to.data.strftime('%H:%M')
        film["day"] = form.day.data
        film["room"] = form.room.data
        json_db["films"].append(film)
        commit_json_db(json_db)
        reload_db()
    return render_template('add_film.html', form=form)
#endregion admin

