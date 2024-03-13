from functools import wraps
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.admin: return 403
        return func(*args, **kwargs)
    return decorated_function