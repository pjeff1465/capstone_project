from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from flask_sqlalchemy import SQLAlchemy 
from flask_login import current_user
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.urandom(24) #on startup, assign random key (used to secure session data). this will reset any persisting sessions
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from routes import auth 
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

@app.route('/')
def home():
    if current_user.is_authenticated: # flask_login feature that stores login state using cookie
        return redirect(url_for('auth.dashboard')) # directs user that is already logged in to dashboard instead of sign up page
    else:
        return redirect(url_for('auth.signup'))

if __name__ == '__main__':
    app.run(debug=True)
