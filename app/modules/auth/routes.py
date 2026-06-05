from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import bcrypt
from app.modules.usuarios.models import Usuario
from app.modules.auth.forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(
            nombre_usuario=form.nombre_usuario.data.strip()
        ).first()

        if usuario and bcrypt.check_password_hash(usuario.contrasena_hash, form.contrasena.data):
            if not usuario.activo:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))

            login_user(usuario, remember=form.recordarme.data)

            next_page = request.args.get('next')
            flash(f'Bienvenido, {usuario.nombre_usuario}.', 'success')
            return redirect(next_page or url_for('dashboard.index'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', form=form, titulo='Iniciar sesión')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario actual."""
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))
