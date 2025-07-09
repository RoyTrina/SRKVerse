def format_tmdb_movie_data(movies):
    """Format TMDb movie data for cleaner output."""
    formatted = []
    for movie in movies:
        formatted.append({
            "title": movie.get("title", ""),
            "year": movie.get("release_date", "")[:4],
            "role": movie.get("character", ""),
            "genres": movie.get("genres", [])
        })
        return formatted