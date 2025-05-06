from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from collections import defaultdict
import uuid

from app.extensions import db, login_manager
from app.models import User, Recipes 
from app.api_handler import get_recipes

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

#globaly store cache of recipes in server-side memory
recipes_cache = {}

@auth.route('/data', methods=['POST'])
@login_required
def call_api():
    query = request.form.get('query') # attempts to pull search query field from html form where route is called

    # build recipe list with added filters
    health_filters = request.form.getlist('health[]')
    diet_filters = request.form.getlist('diet[]')
    meal_filters = request.form.getlist('mealType[]')
    cuisine_filters = request.form.getlist('cuisineType[]')
    dish_filters = request.form.getlist('dishType[]')
    min_val = request.form.get('min_value')
    max_val = request.form.get('max_value')

    recipe_list = get_recipes(search_query=query, health=health_filters, meal=meal_filters, cuisine=cuisine_filters, diet=diet_filters, dish=dish_filters, cal_min=min_val, cal_max=max_val)

    global recipes_cache

    # Assign UUIDs and store in server-side cache
    recipe_links = []
    for recipe in recipe_list:
        recipe_id = str(uuid.uuid4())  # Generate unique ID for each recipe
        recipes_cache[recipe_id] = recipe  # Store recipe data in cache
        recipe_links.append((recipe, recipe_id)) # Make list of recipes along with unique ID's to display on results list. With the UUIDs in recipe_links, we can link to any recipe details by retrieving the data from the server-side cache.

    return render_template('results_list.html', recipe_links = recipe_links)

@auth.route('/recipe_details/<recipe_id>')
@login_required
def recipe_details(recipe_id):

    #retrieve recipe based on UUID (unique id passed through the url from results list, associated with respective recipe data)
    recipe = recipes_cache.get(recipe_id)
    if not recipe:
        flash("Recipe not found.", "danger")
        return redirect(url_for('auth.dashboard'))

    return render_template('recipe_details.html', recipe=recipe, recipe_id=recipe_id)

@auth.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    recipe = recipe_id
    return render_template('recipe.html', recipe=recipe)

@auth.route('/profile')
@login_required
def user_profile():
    saved_recipes = current_user.saved_recipes

    #MAKE GROCERY LIST
    grocery_dict = defaultdict(set)
    for recipe in saved_recipes:
        for ingredient in recipe.ingredients:
            food_name = ingredient.get('food_name')
            food_category = ingredient.get('food_category', 'Uncategorized')
            grocery_dict[food_category.lower().capitalize()].add(food_name)

    grocery_list = {category: sorted(list(foods)) for category, foods in grocery_dict.items()}
    return render_template('user.html', saved_recipes=saved_recipes, grocery_list=grocery_list)

@auth.route('/save_recipe/<recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = recipes_cache.get(recipe_id)
    if not recipe:
        flash("Recipe not found.", "danger")
        return redirect(url_for('auth.dashboard'))

    # Check if recipe already saved
    existing_recipe = Recipes.query.filter_by(user_id=current_user.id, url=recipe['url']).first()
    if existing_recipe:
        flash("This recipe is already saved!", "warning")
        recipe_links = [(v, k) for k, v in recipes_cache.items()]
        return render_template('results_list.html', recipe_links=recipe_links)
    
    # Create and save the recipe to DB
    saved = Recipes(
        user_id=current_user.id,
        recipe_id=recipe_id,
        label=recipe['label'],
        image=recipe['image'],
        url=recipe['url'],
        calories=recipe['calories'],
        servings=recipe['servings'],
        ingredients=recipe['ingredients']
    )
    db.session.add(saved)
    db.session.commit()

    flash("Recipe saved to your profile!", "success")
    return redirect(url_for('auth.user_profile'))

@auth.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id, user_id=current_user.id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted successfully.", "success")
    else:
        flash("Recipe not found or unauthorized.", "danger")
    return redirect(url_for('auth.user_profile'))
