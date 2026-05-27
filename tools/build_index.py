import os
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DATA_DIR = Path("data")
GAMES_FILE = DATA_DIR / "games.jsonl"
CHECKPOINT_FILE = DATA_DIR / "checkpoint.json"

def fetch_all_steam_games(STEAM_API_KEY):

    url = f"https://api.steampowered.com/IStoreService/GetAppList/v1?key={STEAM_API_KEY}"
    last_app_id = 0
    all_apps = []

    while True:
        query = {
            "include_games":True,
            "include_dlc": False,
            "include_videos": False,
            "include_hardware": False, 
            "max_results": 50000,
            "last_appid": last_app_id
        }

        response = requests.get(url, params=query)
        response = response.json()



        if last_app_id != response.get("last_appid"):
            last_app_id = response.get("last_appid")

        all_apps.extend(response["response"]["apps"])
        

        print("More Responses?" + str(response["response"]["have_more_results"]))

        if response["response"]["have_more_results"] != True:
            return all_apps
            break

    



    

    #response = json.dumps(response.json(), indent=2)
    
   #with open("data/all_games.json", mode='w') as f:
   #         f.write(response)




fetch_all_steam_games(STEAM_API_KEY)

    