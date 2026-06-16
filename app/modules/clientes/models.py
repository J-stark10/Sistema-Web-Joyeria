from app.extensions import db
from sqlalchemy import func
from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA_TZ = ZoneInfo("America/La_Paz")

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ci_nit = db.Column(db.String(30),  nullable=False, unique=True)
    telefono = db.Column(db.String(8))
    direccion = db.Column(db.String(200))
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(BOLIVIA_TZ))
    activo = db.Column(db.Boolean, default=True, nullable=False)

    ventas = db.relationship('Venta', back_populates='cliente', lazy=True)

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre=None, ci_nit=None, telefono=None, direccion=None, activo=None):
        if nombre is not None:
            self.nombre = nombre.strip()
        if ci_nit is not None:
            self.ci_nit = ci_nit.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if direccion is not None:
            self.direccion = direccion.strip()
        if activo is not None:
            self.activo = activo

        db.session.commit()

    def deactivate(self):
        self.activo = False
        db.session.commit()

    def restore(self):
        self.activo = True
        db.session.commit()

    # CONSULTAS
    @staticmethod
    def get_all():
        return Cliente.query.order_by(Cliente.nombre).all()

    @staticmethod
    def get_activos():
        return Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()

    @staticmethod
    def get_by_id(id_cliente):
        return Cliente.query.get(id_cliente)

    @staticmethod
    def get_by_ci_nit(ci_nit):
        return Cliente.query.filter(func.lower(Cliente.ci_nit) == ci_nit.lower()).first()

    # REPRESENTACIÓN
    def __repr__(self):
        return f'<Cliente {self.nombre} | CI/NIT: {self.ci_nit}>'