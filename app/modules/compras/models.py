from app.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA_TZ = ZoneInfo("America/La_Paz")

class Compra(db.Model):
    __tablename__ = 'compra'

    id_compra = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    fecha_compra = db.Column(db.DateTime, default=lambda: datetime.now(BOLIVIA_TZ))
    total_compra = db.Column(db.Numeric(12, 2), nullable=False)
    estado = db.Column(db.String(20), default='COMPLETADA')

    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True, cascade='all, delete-orphan')
    proveedor = db.relationship('Proveedor', back_populates='compras')
    usuario = db.relationship('Usuario', back_populates='compras')

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, estado=None):

        if estado is not None:
            self.estado = estado.strip()

        db.session.commit()

    def anular(self):
        self.estado = 'ANULADA'
        db.session.commit()

    # CONSULTAS
    @staticmethod
    def get_all():
        return Compra.query.order_by(Compra.id_compra.desc()).all()

    @staticmethod
    def get_by_id(id_compra):
        return Compra.query.get(id_compra)

    @staticmethod
    def get_completadas():
        return Compra.query.filter_by(estado='COMPLETADA').all()

    @staticmethod
    def get_anuladas():
        return Compra.query.filter_by(estado='ANULADA').all()

    # REPRESENTACIÓN
    def __repr__(self): 
        return f'<Compra #{self.id_compra} | Estado: {self.estado} | Total: {self.total_compra}>'
    
class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'

    id_det_compra = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compra.id_compra'), nullable=False)
    id_joya = db.Column(db.Integer, db.ForeignKey('joya.id_joya'), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unit_compra = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(12,2), nullable=False)

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    # CONSULTAS
    @staticmethod
    def get_by_compra(id_compra):
        return DetalleCompra.query.filter_by(id_compra=id_compra).all()

    @staticmethod
    def get_by_id(id_det_compra):
        return DetalleCompra.query.get(id_det_compra)

    # REPRESENTACIÓN
    def __repr__(self):
        return f'<DetalleCompra compra#{self.id_compra} | joya#{self.id_joya} | canti: {self.cantidad}'