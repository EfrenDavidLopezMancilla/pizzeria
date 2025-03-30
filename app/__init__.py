from flask import Flask
from .extensions import db, migrate
from dotenv import load_dotenv
import os
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # Configuración esencial
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-fallback-12345'),  # Clave secreta con valor por defecto
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_SECURE=False,  # True en producción con HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(days=1)
    )
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints dentro del contexto de la aplicación
    with app.app_context():
        from .routes.pizzas import pizzas_bp
        from .routes.categorias import categorias_bp
        from .routes.main import main_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(pizzas_bp, url_prefix='/pizzas')
        app.register_blueprint(categorias_bp, url_prefix='/categorias')
        
        # Crear tablas si no existen
        db.create_all()
    
    return app