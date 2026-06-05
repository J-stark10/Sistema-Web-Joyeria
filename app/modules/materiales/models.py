from app.extensions import db

class Material(db.Model):
    __tablename__ = 'material'

    id_material     = db.Column(db.Integer, primary_key=True)
    nombre_material = db.Column(db.String(100), nullable=False, unique=True)

    joyas = db.relationship('Joya', backref='material', lazy=True)

    # ==========================
    # CRUD
    # ==========================

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre_material=None):

        if nombre_material is not None:
            self.nombre_material = nombre_material

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ==========================
    # CONSULTAS
    # ==========================

    @staticmethod
    def get_all():
        return Material.query.order_by(Material.nombre_material).all()

    @staticmethod
    def get_by_id(id_material):
        return Material.query.get(id_material)

    @staticmethod
    def get_by_nombre(nombre_material):
        return Material.query.filter_by(nombre_material=nombre_material).first()

    # ==========================
    # REPRESENTACIÓN
    # ==========================

    def __repr__(self):
        return f'<Material {self.nombre_material}>'
