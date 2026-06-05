from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ci_nit = db.Column(db.String(30),  nullable=False, unique=True)
    telefono = db.Column(db.String(30))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())

    ventas = db.relationship('Venta', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nombre} | CI/NIT: {self.ci_nit}>'