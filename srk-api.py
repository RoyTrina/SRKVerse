# srk_api.py
import json
import random

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Shah Rukh Khan API")

# --- Sample Data (load from JSON or DB in a real app) ---
with open("data/movies.json") as f:
    movies = json.load(f)

with open("data/quotes.json") as f:
    quotes = json.load(f)

with open("data/awards.json") as f:
    awards = json.load(f)

with open("data/timeline.json") as f:
    timeline = json.load(f)

# --- TMDb Integration ---
API_KEY = "YOUR_TMDB_API_KEY"  # Replace it with your actual TMDb API key
BASE_URL = "https://api.themoviedb.org/3"

@app.get("/srk/movies/tmdb")
def fetch_movies_from_tmdb():
    srk_id = 33488  # Shah Rukh Khan's person_id in TMDb
    url = f"{BASE_URL}/person/{srk_id}/movie_credits"
    params = {"api_key": API_KEY, "language": "en-US"}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="TMDb API error")
    return response.json().get("cast", [])

# --- Movies Routes ---
@app.get("/srk/movies")
def get_all_movies():
    return movies

@app.get("/srk/movies/{year}")
def get_movies_by_year(year: int):
    return [m for m in movies if m["year"] == year]

@app.get("/srk/movie/{title}")
def get_movie_by_title(title: str):
    for m in movies:
        if m["title"].lower() == title.lower():
            return m
    raise HTTPException(404, detail="Movie not found")

@app.get("/srk/movies/top-rated")
def get_top_rated():
    return sorted(movies, key=lambda x: x.get("rating", 0), reverse=True)[:10]

@app.get("/srk/movies/genres/{genre}")
def get_by_genre(genre: str):
    return [m for m in movies if genre.lower() in [g.lower() for g in m.get("genres", [])]]

# --- Quotes Routes ---
@app.get("/srk/quotes")
def get_all_quotes():
    return quotes

@app.get("/srk/quotes/random")
def get_random_quote():
    return random.choice(quotes)

@app.get("/srk/quotes/movie/{title}")
def get_quotes_by_movie(title: str):
    return [q for q in quotes if q["movie"].lower() == title.lower()]

@app.get("/srk/quotes/tag/{tag}")
def get_quotes_by_tag(tag: str):
    return [q for q in quotes if tag.lower() in [t.lower() for t in q.get("tags", [])]]

# --- Awards Routes ---
@app.get("/srk/awards")
def get_awards():
    return awards

@app.get("/srk/awards/{year}")
def get_awards_by_year(year: int):
    return [a for a in awards if a["year"] == year]

@app.get("/srk/awards/type/{type}")
def get_awards_by_type(type: str):
    return [a for a in awards if type.lower() in a["type"].lower()]

# --- Timeline Routes ---
@app.get("/srk/timeline")
def get_timeline():
    return timeline

@app.get("/srk/events/{year}")
def get_events_by_year(year: int):
    return [e for e in timeline if e["year"] == year]

@app.get("/srk/debut")
def get_debut():
    for e in timeline:
        if "debut" in e.get("event", "").lower():
            return e
    raise HTTPException(404, detail="Debut not found")

# --- Fan Interaction Routes (stubbed) ---
fake_votes = {}

@app.get("/srk/polls/favorite-movie")
def get_votes():
    return fake_votes

@app.post("/srk/polls/favorite-movie")
def vote_favorite(title: str):
    fake_votes[title] = fake_votes.get(title, 0) + 1
    return {"message": "Vote recorded", "votes": fake_votes[title]}

@app.get("/srk/quiz")
def get_quiz():
    return {
        "question": "What was Shah Rukh Khan's debut film?",
        "options": ["Deewana", "Baazigar", "Kabhi Haan Kabhi Naa"],
        "answer": "Deewana"
    }

@app.post("/srk/quiz/validate")
def validate_quiz(answer: str):
    correct = "Deewana"
    return {"correct": answer.strip().lower() == correct.lower()}

@app.post("/srk/fan-messages")
def submit_message(name: str, message: str):
    return {"message": f"Thank you {name} for your message!"}