from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user

from app.auth.forms import LoginForm
from app.auth.service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()

    if form.validate_on_submit():

        result = AuthService.autenticar(
            form.nombre_usuario.data,
            form.contrasena.data
        )

        if result == "INACTIVO":
            flash('Tu cuenta está desactivada.', 'danger')
            return redirect(url_for('auth.login'))

        if result:

            login_user(
                result,
                remember=form.recordarme.data
            )

            # Sesión permanente
            session.permanent = True

            next_page = request.args.get('next')

            if next_page and not next_page.startswith('/'):
                next_page = None

            flash(
                f'Bienvenido, {result.nombre_usuario}.',
                'success'
            )

            return redirect(
                next_page or url_for('dashboard.index')
            )

        flash(
            'Usuario o contraseña incorrectos.',
            'danger'
        )

    return render_template(
        'auth/login.html',
        form=form,
        titulo='Iniciar sesión'
    )


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()

    session.clear()

    flash(
        'Sesión cerrada correctamente.',
        'info'
    )

    return redirect(
        url_for('auth.login')
    )