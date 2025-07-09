# 🎬 SRKVerse – A Shah Rukh Khan Information API

Welcome to the **SRKVerse API** – a 🌟 RESTful API built with **Django REST Framework** that celebrates the legacy of Bollywood icon **Shah Rukh Khan**! 

This project provides structured access to SRK’s films, songs, quotes, awards, timeline, and fan interactions. 
Perfect for fan apps, trivia games, film databases, and Bollywood data mashups! 🎥

---

## 🚀 Features
🎞️ **Movies**: Browse SRK’s films with metadata from TMDb (`/api/srk/movies/tmdb/`) or the database (`/api/srk/movies/`), filter by year, genre, or title, and get top-rated films. <br>

🎵 **Songs**: Access iconic movie soundtracks with metadata (e.g., composer, lyricist) and admin-uploaded audio files (`/api/srk/songs/`, `/api/srk/movies/<title>/songs/`). <br>

🗣️ **Quotes**: Retrieve SRK’s memorable dialogues, filter by movie or tag, or get a random quote (`/api/srk/quotes/`, `/api/srk/quotes/random/`). <br>

🏆 **Awards**: Explore SRK’s accolades, filter by year or type (`/api/srk/awards/`). <br>

📅 **Timeline**: View key milestones in SRK’s career (`/api/srk/timeline/`). <br>

❤️ **Fan Interactions**: Submit fan messages (`/api/srk/fan-message/`), vote for favorite movies (`/api/srk/vote/`), and take SRK quizzes (`/api/srk/quiz/`). <br>

🛠️ **Admin Interface**: Manage data (e.g., upload song audio files) at http://localhost:8000/admin/. <br>

🌍 **Planned**: Spotify/YouTube API integration for enhanced song data, frontend templates for song playback.<br>

---

## 📁 Project Structure
srkverse-a-shah-rukh-khan-information-api/ <br>
├── .env                   # 🔑 Environment variables (SECRET_KEY, TMDB_API_KEY) <br>
├── manage.py              # ⚙️ Django command-line utility <br>
├── srkverse_api/         # 📚 Django project directory <br>
│   ├── __init__.py       # Package marker <br>
│   ├── settings.py       # ⚙️ Django settings (database, media, apps) <br>
│   ├── urls.py           # 🔗 Root URL routing <br>
│   ├── wsgi.py           # 🌐 WSGI config for deployment <br>
│   └── asgi.py           # 🌐 ASGI config for async deployment <br>
├── SRKVerse/             # 📂 Django app directory <br>
│   ├── api/              # 📚 API app <br>
│   │   ├── __init__.py   # Package marker <br>
│   │   ├── admin.py      # 🖥️ Admin interface config <br>
│   │   ├── apps.py       # ⚙️ App config <br>
│   │   ├── models.py     # 🗄️ Database models (Movie, Song, Quote, etc.) <br>
│   │   ├── serializers.py # 🔄 Data serialization for API <br>
│   │   ├── services.py   # 🛠️ Data loading and query logic <br>
│   │   ├── urls.py       # 🔗 API endpoint routing <br>
│   │   ├── views.py      # 🌐 API view handlers <br>
│   │   ├── data/         # 📊 Sample data <br>
│   │   │   ├── __init__.py <br>
│   │   │   └── sample_data.py # Hardcoded data for quotes, awards, songs <br>
│   │   └── management/   # 🛠️ Custom management commands <br>
│   │       ├── __init__.py <br>
│   │       └── commands/ <br>
│   │           ├── __init__.py <br>
│   │           └── load_tmdb_data.py # 📡 Load data from TMDb, samples <br>
├── media/                # 🎵 Storage for song audio files <br>
└── README.md             # 📜 You're here! <br>

---

## ⚙️ Installation

**Clone the Repo 📥**: <br>
```git clone https://gitlab.com/RoyTrina/srkverse-a-shah-rukh-khan-information-api.git``` <br>

```cd srkverse-a-shah-rukh-khan-information-api/SRKVerse``` <br>


**Set Up a Virtual Environment 🧪**:
```python -m venv venv```

On Windows:
```.\venv\Scripts\Activate.ps1```

✅ Success: Virtual environment activated!

**Install Dependencies 📦**: <br>
```pip install django djangorestframework requests python-dotenv```


**Configure Environment Variables 🔧**:

```Create SRKVerse/.env```: <br>
```SECRET_KEY=your-unique-secret-key``` <br>
```DEBUG=True``` <br>
```TMDB_API_KEY=your-tmdb-api-key``` <br>

Replace ```your-unique-secret-key``` with a secure key and ```your-tmdb-api-key``` with your TMDb API key (https://www.themoviedb.org/).

⚠️ Warning: Keep .env out of version control!

**Apply Migrations 🗄️**: <br>
```python manage.py makemigrations```
```python manage.py migrate```

✅ Success: Database schema created!

**Create a Superuser 👑**: <br>
```python manage.py createsuperuser```

**Load Initial Data 📚**:

Populate the database with TMDb movies and sample data: <br>
`python manage.py load_tmdb_data`

✅ Success: Data loaded for movies, songs, quotes, awards, and timeline!

---

## 📡 API Endpoints

| Method | Endpoint                        | Description                                 |
|--------|---------------------------------|---------------------------------------------|
| GET    |`/api/srk/movies/tmdb/`          | 🎬 Raw Shah Rukh Khan movie data from TMDb  |
| GET    |`/api/srk/movies/`               | 🎬 List all SRK movies in database          |
| GET    |`/api/srk/movies/year/<year>/`   | 🎬 Movies by release year                   |
| GET    |`/api/srk/movies/title/<title>/` | 🎬 Movie by title                           |
| GET    |`/api/srk/movies/top-rated/`     | 🎬 Top-rated SRK movies                     |
| GET    |`/api/srk/movies/genre/<genre>/` | 🎬 Movies by genre                          |
| GET    |`/api/srk/songs/`                | 🎵 List all SRK movie songs                 |
| GET    |`/api/srk/movies/<title>/songs/` | 🎵 Songs for a specific movie               |
| GET    |`/api/srk/quotes/`               | 💬 List all SRK quotes                      |
| GET    |`/api/srk/quotes/random/`        | 💬 Random SRK quote                         |
| GET    |`/api/srk/quotes/movie/<title>/` | 💬 Quotes by movie title                    |
| GET    |`/api/srk/quotes/tag/<tag>/`     | 💬 Quotes by tag (e.g., inspirational)      |
| GET    |`/api/srk/awards/`               | 🏆 List all SRK awards                      |
| GET    |`/api/srk/awards/year/<year>/`   | 🏆 Awards by year                           |
| GET    |`/api/srk/awards/type/<type>/`   | 🏆 Awards by type (e.g., Filmfare)          |
| GET    |`/api/srk/timeline/`             | 📅 SRK career milestones                    |
| GET    |`/api/srk/timeline/year/<year>/` | 📅 Timeline events by year                  |
| GET    |`/api/srk/timeline/debut/`       | 📅 SRK’s debut event                        |
| GET    |`/api/srk/votes/`                | ❤️ Fan votes for movies                     |
| POST   |`/api/srk/vote/`                 | ❤️ Vote for a favorite movie                |
| GET    |`/api/srk/quiz/`                 | ❓ Get a quiz question                       |
| POST   |`/api/srk/quiz/validate/`        | ❓ Validate a quiz answer                    |
| POST   |`/api/srk/fan-message/`          | ❤️ Submit a fan message                     |

---

## 📊 Sample JSON Data
**/api/srk/movies/** <br>
{ <br>
  "title": "My Name Is Khan", <br>
  "release_year": 2010, <br>
  "overview": "An Indian Muslim with Asperger’s syndrome embarks on a journey to meet the U.S. President.", <br>
  "rating": 7.9, <br>
  "genres": ["Drama", "Romance"], <br>
  "character": "Rizwan Khan", <br>
  "tmdb_id": 26022, <br>
  "poster_path": "/5Y36lmgVmbxJmN1jC8tiCkx6X1S.jpg" <br>
}

**/api/srk/songs/** <br>
{ <br>
  "title": "Tujh Mein Rab Dikhta Hai", <br>
  "movie": "Rab Ne Bana Di Jodi", <br>
  "audio_file": "/media/songs/tujh_mein_rab.mp3", <br>
  "composer": "Salim-Sulaiman", <br>
  "lyricist": "Jaideep Sahni", <br>
  "duration": "4:43" <br>
}

---

## 🛠️ Built With

🐍 [Django](https://www.djangoproject.com/) – Python web framework

🔄 [Django REST Framework](https://www.django-rest-framework.org/) – API toolkit

📡 [requests](https://requests.readthedocs.io/) – HTTP library for TMDb API

🌐 [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management

🗄️ [SQLite](https://www.sqlite.org/) – Default database ([PostgreSQL](https://www.postgresql.org/) recommended for production)

---

## 🔧 Extending the Project

**Custom Utilities 🛠️** :
- Add functions in api/utils/helpers.py:
   - api/utils/helpers.py <br>
	  - def format_song_data(songs):
	      - return [ <br>
	        - {
	           - "title": song.title,
	           - "movie": song.movie.title,
	           - "audio_url": song.audio_file.url if song.audio_file else "",
	           -  "composer": song.composer,
	           - "lyricist": song.lyricist,
	           - "duration": song.duration
	       -  }
	       -  for song in songs
	    ]
2. Import in api/views.py: <br>
`from .utils.helpers import format_song_data`
3. Frontend 📱: <br>
   1. Create templates with <audio> tags for song playback:
	<audio controls>
    <source src="{{ song.audio_file.url }}" type="audio/mpeg">
	    Your browser does not support the audio element.
	</audio>
4. External APIs 🌍: <br>
Integrate Spotify/YouTube APIs for song metadata (requires API keys).
5. Admin Interface 🖥️: <br>
o	Upload song audio files (MP3/WAV) at http://localhost:8000/admin/api/song/.

---

## 📝 Notes

- Data Sources 📊:
   - 🎬 Movies and song composers fetched from TMDb.
   - 💬 Quotes, 🏆 awards, 📅 timeline, and 🎵 song metadata from api/data/sample_data.py.
   - 🎧 Song audio files uploaded via admin interface.
   - Database 🗄️: SQLite by default; use PostgreSQL for better JSONField support.
   - Deployment 🚀: Consider AWS S3 for song storage and Gunicorn/Daphne for production.
   - Contributing 🤝: Submit issues or merge requests at [GitLab](https://gitlab.com/RoyTrina/srkverse-a-shah-rukh-khan-information-api).

---

##📌 License
This project is licensed under the [MIT License](https://gitlab.com/RoyTrina/srkverse-a-shah-rukh-khan-information-api/-/blob/727b2a608ca7c3eaca1a24e1c63ba5377c707d7f/LICENSE). 🌟 <br>
Data sourced from [The Movie Database (TMDb)](https://www.themoviedb.org/?language=en-GB) <br>
This fan-made, educational project is **not affiliated with Shah Rukh Khan or any official entity**. <br>

---

## 🙏 Acknowledgments
Special thanks to the SRK fan community for inspiration! 🌟 <br>
This is my version of a love letter to Shah Rukh Khan, the King of Bollywood and one of the greatest movie stars of all time! <br>
👑 Made with ❤️ by a fan.. 

