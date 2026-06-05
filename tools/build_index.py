import os
import json
import time
import requests
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DATABASE_PATH = 'data/steam_database.db'

def fetch_all_steam_games(STEAM_API_KEY):

    url = f"https://api.steampowered.com/IStoreService/GetAppList/v1?key={STEAM_API_KEY}"
    last_appid = 0
    all_apps = []

    while True:
        query = {
            "include_games":True,
            "include_dlc": False,
            "include_videos": False,
            "include_hardware": False, 
            "max_results": 50000,
            "last_appid": last_appid
        }

        response_object = requests.get(url, params=query)
        
        # Convert response object into "json" (..actually just a python dict) and extract out everything under the "resposne" key
        response_dictionary = response_object.json()
        response_dictionary = response_dictionary.get('response')

        # Check if there are more paginated results, if so, set the new "last_appid" and re-perform the request with the new parameter    
        if response_dictionary.get('have_more_results') == True:
                last_appid = response_dictionary.get('last_appid')
                all_apps.extend(response_dictionary.get('apps'))
                print ('New last app id = ' + str(last_appid))
        else:
            with open ('data/all_games.json', 'w') as f:
                # Appends the final list of apps to the all_apps dictionary
                all_apps.extend(response_dictionary.get('apps'))
                f.write(json.dumps(all_apps, indent=2))

                # Connect to the database and prepare for... insertion ;)
                db_connector_object = sqlite3.connect('data/steam_database.db')
                db_cursor_object = db_connector_object.cursor()

                for app in all_apps:
                    id = app.get('appid')
                    name = app.get('name')
                    last_modified = app.get('last_modified')
                    
                    # https://www.geeksforgeeks.org/python/python-sqlite/ | Inserting Variables - https://stackoverflow.com/questions/4360593/python-sqlite-insert-data-from-variables-into-table
                    # INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
                    db_cursor_object.execute("INSERT OR IGNORE INTO steam_apps (id, name, last_modified) VALUES (?, ?, ?)", (id, name, last_modified))
                    db_cursor_object.execute("INSERT OR IGNORE INTO app_tags (id) VALUES (?)", (id))
        
            db_connector_object.commit()
            

            statement = '''SELECT id, name FROM steam_apps'''
            print(db_cursor_object.execute(statement).fetchmany(50))
                    
            break

def populate_game_details(STEAM_API_KEY):
    db_connector_object = sqlite3.connect(DATABASE_PATH)  
    db_cursor_object = db_connector_object.cursor()

    # Store all app ids currently in the sqlite3 database to a list to loop through
    all_app_ids = db_connector_object.execute("SELECT id FROM steam_apps")

    # This will take hella long to run due to steam api rate limits - approx. ~20ish hours? 
    for id in all_app_ids:
        last_appid = 0
        url = f"https://store.steampowered.com/api/appdetails?appids={id}"

        response_object = request.get(url)
        





          




populate_game_details(STEAM_API_KEY)
#fetch_all_steam_games(STEAM_API_KEY)