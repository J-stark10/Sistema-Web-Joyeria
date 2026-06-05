from app.extensions import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_razon_social = db.Column(db.String(150), nullable=False)
    nit = db.Column(db.String(30), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True)

    compras = db.relationship('Compra', backref='proveedor', lazy=True)

    def __repr__(self):
        return f'<Proveedor {self.nombre_razon_social} | NIT: {self.nit}>'