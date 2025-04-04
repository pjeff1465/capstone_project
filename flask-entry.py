from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from flask_sqlalchemy import SQLAlchemy 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
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
    return redirect(url_for('auth.login'))
#def hello():
#    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
