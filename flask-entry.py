from flask import Flask
from config import Config
from extensions import mealplan, login_manager


def create_app():

    app = Flask(__name__)

    from . import routes
    app.register_blueprint(routes.bp)
    
    return app

app = create_app()

@app.route('/')
def hello():
    return 'Hello World!'

with app.app_context():
    mealplan.create_all()

if __name__ == '__main__':
    app.run(debug=True)
