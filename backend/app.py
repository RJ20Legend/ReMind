from fastapi import FastAPI
from .main import router
from .database import create_tables

app = FastAPI(title="ReMind API")
app.include_router(router)

# ensure tables exist on startup
create_tables()
