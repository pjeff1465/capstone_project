from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
