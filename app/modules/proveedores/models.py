from app.extensions import db
from sqlalchemy import func

class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_razon_social = db.Column(db.String(150), nullable=False)
    nit = db.Column(db.String(30), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True)

    compras = db.relationship('Compra', back_populates='proveedor', lazy=True)

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre_razon_social=None, nit=None, telefono=None, correo=None, activo=None):

        if nombre_razon_social is not None:
            self.nombre_razon_social = nombre_razon_social.strip()
        if nit is not None:
            self.nit = nit.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if correo is not None:
            self.correo = correo.strip()
        if activo is not None:
            self.activo = activo

        db.session.commit()

    def delete(self):
        self.activo = False
        db.session.commit()

    def restore(self):
        self.activo = True
        db.session.commit()

    # CONSULTAS
    @staticmethod
    def get_all():
        return Proveedor.query.order_by(Proveedor.nombre_razon_social).all()

    @staticmethod
    def get_activos():
        return Proveedor.query.filter_by(activo=True).order_by(Proveedor.nombre_razon_social).all()

    @staticmethod
    def get_by_id(id_proveedor):
        return Proveedor.query.get(id_proveedor)

    @staticmethod
    def get_by_nit(nit):
        return Proveedor.query.filter(func.lower(Proveedor.nit) == nit.lower()).first()

    # REPRESENTACIÓN
    def __repr__(self):
        return f'<Proveedor {self.nombre_razon_social} | NIT: {self.nit}>'