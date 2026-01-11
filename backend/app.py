from fastapi import FastAPI
from .main import router

app = FastAPI(title="ReMind API")
app.include_router(router)
