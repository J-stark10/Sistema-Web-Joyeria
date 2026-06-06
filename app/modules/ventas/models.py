from app.extensions import db

from decimal import Decimal

class Venta(db.Model):
    __tablename__ = 'venta'

    id_venta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=True)

    fecha_venta = db.Column(db.DateTime, server_default=db.func.now())
    total_venta = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    estado = db.Column(db.String(20), default='COMPLETADA')

    usuario = db.relationship('Usuario', back_populates='ventas')
    cliente = db.relationship('Cliente', back_populates='ventas')
    detalles = db.relationship('DetalleVenta', back_populates='venta', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Venta #{self.id_venta} | Total: {self.total_venta} Bs.>'

    # ==========================
    # MÉTODOS (AQUÍ VAN TODOS)
    # ==========================

    def save(self):
        db.session.add(self)
        db.session.commit()

    def calcular_total(self):
        return sum(d.subtotal for d in self.detalles)

    def actualizar_total(self):
        self.total_venta = sum(d.subtotal for d in self.detalles)

    def recalcular_total(self):
        self.total_venta = sum(
            Decimal(d.subtotal) for d in self.detalles
        )
        db.session.commit()

    def anular(self):
        self.estado = 'ANULADA'
        
    def finalizar(self):
        self.estado = 'COMPLETADA'
        db.session.commit()
    


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'), nullable=False)
    id_joya = db.Column(db.Integer, db.ForeignKey('joya.id_joya'), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unit_venta = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(12,2), nullable=False)

    venta = db.relationship('Venta', back_populates='detalles')
    joya = db.relationship('Joya', back_populates='detalles_venta')

    def __repr__(self):
        return f'<DetalleVenta venta#{self.id_venta} | joya#{self.id_joya} | cant:{self.cantidad}>'
