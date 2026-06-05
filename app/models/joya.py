from app import db

class Joya(db.Model):
    __tablename__ = 'joya'

    id_joya = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50),  nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    id_material = db.Column(db.Integer, db.ForeignKey('material.id_material'),   nullable=False)

    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)

    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)

    activo = db.Column(db.Boolean, default=True)

    detalles_venta = db.relationship('DetalleVenta',      backref='joya', lazy=True)
    detalles_compra = db.relationship('DetalleCompra',     backref='joya', lazy=True)
    ajustes = db.relationship('AjusteInventario',  backref='joya', lazy=True)

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo

    @property
    def valor_en_stock(self):
        return float(self.precio_compra) * self.stock_actual

    @property
    def margen_utilidad(self):
        return float(self.precio_venta) - float(self.precio_compra)

    @property
    def margen_porcentaje(self):
        if float(self.precio_venta) == 0:
            return 0
        return (self.margen_utilidad / float(self.precio_venta)) * 100

    def __repr__(self):
        return f'<Joya {self.codigo} | {self.nombre} | Stock: {self.stock_actual}>'
