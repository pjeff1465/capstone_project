# This file will define all functions included in main.py, including connection to database

import sqlite3
import os
from datetime import datetime
from queries import *

## Connect to database ##
def connect_to_db(db_name = "mealplan.db"):
    try: # if db does not exist, create it
        cnx = sqlite3.connect(db_name)
        cnx.row_factory = sqlite3.Row
        cursor = cnx.cursor()
        print(f"Successfully connected to {db_name}!")
        return cnx, cursor
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None

def init_db_from_sql(cnx, cursor, sql_file="mealplan_DB.sql"):
    try:
        if not os.path.isfile(sql_file):
            print(f"SQL file {sql_file} does not exist!")
            return False
        
        with open(sql_file, 'r') as file:
            sql_script = file.read()

        cursor.executescript(sql_script)
        cnx.commit()
        print(f"Database initalized succesffuly from {sql_file}!")
        return True
    except sqlite3.Error as e:
        print(f"Error initalizing database: {e}")
        return False
    
def add_user(cnx, cursor, email, username, password):
    try:
        #created = datetime.now().isoformat()
        cursor.execute(CREATE_USER, (email, username, password)) # NEED TO CREATE CREATE_USER QUERY
        cnx.commit()
        print(f"User {username} added successfully!")
        return True
    except sqlite3.IntegrityError:
        print(f"User {username} or email {email} already exists!")
        return False
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")
        return False
    
def close_cnx(cnx):
    if cnx:
        cnx.close()
        print("Database connection closed")