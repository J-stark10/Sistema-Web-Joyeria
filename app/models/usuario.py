from datetime import datetime
from flask_login import UserMixin

from app import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer,primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True,nullable=False)
    contrasena_hash = db.Column(db.Text, nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    ventas = db.relationship('Venta', backref='usuario', lazy=True)
    compras = db.relationship('Compra', backref='usuario', lazy=True)
    ajustes_inventario = db.relationship('AjusteInventario', backref='usuario', lazy=True)

    def get_id(self):
        return str(self.id_usuario)
    
    @property
    def es_admin(self):
        return self.rol == 'ADMIN'
    
    @property
    def es_vendedor(self):
        return self.rol == 'VENDEDOR'

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"