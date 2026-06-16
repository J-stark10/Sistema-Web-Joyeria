from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def roles_required(*roles):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            if current_user.rol not in roles:
                flash(
                    "No tienes permisos para acceder.",
                    "danger"
                )
                return redirect(
                    url_for("dashboard.index")
                )

            return f(*args, **kwargs)

        return decorated

    return decorator