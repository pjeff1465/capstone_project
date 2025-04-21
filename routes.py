from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, login_manager
from models import User 
from api import get_recipes

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': # Save new login information to database
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first() # check if user already exists
        
        if existing_user:
            flash("Email already exists! Please log in.", "warning") # display warning message and redirect to log in page
            return render_template('login.html')
        
        hashed_password = generate_password_hash(password) # hash password before saving (do not store raw password)
        new_user = User(email=email, password=hashed_password) # create new user instance

        # save user to database
        db.session.add(new_user)
        db.session.commit()
        
# after storing user to DB redirect to login page. Allows to add email verifaction before automatically signing user in if wanted
        return redirect(url_for('auth.login')) 
    else: # its a GET request (user has not clicked sign up button)
        return render_template('signup.html')
    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    # fetch user from database
    user = User.query.filter_by(email=email).first()

    # check if password correct by referencing db
    if user and check_password_hash(user.password, password): 
        login_user(user)
        return redirect(url_for('auth.dashboard'))
    else:
        flash("Email or Password Incorrect! Please re-try.", "warning") # display warning message and redirect to log in page
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/data', methods=['POST'])
@login_required
def call_api():
    query = request.form.get('query') # attempts to pull search query field from html form where route is called. will need to add more lines for further filters
    recipe_list = get_recipes(search_query=query) #this function call, and the function itself will need to be updated to handle additional filters

    return render_template('results_list.html', recipes = recipe_list)