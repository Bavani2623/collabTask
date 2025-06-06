from flask import Flask
from mongoengine import connect, connection
from app.config import Config
from models import *


def createapp():
    app=Flask(__name__)     

    app.config.from_object(Config)

    try:
        connect(host=Config.MONGO__URI)
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




    return app