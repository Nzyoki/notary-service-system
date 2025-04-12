from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_object="config.Config"):
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.document import document_bp
    from app.routes.notary import notary_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(notary_bp)
    
    # Load login manager user loader
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create a route to test the app
    @app.route('/')
    def index():
        return "Welcome to the Notary System"
    
    return app