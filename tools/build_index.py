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
    url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/?key={STEAM_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("applist", {}).get("apps", [])