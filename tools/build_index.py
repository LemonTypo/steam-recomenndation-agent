import os
import json
import time
import requests
import sqlite3
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DATABASE_PATH = 'data/steam_database.db'

def fetch_all_steam_games(STEAM_API_KEY):

    url = f"https://api.steampowered.com/IStoreService/GetAppList/v1?key={STEAM_API_KEY}"
    last_appid = 0
    all_apps = []

    print("Starting to fetch all steam games- this should only take a minute or two...")
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
        
            db_connector_object.commit()
            

            statement = '''SELECT id, name FROM steam_apps'''
            print("Initial Database Build Complete")
                    
            break

def populate_game_details(STEAM_API_KEY):
    db_connector_object = sqlite3.connect(DATABASE_PATH)  
    db_cursor_object = db_connector_object.cursor()

    # Store all app ids currently in the sqlite3 database to a list to loop through
    all_app_ids = db_connector_object.execute("SELECT id FROM steam_apps WHERE details_fetched IS NULL").fetchall()

    # Set variables that will be useful for tracking progress- as each app gets looped it will increment the current_app_count and display it to the terminal
    current_app_count = 1
    total_app_count = len(all_app_ids)
   

    # This will take hella long to run due to steam api rate limits - approx. ~20ish hours? 

    print("Starting to fetch game details for each app- this will take roughly " + str(total_app_count * 2 / 3600) + " hours due to steam api rate limits...")
    #for id in all_app_ids: 
    # (INCLUDE A PROGRESS BAR TO SHOW CURRENT APP NUMBER OUT OF TOTAL NUMBER OF APPS) (ie. Working on app 6/160,000)
    id = 252490
    url = f"https://store.steampowered.com/api/appdetails?appids={id}&language=en"

    # Make the request to the steam api to get the game details for the current app id. Filter the response to get just the "data" key in the json output
    response_object = requests.get(url)
    response_dictionary = response_object.json()
    response_dictionary = response_dictionary.get(str(id)).get('data')

    #### --- Begin assigning relevant variables to game data to be INSERTED into the database --- ####
    description = response_dictionary.get('detailed_description')

    categories = response_dictionary.get('categories')
    genres = response_dictionary.get('genres')

    # Where I store the categories and genres for each game which will be stored in the "tags" column of the steam_apps table in the database
    tag_list = []

    # Loop through the categories JSON to just retrieve the category name and genre names to add to the tag_list list
    for category in categories:
         category_name = category.get('description')
         tag_list.append(category_name)
    for genre in genres:
        genre_name = genre.get('description')
        tag_list.append(genre_name)
    
    if response_dictionary.get('is_free') != True:
        price = response_dictionary.get('price_overview').get('final_formatted')
    else:
        price = 0

    time.sleep(2)

    url = f"https://store.steampowered.com/appreviews/{id}?purchase_type=all&filter=all&language=all"
  
    response_object = requests.get(url)
    response_dictionary = response_object.json()

    response_dictionary = response_dictionary.get('review_score')
    print (response_dictionary)

    # Can't lie, AI generated this regex because...regex
    review_data = re.findall(r'(\d+)%\s+of the\s+([\d,]+)', str(response_dictionary))

    if review_data:
        review_percentage_positive = review_data[0][0]
        review_percentage_positive = int(review_percentage_positive) / 100 # Converted to decimal for review_score calculation
        total_reviews = review_data[0][1]
        total_reviews = int(total_reviews.replace(',', '')) # Remove commas from the total reviews string and convert to int

        if total_reviews >= 500:
            review_score = review_percentage_positive

        else:
            review_score = None

    else:
        review_score = None

    #### --- END of assigning relevant variables to game data to be INSERTED into the database --- ####


    print('ID = ' + str(id))
    print('Tags = ' + str(tag_list))
    print('Price = ' + str(price))
    print('Review Score = ' + str(review_score))


populate_game_details(STEAM_API_KEY)
#fetch_all_steam_games(STEAM_API_KEY)