#!/usr/bin/env python3

from funcs import *

cnx, cursor = connect_to_db("mealplan.db")

add_user(cnx, cursor, "piper_j", "piper@example.com", "1234")

cnx.close()