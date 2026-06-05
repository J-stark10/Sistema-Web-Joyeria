from app.extensions import db

class AjusteInventario(db.Model):
    __tablename__ = 'ajuste_inventario'

    id_ajuste = db.Column(db.Integer, primary_key=True)
    id_joya = db.Column(db.Integer, db.ForeignKey('joya.id_joya'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    fecha_ajuste = db.Column(db.DateTime, server_default=db.func.now())
    cantidad_ajustada = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Text)
    tipo_ajuste = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<AjusteInventario joya#{self.id_joya} | {self.tipo_ajuste} | cant: {self.cantidad_ajustada}>'