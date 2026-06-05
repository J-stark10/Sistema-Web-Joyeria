from app.extensions import db

class Material(db.Model):
    __tablename__ = 'material'

    id_material     = db.Column(db.Integer, primary_key=True)
    nombre_material = db.Column(db.String(100), nullable=False, unique=True)

    joyas = db.relationship('Joya', backref='material', lazy=True)

    def __repr__(self):
        return f'<Material {self.nombre_material}>'
