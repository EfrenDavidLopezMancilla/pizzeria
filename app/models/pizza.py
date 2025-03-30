from app.extensions import db
from datetime import datetime

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    disponible = db.Column(db.Boolean, default=True)
    imagen_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_pizza.id'))
    categoria = db.relationship('Categoria', back_populates='pizzas')

    def __repr__(self):
        return f'<Pizza {self.nombre}>'