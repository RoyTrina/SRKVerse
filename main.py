from fastapi import FastAPI
from routes import shah_rukh_khan_router


app = FastAPI(title='SRKverse API', version="1.0")

app.include_router(shah_rukh_khan_router, prefix="/srk")