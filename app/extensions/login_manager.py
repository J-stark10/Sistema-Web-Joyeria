from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    from app.modules.usuarios.models import Usuario

    return Usuario.query.filter_by(
        id_usuario=int(user_id)
    ).first()