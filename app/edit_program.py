from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from werkzeug.utils import secure_filename
from .decorators import perm_program_edit_required
import os
from app.forms import FilmForm, BesedaForm, WorkshopForm, HostForm
from app.db_classes import Film, Host, Beseda, Workshop
from .utils import update_rooms, random_hex_token
import datetime
from flask import request

edit_program = Blueprint('edit_program', __name__)

@edit_program.route('/program/edit')
@login_required
@perm_program_edit_required
def index():
    films = Film.query.all()
    besedy = Beseda.query.all()
    workshops = Workshop.query.all()
    hosts = Host.query.all()
    sort = request.args.get("sort")
    if sort:
        if sort == "day" or sort== "time":
            films.sort(key=lambda x: (x.day, x.time_from))
            besedy.sort(key=lambda x: (x.day, x.time_from))
            workshops.sort(key=lambda x: (x.day, x.time_from))
        elif sort == "room":
            films.sort(key=lambda x: x.room)
            besedy.sort(key=lambda x: x.room)
            workshops.sort(key=lambda x: x.room)
        elif sort == "name":
            films.sort(key=lambda x: x.name.lower())
            besedy.sort(key=lambda x: x.name.lower())
            workshops.sort(key=lambda x: x.name.lower())
            hosts.sort(key=lambda x: x.name.lower())
    return render_template('editing_program/edit_program.html', films=films, besedy=besedy, workshops=workshops, hosts=hosts)

@edit_program.route('/program/edit/interactive/<dayn>')
@login_required
@perm_program_edit_required
def interactive(dayn):
    update_rooms() # tohle je tu proto, protoze kdyz server bezi s vic workerama tak se updatne vzdycky jenom u jednoho app.rooms a jsou s tim pak problemy
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)
    program = {}
    for room in app.rooms[dayn]:
        program[room] = {}
        program[room]["films"] = sorted(Film.query.filter_by(day=dayn, room=room).all(), key=lambda film:film.time_from)
        program[room]["besedy"] = sorted(Beseda.query.filter_by(day=dayn, room=room).all(), key=lambda beseda:beseda.time_from)
        program[room]["workshops"] = sorted(Workshop.query.filter_by(day=dayn, room=room).all(), key=lambda workshop:workshop.time_from)
    return render_template('editing_program/edit_interactive.html', program=program, rooms=app.rooms[dayn], day=dayn)

@edit_program.route('/add_film', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def add_film():
    form = FilmForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
        else:
            picture_filename = 'default.png'
        film = Film(name=form.name.data,
                    link=form.link.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    day = form.day.data,
                    room = form.room.data,
                    picture_filename = picture_filename,
                    language = form.language.data,
                    description = form.description.data,
                    short_description = form.short_description.data,
                    filename = form.filename.data,
                    vg = form.vg.data,
                    )
        db.session.add(film)
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/add_film.html', form=form)

@edit_program.route('/add_workshop', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def add_workshop():
    form = WorkshopForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
        else:
            picture_filename = 'default.png'
        workshop = Workshop(name=form.name.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    day = form.day.data,
                    room = form.room.data,
                    picture_filename = picture_filename,
                    author=form.author.data,
                    description = form.description.data,
                    vg = form.vg.data,
                    )
        db.session.add(workshop)
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/add_workshop.html', form=form)

@edit_program.route('/add_beseda', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def add_beseda():
    form = BesedaForm()
    if form.validate_on_submit():
        beseda = Beseda(name=form.name.data,
                    time_from = form.time_from.data.strftime('%H:%M'),
                    time_to = form.time_to.data.strftime('%H:%M'),
                    host_id = form.host.data.id if form.host.data else None,
                    day = form.day.data,
                    room = form.room.data,
                    vg = form.vg.data,
                    )
        db.session.add(beseda)
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/add_beseda.html', form=form)

@edit_program.route('/add_host', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def add_host():
    form = HostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
        else:
            picture_filename = 'default.png'
        host = Host(name=form.name.data,
                    description = form.description.data,
                    short_description = form.short_description.data,
                    picture_filename = picture_filename
                    )
        db.session.add(host)
        db.session.commit()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/add_host.html', form=form)

@edit_program.route('/edit_film/<id>', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def edit_film(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    film = Film.query.get(id)
    form = FilmForm(name=film.name, 
                    link=film.link, time_from=datetime.datetime.strptime(film.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(film.time_to, '%H:%M').time(),
                    day=film.day, room=film.room, language=film.language, description=film.description, short_description=film.short_description, filename=film.filename, vg=film.vg)
    if form.validate_on_submit():
        if form.picture.data:
            try:
                if not film.picture_filename == "default.png":
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", film.picture_filename))
            except Exception as e:
                flash(f'Unable to delete old image: {e}')
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
            film.picture_filename = picture_filename
        film.name = form.name.data
        film.link = form.link.data
        film.time_from = form.time_from.data.strftime('%H:%M')
        film.time_to = form.time_to.data.strftime('%H:%M')
        film.day = form.day.data
        film.room = form.room.data
        film.language = form.language.data
        film.description = form.description.data
        film.short_description = form.short_description.data
        film.filename = form.filename.data
        film.vg = form.vg.data
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/edit_film.html', film=film, form=form)

@edit_program.route('/edit_beseda/<id>', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def edit_beseda(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    beseda = Beseda.query.get(id)
    form = BesedaForm(name=beseda.name, host=Host.query.get(beseda.host_id),
                    time_from=datetime.datetime.strptime(beseda.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(beseda.time_to, '%H:%M').time(),
                    day=beseda.day, room=beseda.room, vg=beseda.vg)
    if form.validate_on_submit():
        beseda.name = form.name.data
        if form.host.data:
            beseda.host_id = form.host.data.id
        else: beseda.host_id = None
        beseda.time_from = form.time_from.data.strftime('%H:%M')
        beseda.time_to = form.time_to.data.strftime('%H:%M')
        beseda.day = form.day.data
        beseda.room = form.room.data
        beseda.vg = form.vg.data
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/edit_beseda.html', beseda=beseda, form=form)

@edit_program.route('/edit_workshop/<id>', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def edit_workshop(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    workshop = Workshop.query.get(id)
    form = WorkshopForm(name=workshop.name,
                    time_from=datetime.datetime.strptime(workshop.time_from, '%H:%M').time(), time_to=datetime.datetime.strptime(workshop.time_to, '%H:%M').time(),
                    day=workshop.day, room=workshop.room, author=workshop.author, description=workshop.description, vg=workshop.vg)
    if form.validate_on_submit():
        if form.picture.data:
            try:
                if not workshop.picture_filename == "default.png":
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", workshop.picture_filename))
            except Exception as e:
                flash(f'Unable to delete old image: {e}')
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
            workshop.picture_filename = picture_filename
        workshop.name = form.name.data
        workshop.time_from = form.time_from.data.strftime('%H:%M')
        workshop.time_to = form.time_to.data.strftime('%H:%M')
        workshop.day = form.day.data
        workshop.room = form.room.data
        workshop.author = form.author.data
        workshop.description = form.description.data
        workshop.vg = form.vg.data
        db.session.commit()
        update_rooms()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/edit_workshop.html', workshop=workshop, form=form)

@edit_program.route('/edit_host/<id>', methods=['GET', 'POST'])
@login_required
@perm_program_edit_required
def edit_host(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    host = Host.query.get(id)
    form = HostForm(name=host.name,
                    description=host.description, short_description=host.short_description)
    if form.validate_on_submit():
        if form.picture.data:
            try:
                if not host.picture_filename == "default.png":
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", host.picture_filename))
            except Exception as e:
                flash(f'Unable to delete old image: {e}')
            picture = form.picture.data
            extension = picture.filename.split(".")[-1]
            picture_filename = random_hex_token() + "." + extension
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", picture_filename))
            host.picture_filename = picture_filename
        host.name = form.name.data
        host.description = form.description.data
        host.short_description = form.short_description.data
        db.session.commit()
        flash('Změny uloženy')
        return redirect(url_for('edit_program.index'))
    return render_template('editing_program/edit_host.html', host=host, form=form)


@edit_program.route('/delete_film/<id>')
@login_required
@perm_program_edit_required
def delete_film(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    film = Film.query.filter_by(id=id).first()
    try:
        if not film.picture_filename == "default.png":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", film.picture_filename))
    except: pass
    Film.query.filter_by(id=id).delete()
    db.session.commit()
    update_rooms()
    flash('Změny uloženy')
    return redirect(url_for('edit_program.index'))

@edit_program.route('/delete_workshop/<id>')
@login_required
@perm_program_edit_required
def delete_workshop(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    workshop = Workshop.query.filter_by(id=id).first()
    try:
        if not workshop.picture_filename == "default.png":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", workshop.picture_filename))
    except: pass
    Workshop.query.filter_by(id=id).delete()
    db.session.commit()
    update_rooms()
    flash('Změny uloženy')
    return redirect(url_for('edit_program.index'))

@edit_program.route('/delete_beseda/<id>')
@login_required
@perm_program_edit_required
def delete_beseda(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    Beseda.query.filter_by(id=id).delete()
    db.session.commit()
    update_rooms()
    flash('Změny uloženy')
    return redirect(url_for('edit_program.index'))

@edit_program.route('/delete_host/<id>')
@login_required
@perm_program_edit_required
def delete_host(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    host = Host.query.filter_by(id=id).first()
    try:
        if not host.picture_filename == "default.png":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "program_items", host.picture_filename))
    except: pass
    Host.query.filter_by(id=id).delete()
    db.session.commit()
    update_rooms()
    flash('Změny uloženy')
    return redirect(url_for('edit_program.index'))