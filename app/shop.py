"""
system kavarny/cajovny (pripadne nekdy merche atd.)
"""
from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from flask_login import login_required
from app import app
from app.forms import ShopForm
from app.db_classes import ShopItem
from app import db
from app.utils import write_albums, load_albums
import random
import shutil
from werkzeug.utils import secure_filename
from .decorators import admin_required, wip_disabled
import os

shop = Blueprint('shop', __name__)

@shop.route("/add_shop_item", methods=['GET', 'POST'])
@login_required
@admin_required
def add_item():
    form = ShopForm()
    if form.validate_on_submit():
        shop_item = ShopItem(name=form.name.data,
                    item_type = form.item_type.data,
                    price = form.price.data
                    )
        db.session.add(shop_item)
        db.session.commit()
        flash('Změny uloženy')
        return redirect(url_for("shop.kavarna_cajovna"))
    return render_template('shop/add_shop_item.html', form=form)

@shop.route('/delete_shop_item/<id>')
@login_required
@admin_required
def delete_item(id):
    if not id.isdigit(): abort(404)
    id = int(id)
    ShopItem.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Změny uloženy')
    return redirect(url_for('shop.kavarna_cajovna'))

@shop.route("/kavarna_cajovna")
@wip_disabled
def kavarna_cajovna():
    kavarna_items = ShopItem.query.filter_by(item_type="kavarna")
    cajovna_items = ShopItem.query.filter_by(item_type="cajovna")
    return render_template('shop/kavarna_cajovna.html', kavarna_items=kavarna_items, cajovna_items=cajovna_items)