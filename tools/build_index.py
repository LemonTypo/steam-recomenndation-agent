import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DATA_DIR = Path("data")
GAMES_FILE = DATA_DIR / "all_games.json"

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

        # Check if there are more paginated results, if so, set the new "last_appid" and re-preform the request with the new parameter    
        if response_dictionary.get('have_more_results') == True:
                last_appid = response_dictionary.get('last_appid')
                all_apps.extend(response_dictionary.get('apps'))
                print ('New last app id = ' + str(last_appid))
        else:
            with open ('data/all_games.json', 'w') as f:
                # Appends the final list of apps to the all_apps dictionary
                all_apps.extend(response_dictionary.get('apps'))
                
                f.write(json.dumps(all_apps, indent=2))
            break

fetch_all_steam_games(STEAM_API_KEY)