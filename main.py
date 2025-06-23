from fastapi import FastAPI
from routes import Shah_Rukh_Khan_router


app = FastAPI(title="SRKverse API", version="1.0")

app.include_router(Shah_Rukh_Khan_router, prefix="/srk")