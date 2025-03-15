import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configuración de la base de datos MySQL
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/usuarios_v'  # Reemplaza 'password' por tu contraseña
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar el seguimiento de modificaciones
    db.init_app(app)
    migrate.init_app(app, db)
