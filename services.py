import json
import random
from pathlib import Path
from models import Quote, Movie

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def load_movies() -> list[Movie]:
    with open(DATA_DIR / "movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
    return [Movie(**movie) for movie in movies]

def get_random_quote() -> Quote:
    quotes = [
        {"quote": "Don’t underestimate the power of a common man.", "movie": "Chennai Express", "year": 2013},
        {"quote": "Kabhi kabhi jeetne ke liye kuch haarna padta hai.", "movie": "Baazigar", "year": 1993},
        {"quote": "Picture abhi baaki hai mere dost.", "movie": "Om Shanti Om", "year": 2007}
    ]
    return Quote(**random.choice(quotes))
