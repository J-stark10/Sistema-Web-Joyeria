from app.extensions import db

class Venta(db.Model):
    __tablename__ = 'venta'

    id_venta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=True)

    fecha_venta = db.Column(db.DateTime, server_default=db.func.now())
    total_venta = db.Column(db.Numeric(12, 2), nullable=False)
    estado = db.Column(db.String(20), default='COMPLETADA')

    detalles = db.relationship('DetalleVenta', backref='venta',lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Venta #{self.id_venta} | Total: {self.total_venta} Bs.>'


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'),  nullable=False)
    id_joya = db.Column(db.Integer, db.ForeignKey('joya.id_joya'),    nullable=False)

    cantidad = db.Column(db.Integer,       nullable=False)
    precio_unit_venta = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(12,2), nullable=False)

    def __repr__(self):
        return f'<DetalleVenta venta#{self.id_venta} | joya#{self.id_joya} | cant:{self.cantidad}>'
