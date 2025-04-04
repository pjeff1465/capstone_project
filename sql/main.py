# This file will include all use cases for funcs defined in funcs.py

from sql.funcs import *

def main():
    db_name = "mealplan.db"
    sql_file = "mealplan_DB.sql"

    cnx, cursor = connect_to_db(db_name)

    if cnx is None or cursor is None:
        print("Failed to connect to database")
        return
    
    if not init_db_from_sql(cnx, cursor, sql_file):
        print("Failed to initialize database from SQL file")
        close_cnx(cnx)
        return
    
    close_cnx(cnx)

if __name__ == "__main__":
    main()