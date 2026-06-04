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

appid = 1174180 #RDR2

def get_game_tags():
    print("Hello! Tags and Bags")

    






