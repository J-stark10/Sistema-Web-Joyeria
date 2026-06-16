from app.extensions import db
from sqlalchemy import func

class Joya(db.Model):
    __tablename__ = 'joya'

    id_joya = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(150), nullable=False)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    id_material = db.Column(db.Integer, db.ForeignKey('material.id_material'), nullable=False)

    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)

    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)

    activo = db.Column(db.Boolean, default=True)

    detalles_venta = db.relationship('DetalleVenta', back_populates='joya', lazy=True)
    detalles_compra = db.relationship('DetalleCompra', backref='joya', lazy=True)
    ajustes = db.relationship('AjusteInventario', backref='joya', lazy=True)
    categoria = db.relationship('Categoria', back_populates='joyas', lazy=True)

    # PROPIEDADES
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

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(
        self,
        codigo=None,
        nombre=None,
        id_categoria=None,
        id_material=None,
        precio_compra=None,
        precio_venta=None,
        stock_actual=None,
        stock_minimo=None,
        activo=None
    ):

        if codigo is not None:
            self.codigo = codigo.strip()

        if nombre is not None:
            self.nombre = nombre.strip()

        if id_categoria is not None:
            self.id_categoria = id_categoria

        if id_material is not None:
            self.id_material = id_material

        if precio_compra is not None:
            self.precio_compra = precio_compra

        if precio_venta is not None:
            self.precio_venta = precio_venta

        if stock_actual is not None:
            self.stock_actual = stock_actual

        if stock_minimo is not None:
            self.stock_minimo = stock_minimo

        if activo is not None:
            self.activo = activo

        db.session.commit()

    def delete(self):
        self.activo = False
        db.session.commit()

    def restore(self):
        self.activo = True
        db.session.commit()

    def aumentar_stock(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad a incrementar no puede ser negativa.")

        self.stock_actual += cantidad
        db.session.commit()

    def disminuir_stock(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad a descontar no puede ser negativa.")

        if cantidad > self.stock_actual:
            raise ValueError("La cantidad excede el stock disponible.")

        self.stock_actual -= cantidad
        db.session.commit()

    def actualizar_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.stock_actual = nuevo_stock
        db.session.commit()

    # CONSULTAS
    @staticmethod
    def get_all():
        return Joya.query.order_by(Joya.nombre).all()

    @staticmethod
    def get_activos():
        return Joya.query.filter_by(activo=True).order_by(Joya.nombre).all()

    @staticmethod
    def get_by_id(id_joya):
        return Joya.query.get(id_joya)

    @staticmethod
    def get_by_codigo(codigo):
        return Joya.query.filter(func.lower(Joya.codigo) == codigo.lower()).first()
    
    @staticmethod
    def get_stock_bajo():
        return Joya.query.filter(Joya.stock_actual <= Joya.stock_minimo, Joya.activo == True).all()

    # REPRESENTACIÓN
    def __repr__(self):
        return f'<Joya {self.codigo} | {self.nombre} | Stock: {self.stock_actual}>'