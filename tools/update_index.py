import os
import json
import requests
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


def find_new_ids(STEAM_API_KEY):

    db_connector_object = sqlite3.connect("data/steam_database.db")
    db_cursor_object = db_connector_object.cursor()

    # Get all of the current steam app ids from the existing database
    current_database_index = db_cursor_object.execute("SELECT id FROM steam_apps").fetchall()

    # fetchall() returns a list of tuples, converting that list of tuples to just a list. Not sure if necessary but seems useful
    current_database_index = [item[0] for item in current_database_index]

    db_connector_object.commit()
    db_connector_object.close()


    # Do not repeat yourself... ;) [ctrl + c] & [ctrl + v]
    url = f"https://api.steampowered.com/IStoreService/GetAppList/v1?key={STEAM_API_KEY}"
    last_appid = 0
    all_apps = []
    all_app_ids = []

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
            print ('Gathering paginated results... last_appid = ' + str(last_appid))
        else:
            all_apps.extend(response_dictionary.get('apps'))      
            break
    
    for app in all_apps:
        all_app_ids.append(app.get('appid'))

    # Return a list of all the app ids that are in the steam api but not in the current database index
    return set(all_app_ids) - set(current_database_index)

def update_index(new_app_ids):
    print("\nDetected " + str(len(new_app_ids)) + " new apps to add to the database...")



new_app_ids = find_new_ids(STEAM_API_KEY)


update_index(new_app_ids)