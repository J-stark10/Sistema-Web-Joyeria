from datetime import datetime
from flask_login import UserMixin

from app import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer,primary_key=True)
    nombre_usuario = db.Column(db.String(50),unique=True,nullable=False)
    contrasena_hash = db.Column(db.String(255),nullable=False)
    rol = db.Column(db.String(20),nullable=False)
    activo = db.Column(db.Boolean,default=True,nullable=False)
    fecha_creacion = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    def get_id(self):
        return str(self.id_usuario)

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"