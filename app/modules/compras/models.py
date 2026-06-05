from app.extensions import db

class Compra(db.Model):
    __tablename__ = 'compra'

    id_compra = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    fecha_compra = db.Column(db.DateTime, server_default=db.func.now())
    total_compra = db.Column(db.Numeric(12, 2), nullable=False)
    estado = db.Column(db.String(20), default='PENDIENTE')

    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True, cascade='all, delete-orphan')

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

    def __repr__(self):
        return f'<DetalleCompra compra#{self.id_compra} | joya#{self.id_joya} | canti: {self.cantidad}'