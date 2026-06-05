from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.modules.usuarios.services import UsuarioService

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route("/")
def index():
    usuarios = UsuarioService.listar_usuarios()
    return render_template("usuarios/index.html",usuarios=usuarios)

@usuario_bp.route("/crear", methods=["GET", "POST"])
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

@usuario_bp.route( "/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar(id_usuario):
    usuario = UsuarioService.obtener_usuario( id_usuario)

    if not usuario:
        flash( "Usuario no encontrado.","danger")
        return redirect( url_for("usuario.index"))

    if request.method == "POST":
        try:
            UsuarioService.actualizar_usuario(
                id_usuario=id_usuario,
                nombre_usuario=request.form["nombre_usuario"],
                rol=request.form["rol"],
                activo="activo" in request.form
            )

            flash("Usuario actualizado correctamente.","success")
            return redirect(url_for("usuario.index"))

        except ValueError as e:
            flash(str(e),"danger")

    return render_template("usuarios/editar.html",usuario=usuario)

@usuario_bp.route("/password/<int:id_usuario>",methods=["GET", "POST"])
def cambiar_password(id_usuario):
    usuario = UsuarioService.obtener_usuario(id_usuario)

    if not usuario:
        flash("Usuario no encontrado.","danger")
        return redirect( url_for("usuario.index"))

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
def desactivar(id_usuario):
    try:
        UsuarioService.desactivar_usuario(id_usuario)
        flash( "Usuario desactivado.","warning")

    except ValueError as e:
        flash(str(e),"danger")

    return redirect( url_for("usuario.index") )


@usuario_bp.route("/activar/<int:id_usuario>")
def activar(id_usuario):
    try:
        UsuarioService.activar_usuario(id_usuario)
        flash("Usuario activado.","success")

    except ValueError as e:
        flash(str(e), "danger" )

    return redirect( url_for("usuario.index"))

