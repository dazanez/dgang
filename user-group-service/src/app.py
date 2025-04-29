from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config
from .models import db
from .routes import groups

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Registrar blueprints
    app.register_blueprint(groups, url_prefix='/api/v1')
    
    # Crear las tablas de la base de datos
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)