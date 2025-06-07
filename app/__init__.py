from flask import Flask, session
from mongoengine import connect, connection
from app.config import Config
from models import *


def createapp():
    app=Flask(__name__)     

    app.config.from_object(Config)

    try:
        connect(host=Config.MONGO_URI)
        if connection.get_connection():
            print("Database Connected Successfully")
        else:
            print("Database Connection Failed")
    except Exception as e:
        print(e)
        raise e
    

    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.project import project_bp
    app.register_blueprint(project_bp, url_prefix='/project')

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')


    @app.context_processor
    def inject_user():
        data = session.get("user")
        userId = None

        if data:
            userId = data.get("id")
            
        user = User.objects(id=userId).first()

        if not user:
            return {
                "user": None,
                "isLoggedIn": False
            }
        return {
            "user": data,
            "isLoggedIn": True
        }

    return app