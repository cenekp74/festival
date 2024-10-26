from functools import wraps
from flask_login import current_user
from app import app
from flask import redirect, url_for, request, abort

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin: abort(403)
        return func(*args, **kwargs)
    return decorated_function

def perm_program_edit_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not (current_user.admin or current_user.perm_program_edit): abort(403)
        return func(*args, **kwargs)
    return decorated_function

def perm_shop_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not (current_user.admin or current_user.perm_shop): abort(403)
        return func(*args, **kwargs)
    return decorated_function

def wip_disabled(func): # decorator pro funkce co maj bejt zakazany v WIP modu
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if app.config['WIP_MODE']:
            if not current_user.is_authenticated and not "force-display" in request.args:
                return redirect(url_for('wip'))
        return func(*args, **kwargs)
    return decorated_function