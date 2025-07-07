# 🎬 SRKverse – A Shah Rukh Khan Information API

Welcome to the **SRKverse API** –
a RESTful API built with **FastAPI** that celebrates the legacy of Bollywood icon **Shah Rukh Khan**.

This project provides structured access to Shah Rukh Khan's biography, films, famous quotes, and more.
Great for fan apps, trivia games, film databases, and Bollywood data mashups.

---

## 🚀 Features

- 📜 **Biography** – Learn about SRK's journey and legacy
- 🎞️ **Movies** – Browse key films with metadata
- 🗣️ **Quotes** – Iconic quotes from memorable films
- 🎯 **Random Quote** – Get a surprise SRK dialogue
- 🏆 *(Planned)*: Awards, timeline, trivia, polls, and more!

---

## 📁 Project Structure

srkverse-a-shah-rukh-khan-information-api/ <br>
├── manage.py  <br>
├── srkverse_api/ <br>
│   ├── __init__.py <br>
│   ├── settings.py <br>
│   ├── urls.py <br>
│   ├── wsgi.py <br>
│   └── asgi.py <br>
├── SRKVerse/ <br>
│   ├── api/ <br>
│   │   ├── __init__.py <br>
│   │   ├── admin.py <br>
│   │   ├── apps.py <br>
│   │   ├── models.py <br>
│   │   ├── serializers.py <br>
│   │   ├── services.py <br>
│   │   ├── urls.py <br>
│   │   ├── views.py <br>
│   │   └── management/ <br>
│   │       ├── __init__.py <br>
│   │       └── commands/ <br>
│   │           ├── __init__.py <br>
│   │           └── load_tmdb_data.py <br>
├── media/ <br>
└── .env <br>
| README.md #You're here!

## ⚙️ Installation

1. **Clone the repo**:
    ```bash git clone https://gitlab.com/RoyTrina/srkverse-api.git 
    cd srkverse-api```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows the second line becomes: ```venv\Scripts\activate```
   <br>
   <br>
3. Install dependencies
   ```pip install -r requirements.txt```
   <br>
   <br>
4. Run the server:
   ```uvicorn app.main:app --reload```

## 📡 API Endpoints

| Method | Endpoint            | Description                |
|--------|---------------------|----------------------------|
| GET    | `/srk/bio`          | Returns SRK's biography    |
| GET    | `/srk/movies`       | List of popular SRK movies |
| GET    | `/srk/random-quote` | Get a random SRK quote     |

## 📊 Sample JSON Data (/srk/movies)

{ <br>
"title": "My Name Is Khan", <br>
"year": 2010, <br>
"director": "Karan Johar", <br>
"genres": ["Drama", "Romance"], <br>
"plot": "An Indian Muslim with Asperger’s syndrome embarks on a journey to meet the U.S. President."
<br>
}

## 🛠️ Built With

1. [FastAPI](https://fastapi.tiangolo.com/) – Modern Python web framework

2. [Uvicorn](https://www.uvicorn.org/) – ASGI server

3. [Pydantic](https://docs.pydantic.dev/) – Data parsing and validation

## 📌 License

This project is licensed under the [MIT Licence](LICENSE).
This is a fan-made, educational project is **not affiliated with Shah Rukh Khan** or any official entity.

## 🙏 Acknowledgments

This is my version of a love letter to Shah Rukh Khan, one of the greatest movie stars of all time 🌟

Data and ideas partially derived from [The Movie Database (TMDb)](https://www.themoviedb.org/)

## 👑 Made with ❤️ for the King of Bollywood from a fan