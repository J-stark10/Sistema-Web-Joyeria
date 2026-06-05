from app.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False, unique=True)

    joyas = db.relationship('Joya', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre_categoria}>'