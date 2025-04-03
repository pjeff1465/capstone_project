from flask import Flask
from config import Config
from extensions import mealplan, login_manager

app = Flask(__name__)

with app.app_context():
    mealplan.create_all()

if __name__ == '__main__':
    app.run(debug=True)
