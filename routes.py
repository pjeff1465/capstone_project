#login
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User 

from flask import Flask 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = Flask.request.form['email']
    if email in login_user and Flask.request.form['password'] == login_user[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return Flask.redirect(Flask.url_for('protected'))

    return 'Bad login'

@auth.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

#class User(flask_login.UserMixin):
#    pass

@login_manager.user_loader
def user_loader(email):
    if email not in login_user:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in login_user:
        return

    user = User()
    user.id = email
    return user