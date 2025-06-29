from fastapi import FastAPI

from routes import shah_rukh_khan_router

app = FastAPI(title="SRKverse API", version="1.0")

app.include_router(shah_rukh_khan_router, prefix="/srk")

# --- TMDb Integration ---
API_KEY = "YOUR_TMDB_API_KEY"  # Replace it with your actual TMDb API key
BASE_URL = "https://api.themoviedb.org/3"
