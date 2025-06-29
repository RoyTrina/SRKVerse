import requests

API_KEY = "YOUR_TMDB_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"

def search_srk_movies():
    srk_id = 33488  # Shah Rukh Khan's person_id in TMDb
    url = f"{BASE_URL}/person/{srk_id}/movie_credits"
    params = {"api_key": API_KEY, "language": "en-US"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("cast", [])

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()