from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from flask_login import login_required
from app import app
from app.utils import write_albums, load_albums
import random
import shutil
from werkzeug.utils import secure_filename
from .decorators import admin_required
import os

IMAGE_THUMBNAIL_WIDTH = 500

from PIL import Image
def resize_image(input_path, output_path, new_width):
    with Image.open(input_path) as img:
        width, height = img.size
        new_height = int((new_width / width) * height)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(output_path)

fotogalerie = Blueprint('fotogalerie', __name__)

@fotogalerie.route('/')
def index():
    load_albums() # stejny problem jako s rooms_dict - pokud server bezi na vice workeru, albums_dict se updatuje vzdycky jenom v jednom a pak vznikaj problemy, proto je potreba cist vzdy ze souboru ikdyz je to postizeny
    return render_template('fotogalerie/fotogalerie.html', albums=list(app.albums_dict.items()))

@fotogalerie.route('/<album_id>')
def album(album_id):
    if album_id not in list(app.albums_dict.keys()):
        abort(404)
    files = [f for f in os.listdir(f'app/static/fotogalerie/{album_id}/') if not f.startswith('thumb')]
    images = [(f"/static/fotogalerie/{album_id}/{file}", f"/static/fotogalerie/{album_id}/thumb-{file}") for file in files] # [(imgae, thumbnail)]
    return render_template('fotogalerie/album.html', images=images, name=app.albums_dict[album_id], id=album_id)

@fotogalerie.route('/<album_id>', methods=['POST'])
@login_required
@admin_required
def add_photos(album_id):
    try:
        if album_id not in list(app.albums_dict.keys()):
            return abort(404)
        uploaded_files = request.files.getlist("file")
        for file in uploaded_files:
            fn = secure_filename(file.filename)
            file.save(f'app/static/fotogalerie/{album_id}/{fn}')
            resize_image(f'app/static/fotogalerie/{album_id}/{fn}', f'app/static/fotogalerie/{album_id}/thumb-{fn}', IMAGE_THUMBNAIL_WIDTH)
    except Exception as e:
        return f"Upload selhal: {e}"
    flash('Upload úspěšný')
    return redirect(f'{album_id}')

@fotogalerie.route('/new_album', methods=['POST'])
@login_required
@admin_required
def new_album():
    album_name = request.form.get('album_name')
    id = str(random.randint(0, 9999)).zfill(4)
    if id in list(app.albums_dict.keys()):
        return new_album()
    try:
        os.mkdir(f'app/static/fotogalerie/{id}')
        app.albums_dict[id] = album_name
        write_albums()
        flash('Nové album úspěšně vytvořeno')
        return redirect(url_for('fotogalerie.index'))
    except Exception as e:
        return f"Vytváření nového alba selhalo: {e}"
        
@fotogalerie.route('/delete_album/<album_id>')
@login_required
@admin_required
def delete_album(album_id):
    if album_id not in list(app.albums_dict.keys()):
        abort(404)
    del app.albums_dict[album_id]
    shutil.rmtree(f'app/static/fotogalerie/{album_id}')
    write_albums()
    flash('Album smazáno')
    return redirect(url_for('fotogalerie.index'))

@fotogalerie.route('/<album_id>/delete_photo/<photo_name>')
@login_required
@admin_required
def delete_photo(album_id, photo_name):
    if album_id not in list(app.albums_dict.keys()):
        abort(404)
    os.remove(f'app/static/fotogalerie/{album_id}/{photo_name}')
    return redirect(f'/fotogalerie/{album_id}')