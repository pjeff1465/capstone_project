-- Used to create all tables used in database

-- Stores users and user information 
CREATE TABLE IF NOT EXISTS USER (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(250) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);