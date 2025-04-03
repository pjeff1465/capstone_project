from flask import Flask
app = Flask(__name__)

#login
import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if Flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = Flask.request.form['email']
    if email in users and Flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return Flask.redirect(Flask.url_for('protected'))

    return 'Bad login'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
