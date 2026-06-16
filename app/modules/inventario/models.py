from app.extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

BOLIVIA_TZ = ZoneInfo("America/La_Paz")

class AjusteInventario(db.Model):
    __tablename__ = 'ajuste_inventario'

    id_ajuste = db.Column(db.Integer, primary_key=True)
    id_joya = db.Column(db.Integer, db.ForeignKey('joya.id_joya'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    fecha_ajuste = db.Column(db.DateTime, default=lambda: datetime.now(BOLIVIA_TZ))
    cantidad_ajuste = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Text)
    tipo_ajuste = db.Column(db.String(20), nullable=False)

    # CRUD
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return AjusteInventario.query.order_by(AjusteInventario.fecha_ajuste.desc()).all()

    @staticmethod
    def get_by_id(id_ajuste):
        return AjusteInventario.query.get(id_ajuste)

    @staticmethod
    def get_by_joya(id_joya):
        return AjusteInventario.query.filter_by(id_joya=id_joya).order_by(AjusteInventario.fecha_ajuste.desc()).all()

    # REPRESENTACIÓN
    def __repr__(self):
        return f'<AjusteInventario joya#{self.id_joya} | {self.tipo_ajuste} | cant: {self.cantidad_ajuste}>'