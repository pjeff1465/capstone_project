from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User 

 

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    # fetch user from database
    user = User.query.filter_by(email=email).first()

    # check if passwrod correct by referencing db
    if user and check_password_hash(user.password, password): 
        login_user(user)
        return redirect(url_for('auth.dashboard'))

    return 'Invalid email or password!'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

'''
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
'''

@auth.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.email}"

