from fastapi import FastAPI
from backend.routes import memory as memory_routes
from backend.routes import scheduler as scheduler_routes

app = FastAPI(title="ReMind Backend")

# Include routers
app.include_router(memory_routes.router)
app.include_router(scheduler_routes.router)

@app.get("/")
def root():
    return {"message": "ReMind backend is running!"}


@app.get('/health')
def health():
    return {'status': 'ok'}
