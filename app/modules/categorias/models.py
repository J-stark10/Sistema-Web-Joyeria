from app.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False, unique=True)

    joyas = db.relationship('Joya', backref='categoria', lazy=True)

    # ==========================
    # CRUD
    # ==========================

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre_categoria=None):

        if nombre_categoria is not None:
            self.nombre_categoria = nombre_categoria

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ==========================
    # CONSULTAS
    # ==========================

    @staticmethod
    def get_all():
        return Categoria.query.order_by(Categoria.nombre_categoria).all()

    @staticmethod
    def get_by_id(id_categoria):
        return Categoria.query.get(id_categoria)

    @staticmethod
    def get_by_nombre(nombre_categoria):
        return Categoria.query.filter_by(nombre_categoria=nombre_categoria).first()

    # ==========================
    # REPRESENTACIÓN
    # ==========================

    def __repr__(self):
        return f'<Categoria {self.nombre_categoria}>'