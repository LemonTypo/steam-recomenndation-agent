import sqlite3

db_connector_object = sqlite3.connect('data/steam_database.db')
db_cursor_object = db_connector_object.cursor()

create_app_table = """
    CREATE TABLE IF NOT EXISTS steam_apps (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT,
        description TEXT,
        tags TEXT,
        price REAL,
        multiplayer_type TEXT, 
        review_score REAL
    );
"""

create_tag_table = """
    CREATE TABLE IF NOT EXISTS app_tags  (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        tags TEXT
    );
"""

db_cursor_object.execute(create_app_table)
db_cursor_object.execute(create_tag_table)

db_connector_object.commit()



db_connector_object.close()


