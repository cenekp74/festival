from app.db_classes import Host, User, Film, Beseda, Workshop
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, session
from app.forms import LoginForm, FilmForm, WorkshopForm, BesedaForm, HostForm
from app import app, db, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.utils import get_rooms, allowed_file, correct_uid, get_object_by_uid
import datetime
import os
from werkzeug.utils import secure_filename
from PIL import Image
import json
import random

rooms = None

albums_dict = json.load(open('app/static/fotogalerie/albums.json', 'r'))

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
    global rooms
    if rooms is None:
        rooms = get_rooms()
    program = {}
    for room in rooms[dayn]:
        program[room] = {}
        program[room]["films"] = sorted(Film.query.filter_by(day=dayn, room=room).all(), key=lambda film:film.time_from)
        program[room]["besedy"] = sorted(Beseda.query.filter_by(day=dayn, room=room).all(), key=lambda beseda:beseda.time_from)
        program[room]["workshops"] = sorted(Workshop.query.filter_by(day=dayn, room=room).all(), key=lambda workshop:workshop.time_from)
    return render_template('program_day.html', program=program, rooms=rooms[dayn], day=dayn)

@app.route('/film/<id>')
def film(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    return render_template('program_items/film.html', film=Film.query.get(id))

@app.route('/workshop/<id>')
def workshop(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    return render_template('program_items/workshop.html', workshop=Workshop.query.get(id))

@app.route('/beseda/<id>')
def beseda(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    return render_template('program_items/beseda.html', beseda=Beseda.query.get(id))

@app.route('/host/<id>')
def host(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    return render_template('program_items/host.html', host=Host.query.get(id))

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
    global rooms
    if rooms is None:
        rooms = get_rooms()
    rooms_ = rooms[dayn].copy()
    program = {}
    for room in rooms[dayn]:
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
@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    if not current_user.admin:
        abort(403)
    form = FilmForm()
    if form.validate_on_submit():
        film = Film(name=form.name.data,
                    link=form.link.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    day = form.day.data,
                    room = form.room.data,
                    language = form.language.data,
                    )
        db.session.add(film)
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/add_film.html', form=form)

@app.route('/add_workshop', methods=['GET', 'POST'])
@login_required
def add_workshop():
    if not current_user.admin:
        abort(403)
    form = WorkshopForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
        else:
            picture_filename = 'default.png'
        workshop = Workshop(name=form.name.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    day = form.day.data,
                    room = form.room.data,
                    picture_filename = picture_filename,
                    author=form.author.data,
                    description = form.description.data
                    )
        db.session.add(workshop)
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/add_workshop.html', form=form)

@app.route('/add_beseda', methods=['GET', 'POST'])
@login_required
def add_beseda():
    if not current_user.admin:
        abort(403)
    form = BesedaForm()
    if form.validate_on_submit():
        beseda = Beseda(name=form.name.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    host_id = form.host.data.id if form.host.data else None,
                    day = form.day.data,
                    room = form.room.data
                    )
        db.session.add(beseda)
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/add_beseda.html', form=form)

@app.route('/add_host', methods=['GET', 'POST'])
@login_required
def add_host():
    if not current_user.admin:
        abort(403)
    form = HostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
        else:
            picture_filename = 'default.png'
        host = Host(name=form.name.data,
                    description = form.description.data,
                    short_description = form.short_description.data,
                    picture_filename = picture_filename
                    )
        db.session.add(host)
        db.session.commit()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/add_host.html', form=form)


@app.route('/program/edit')
@login_required
def edit_program():
    if not current_user.admin:
        abort(403)
    return render_template('editing_program/edit_program.html', films=Film.query.all(), besedy=Beseda.query.all(), workshops=Workshop.query.all(), hosts=Host.query.all())


@app.route('/edit_film/<id>', methods=['GET', 'POST'])
@login_required
def edit_film(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
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
        film.language = form.language.data
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/edit_film.html', film=film, form=form)

@app.route('/edit_beseda/<id>', methods=['GET', 'POST'])
@login_required
def edit_beseda(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    beseda = Beseda.query.get(id)
    form = BesedaForm(name=beseda.name, host=Host.query.get(beseda.host_id),
                    time_from=datetime.datetime.strptime(beseda.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(beseda.time_to, '%H:%M').time(), day=beseda.day, room=beseda.room)
    if form.validate_on_submit():
        beseda.name = form.name.data
        if form.host.data:
            beseda.host_id = form.host.data.id
        else: beseda.host_id = None
        beseda.time_from = form.time_from.data.strftime('%H:%M')
        beseda.time_to = form.time_to.data.strftime('%H:%M')
        beseda.day = form.day.data
        beseda.room = form.room.data
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/edit_beseda.html', beseda=beseda, form=form)

@app.route('/edit_workshop/<id>', methods=['GET', 'POST'])
@login_required
def edit_workshop(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    workshop = Workshop.query.get(id)
    form = WorkshopForm(name=workshop.name,
                    time_from=datetime.datetime.strptime(workshop.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(workshop.time_to, '%H:%M').time(), day=workshop.day, room=workshop.room, author=workshop.author, description=workshop.description)
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            workshop.picture_filename = picture_filename
        workshop.name = form.name.data
        workshop.time_from = form.time_from.data.strftime('%H:%M')
        workshop.time_to = form.time_to.data.strftime('%H:%M')
        workshop.day = form.day.data
        workshop.room = form.room.data
        workshop.author = form.author.data
        workshop.description = form.description.data
        db.session.commit()
        global rooms
        rooms = get_rooms()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/edit_workshop.html', workshop=workshop, form=form)

@app.route('/edit_host/<id>', methods=['GET', 'POST'])
@login_required
def edit_host(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    host = Host.query.get(id)
    form = HostForm(name=host.name,
                    description=host.description, short_description=host.short_description)
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            picture_filename = secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            host.picture_filename = picture_filename
        host.name = form.name.data
        host.description = form.description.data
        host.short_description = form.short_description.data
        db.session.commit()
        return redirect(url_for('edit_program'))
    return render_template('editing_program/edit_host.html', host=host, form=form)


@app.route('/delete_film/<id>')
@login_required
def delete_film(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    Film.query.filter_by(id=id).delete()
    db.session.commit()
    global rooms
    rooms = get_rooms()
    return redirect(url_for('edit_program'))

@app.route('/delete_workshop/<id>')
@login_required
def delete_workshop(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    Workshop.query.filter_by(id=id).delete()
    db.session.commit()
    global rooms
    rooms = get_rooms()
    return redirect(url_for('edit_program'))

@app.route('/delete_beseda/<id>')
@login_required
def delete_beseda(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    Beseda.query.filter_by(id=id).delete()
    db.session.commit()
    global rooms
    rooms = get_rooms()
    return redirect(url_for('edit_program'))

@app.route('/delete_host/<id>')
@login_required
def delete_host(id):
    if not current_user.admin:
        abort(403)
    if not id.isdigit(): abort(404)
    id = int(id)
    Host.query.filter_by(id=id).delete()
    db.session.commit()
    global rooms
    rooms = get_rooms()
    return redirect(url_for('edit_program'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
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

#region fotogalerie
@app.route('/fotogalerie')
def fotogalerie():
    return render_template('fotogalerie.html', albums=list(albums_dict.items()))

@app.route('/fotogalerie/<album_id>')
def album(album_id):
    if album_id not in list(albums_dict.keys()):
        return "Album does not exist"
    files = list(os.listdir(f'app/static/fotogalerie/{album_id}/'))
    images = [f"/static/fotogalerie/{album_id}/{file}" for file in files]
    return render_template('album.html', images = images, name = albums_dict[album_id], id=album_id)

@app.route('/fotogalerie/<album_id>', methods=['POST'])
@login_required
def add_photos(album_id):
    if not current_user.admin:
        abort(403)
    try:
        if album_id not in list(albums_dict.keys()):
            return "Upload failed: album does not exist"
        uploaded_files = request.files.getlist("file[]")
        for file in uploaded_files:
            file.save(f'app/static/fotogalerie/{album_id}/{secure_filename(file.filename)}')
    except Exception as e:
        return f"Upload failed: {e}"
    return "Upload succesfull"

@app.route('/fotogalerie/new_album', methods=['POST'])
@login_required
def new_album():
    if not current_user.admin:
        abort(403)
    album_name = request.form.get('album_name')
    id = str(random.randint(0, 9999)).zfill(4)
    if id in list(albums_dict.keys()):
        return new_album(album_name)
    try:
        os.mkdir(f'app/static/fotogalerie/{id}')
        albums_dict[id] = album_name
        json.dump(albums_dict, open('app/static/fotogalerie/albums.json', 'w'))
        return "New album created succesfuly"
    except Exception as e:
        return f"Creating new album failed: {e}"
        
@app.route('/fotogalerie/delete_album/<album_id>', methods=['POST'])
@login_required
def delete_album(album_id):
    if not current_user.admin:
        abort(403)
    if album_id not in list(albums_dict.keys()):
        return "Album does not exist"
    del albums_dict[album_id]
    json.dump(albums_dict, open('app/static/fotogalerie/albums.json', 'w'))
    return "Album delted"
#endregion fotogalerie

#endregion admin

