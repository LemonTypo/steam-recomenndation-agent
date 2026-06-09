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
        review_score REAL,
        release_date TEXT,
        details_fetched INTEGER,
        last_modified INTEGER
    );
"""

db_cursor_object.execute(create_app_table)

db_connector_object.commit()
db_connector_object.close()