from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME= 'tracker_database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wrkjfu;ibrf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app=app)

    from .views import views
    from .auth import auth
    from .transanctions import transanctions

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(transanctions, url_prefix="/transanctions")

    from .models import User

    with app.app_context():
        create_db()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_db():
    if not path.exists(f'tracker/{DB_NAME}'):
        db.create_all()
        print('Database created!')