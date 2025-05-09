# CS4090 Capstone I Project
Meal-Plan Web Based App
## 1.0 Team Members:
Ryan Jepson, Piper Jeffries, Kelsey Bird, Evan Stamm

## 2.0 Problem Statement
Our project will solve the problem of not knowing what you are going to eat! Our app will give users an interface that is simple to use and understand to help them map out a meal plan for specific nutrition goals. It will allow users to create a grocery list for meals they have saved to their profile. Users will also be able to access a cookbook to save their recipes.

## 3.0 Proposed Solution
**3.1** - This application will provide meals and recipes where the user can provide multiple forms of input, such as the giving ingredients or filtering by food group

**3.2** - Key Features: 
- Select based on all meal times
    - Breakfast, lunch, dinner, snack, dessert, appetizer, etc.
- Drop-down Filter
- Type of food, meal price, amount of people, macros of nutrition, number of ingredients, time of day, etc.
- Scale recipe and provide appropriate ingredient amounts based on number of people or total calories.

**3.3** - Stretch Goals:
- Allow users to sign up for an account to access the following features: 
    - Sign-up goals
    - Grocery check-list
- Get macros, find new recipes, budget meals, explore new foods, etc.

## 4.0 Expected Outcome
**4.1** Minimum Viable Product Overview: A web based application which provides a meal plan and recipes for the user based on user needs.

**4.2** MVP Components:
- Users are able to filter search options for preferred food types per food group (i.e meat: chicken, beef, vegetables: beans, carrots, etc.)
- Users are able to filter for dietary needs (i.e, vegetarian, vegan, gluten-free)
- Users are able to view photo and text descriptions of recipes and save favorites to profile (if we set up database)


## 5.0 Dependencies

Full list of dependencies can be found in `./requirements.txt`

**5.1** - Backend: Python/Flask, SQLite

**5.2** - Frontend: HTML/CSS

## 6.0 Deployment / How to Run
To run or deploy this application see the following steps

Clone the git repo found here: [Git Repo](https://github.com/pjeff1465/capstone_project)

**6.1** - Python Virtual Environment 

Create a .venv in the root of the project folder and download the contents of requirements.txt using the following command: `pip install -r requirements.txt`

**6.2** - Run in development mode

To view this application you can run locally, hosted on localhost using the following command: `flask --app app/flask_entry run`
This application uses `flask-entry.py` as the entry point to create the app and initial route

**6.3** - Run Tests

Tests are split into files mirroring the file structure of the application.
To run any of the test files, ensure you are in the root directory and run the following: `pytest .\tests\<filename>`. For example: `pytest .\tests\test_api.py` which will run unit tests checking the functions which handle api requests. 

NOTE: the file `test_api_integration.py` is integration tests for the api and makes real requests to external api. This does not use mocking and therefore rate limits apply.

## 7.0 File Structure & Key Pages
Main python code is found in routes.py and api_handler.py. HTML files are found in templates/. Most styling/css is found in static/. Other files are used for database or configuration / setup settings.

- Dashboard: This page initially shows search bar, as well as filters required to generate personalized recipes, such as dietary restrictions, nutritional preferences, calories per serving, etc. Once the user chooses filters and makes a search they are redirected to results_list
- Results List: After a user has made a search this page populates with a list of all generated results, with each recipe having a card with name, picture, and link to view more details, which redirects to recipe_details
- Recipe Details: After selecting a recipe users will be brought to this page which shows all the detailed information about a recipe, including nutritional data (per serving & total), ingredients and other relevant tags. Here you can save a recipe to your user
- Profile: This page can be accessed by saving a recipe or navigating to the Profile tab on the navbar. This page will show all saved recipes for your user, as well as automatically generate a grocery list based on the ingredients present in your saved recipes.
