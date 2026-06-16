from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.modules.usuarios.services import UsuarioService

from app.auth.decorators import roles_required
from flask_login import login_required

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route("/")
@login_required
@roles_required('ADMIN')
def index():
    usuarios = UsuarioService.listar_usuarios()
    return render_template("usuarios/index.html",usuarios=usuarios)

@usuario_bp.route("/crear", methods=["GET", "POST"])
@roles_required('ADMIN')
def crear():
    if request.method == "POST":
        try:
            UsuarioService.crear_usuario(
                nombre_usuario=request.form["nombre_usuario"],
                password=request.form["password"],
                rol=request.form["rol"]
            )
            flash( "Usuario creado correctamente.", "success")
            return redirect(url_for("usuario.index"))

        except ValueError as e:
            flash(str(e),"danger")

    return render_template("usuarios/crear.html")

@usuario_bp.route("/editar/<int:id_usuario>", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def editar(id_usuario):

    try:
        usuario = UsuarioService.obtener_usuario(id_usuario)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuario.index"))

    if request.method == "POST":

        try:
            UsuarioService.actualizar_usuario(
                id_usuario=id_usuario,
                nombre_usuario=request.form["nombre_usuario"],
                rol=request.form["rol"],
                activo="activo" in request.form
            )

            password = request.form.get("password")

            if password and password.strip():
                UsuarioService.cambiar_password(
                    id_usuario,
                    password
                )

            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuario.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("usuarios/editar.html", usuario=usuario)

@usuario_bp.route("/password/<int:id_usuario>",methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def cambiar_password(id_usuario):
    try:
        usuario = UsuarioService.obtener_usuario(id_usuario)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("usuario.index"))

    if request.method == "POST":
        password = request.form["password"]
        UsuarioService.cambiar_password(
            id_usuario,
            password
        )
        flash("Contraseña actualizada.","success")
        return redirect(url_for("usuario.index"))

    return render_template("usuarios/cambiar_password.html",usuario=usuario)

@usuario_bp.route("/desactivar/<int:id_usuario>")
@login_required
@roles_required('ADMIN')
def desactivar(id_usuario):
    try:
        UsuarioService.desactivar_usuario(id_usuario)
        flash("Usuario desactivado.", "warning")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("usuario.index"))


@usuario_bp.route("/activar/<int:id_usuario>")
@login_required
@roles_required('ADMIN')
def activar(id_usuario):
    try:
        UsuarioService.activar_usuario(id_usuario)
        flash("Usuario activado.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("usuario.index"))



from flask_login import login_required, current_user

@usuario_bp.route("/perfil", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN','VENDEDOR')
def perfil():

    if request.method == "POST":

        password_actual = request.form.get("password_actual", "").strip()
        password_nueva = request.form.get("password_nueva", "").strip()
        password_confirmacion = request.form.get("password_confirmacion", "").strip()

        try:

            if not password_actual:
                raise ValueError(
                    "Debe ingresar su contraseña actual."
                )

            if not password_nueva:
                raise ValueError(
                    "Debe ingresar una nueva contraseña."
                )

            if password_nueva != password_confirmacion:
                raise ValueError(
                    "La confirmación de contraseña no coincide."
                )

            if not current_user.check_password(password_actual):
                raise ValueError(
                    "La contraseña actual es incorrecta."
                )

            if len(password_nueva) < 6:
                raise ValueError(
                    "La nueva contraseña debe tener al menos 6 caracteres."
                )

            current_user.update_password(password_nueva)

            flash(
                "La contraseña fue actualizada correctamente.",
                "success"
            )

            return redirect(
                url_for("usuario.perfil")
            )

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "usuarios/perfil.html"
    )
