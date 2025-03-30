from app.extensions import db
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = 'categorias_pizza'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pizzas = db.relationship('Pizza', back_populates='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'