from app.db_classes import User, Film
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from app.forms import LoginForm, FilmForm
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.utils import get_rooms
import datetime

rooms = None

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
    return render_template('program_all.html', films=Film.query.all())

@app.route('/program/day/<dayn>')
def program_day(dayn):
    if not dayn.isdigit(): return '500'
    dayn = int(dayn)
    if dayn not in [1,2,3]: return '404'
    global rooms
    if rooms is None:
        rooms = get_rooms()
    program = {}
    for room in rooms:
        program[room] = sorted(Film.query.filter_by(day=dayn, room=room).all(), key=lambda film:film.time_from)
    return render_template('program_day.html', program=program, rooms=rooms)

@app.route('/film/<id>')
def film(id):
    if not id.isdigit(): return '500'
    id = int(id)
    return render_template('film.html', film=Film.query.get(id))

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
@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    if not current_user.admin:
        return '403'
    form = FilmForm()
    if form.validate_on_submit():
        film = Film(name=form.name.data,
                    link=form.link.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    day = form.day.data,
                    room = form.room.data
                    )
        db.session.add(film)
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('add_film.html', form=form)

@app.route('/program/edit')
@login_required
def edit_program():
    if not current_user.admin:
        return '403'
    return render_template('edit_program.html', films=Film.query.all())

@app.route('/edit_film/<id>', methods=['GET', 'POST'])
@login_required
def edit_film(id):
    if not current_user.admin:
        return '403'
    if not id.isdigit(): return '500'
    id = int(id)
    film = Film.query.get(id)
    form = FilmForm(name=film.name, 
                    link=film.link, time_from=datetime.datetime.strptime(film.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(film.time_to, '%H:%M').time(), day=film.day, room=film.room)
    if form.validate_on_submit():
        film.name = form.name.data
        film.link = form.link.data
        film.time_from = form.time_from.data.strftime('%H:%M')
        film.time_to = form.time_to.data.strftime('%H:%M')
        film.day = form.day.data
        film.room = form.room.data
        db.session.commit()
        return redirect(url_for('edit_program'))
    return render_template('edit_film.html', film=film, form=form)

@app.route('/delete_film/<id>')
@login_required
def delete_film(id):
    if not current_user.admin:
        return '403'
    if not id.isdigit(): return '500'
    id = int(id)
    Film.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('edit_program'))

#endregion admin

