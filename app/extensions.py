from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Crear instancias de las extensiones
db = SQLAlchemy()
migrate = Migrate()