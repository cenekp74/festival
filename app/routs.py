from app.db_classes import Host, User, Film, Beseda, Workshop
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from app.forms import LoginForm, FilmForm, WorkshopForm, BesedaForm, HostForm
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.utils import allowed_file, correct_uid, update_rooms
from app.decorators import admin_required
import datetime
import os
from werkzeug.utils import secure_filename

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
    return render_template('program_all.html', films=Film.query.all(), besedy=Beseda.query.all(), workshops=Workshop.query.all(), hosts=Host.query.all())

@app.route('/program/day/<dayn>')
def program_day(dayn):
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)
    update_rooms() # tohle je tu proto, protoze kdyz server bezi s vic workerama tak se updatne vzdycky jenom u jednoho app.rooms a jsou s tim pak problemy. neni to idealni reseni, ale nevim jak jinak to udelat. stejne je to v interaktivnim editovani a ve favorites
    program = {}
    for room in app.rooms[dayn]:
        program[room] = {}
        program[room]["films"] = sorted(Film.query.filter_by(day=dayn, room=room).all(), key=lambda film:film.time_from)
        program[room]["besedy"] = sorted(Beseda.query.filter_by(day=dayn, room=room).all(), key=lambda beseda:beseda.time_from)
        program[room]["workshops"] = sorted(Workshop.query.filter_by(day=dayn, room=room).all(), key=lambda workshop:workshop.time_from)
    return render_template('program_day.html', program=program, rooms=app.rooms[dayn], day=dayn)

@app.route('/film/<id>')
def film(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    return render_template('program_items/film.html', film=Film.query.get(id))

@app.route('/hoste')
def hoste():
    return render_template('hoste.html', items=Host.query.all())

@app.route('/workshopy')
def workshopy():
    return render_template('workshopy.html', items=Workshop.query.all())

@app.route('/historie')
def historie():
    return render_template('historie.html')

@app.route('/tym')
def tym():
    return render_template('tym.html')
#endregion routs

#region favorite
@app.route('/favorite/add/<uid>')
def add_favorite(uid):
    if not correct_uid(uid, h_allowed=False): abort(500)
    favorite_cookie = request.cookies.get("favorite")
    if not favorite_cookie: favorite_cookie = ''
    if uid in favorite_cookie:
        return redirect(url_for('favorite'))
    favorite_cookie += uid + ' '
    resp = make_response('200')
    resp.set_cookie('favorite', favorite_cookie)
    return resp

@app.route('/favorite/clear')
def clear_favorite():
    resp = make_response(redirect(url_for('favorite')))
    resp.set_cookie('favorite', '')
    return resp

@app.route('/favorite/remove/<uid>')
def remove_favorite(uid):
    if not correct_uid(uid, h_allowed=False): abort(500)
    favorite_cookie = request.cookies.get("favorite")
    if not favorite_cookie: favorite_cookie = ''
    if uid not in favorite_cookie:
        return redirect(url_for('favorite'))
    favorite_cookie = favorite_cookie.replace(uid+' ', '')
    favorite_cookie = favorite_cookie.replace(uid, '')
    resp = make_response('200')
    resp.set_cookie('favorite', favorite_cookie)
    return resp

@app.route('/favorite/toggle/<uid>')
def toggle_favorite(uid):
    if not correct_uid(uid, h_allowed=False): abort(500)
    favorite_cookie = request.cookies.get("favorite")
    if not favorite_cookie: favorite_cookie = ''
    if uid not in favorite_cookie:
        favorite_cookie += uid + ' '
    else:
        favorite_cookie = favorite_cookie.replace(uid+' ', '')
        favorite_cookie = favorite_cookie.replace(uid, '')
    resp = make_response('200')
    resp.set_cookie('favorite', favorite_cookie)
    return resp

@app.route('/favorite/<dayn>')
@app.route('/program/favorite/<dayn>')
@app.route('/program/my/<dayn>')
def favorite_day(dayn):
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)
    update_rooms() # tohle je tu proto, protoze kdyz server bezi s vic workerama tak se updatne vzdycky jenom u jednoho app.rooms a jsou s tim pak problemy
    favorite_cookie = request.cookies.get("favorite")
    if not favorite_cookie: favorite_cookie = ''
    films = []
    besedy = []
    workshops = []
    for uid in favorite_cookie.split(' '):
        if not correct_uid(uid, h_allowed=False): continue
        item_type, item_id = uid.split('_')
        if item_type == 'f': films.append(int(item_id))
        elif item_type == 'b': besedy.append(int(item_id))
        elif item_type == 'w': workshops.append(int(item_id))
    rooms_ = app.rooms[dayn].copy()
    program = {}
    for room in app.rooms[dayn]:
        program[room] = {}
        program[room]["films"] = [item for item in sorted(Film.query.filter_by(day=dayn, room=room).all(), key=lambda film:film.time_from) if item.id in films]
        program[room]["besedy"] = [item for item in sorted(Beseda.query.filter_by(day=dayn, room=room).all(), key=lambda beseda:beseda.time_from) if item.id in besedy]
        program[room]["workshops"] = [item for item in sorted(Workshop.query.filter_by(day=dayn, room=room).all(), key=lambda workshop:workshop.time_from) if item.id in workshops]
        if not program[room]["films"] and not program[room]["besedy"] and not program[room]["workshops"]:
            rooms_.remove(room)
    return render_template('favorite_day.html', program=program, rooms=rooms_, day=dayn)

@app.route('/favorite')
def favorite():
    return render_template('favorite.html')

#endregion favorite

#region search

@app.route('/search/query')
def search_query():
    q = request.args.get('q')
    
    results = []
    if q:
        if len(q) > 1:
            results.extend(Film.query.filter(Film.name.icontains(q)))

            results.extend(Beseda.query.filter(Beseda.name.icontains(q)))

            results.extend(Workshop.query.filter(Workshop.description.icontains(q)))
            results.extend(Workshop.query.filter(Workshop.author.icontains(q)))
            results.extend(Workshop.query.filter(Workshop.name.icontains(q)))

            results.sort(key=lambda item:item.day)
            results.sort(key=lambda item:item.time_from)

            results.extend(Host.query.filter(Host.name.icontains(q)))
            for item in results:
                item.name = item.name.replace(q, f'<mark>{q}</mark>')
                if isinstance(item, Film):
                    item.type = 'film'
                elif isinstance(item, Beseda):
                    item.type = 'beseda'
                elif isinstance(item, Workshop):
                    item.author = item.author.replace(q, f'<mark>{q}</mark>')
                    item.description = item.description.replace(q, f'<mark>{q}</mark>')
                    item.type = 'workshop'
                elif isinstance(item, Host):
                    item.type = 'host'
    return render_template('search_result.html', results=results, q=q)

@app.route('/search')
def search():
    return render_template('search.html')

#endregion search

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
@app.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_file():
    if not current_user.admin:
        abort(403)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
    files = list(os.listdir('app/static/upload/'))

    return render_template('upload.html', files=files)

@app.route('/colors') # testovani barvicek
@login_required
def colors():
    return render_template('colors.html')

#endregion admin

