from fastapi import APIRouter

from routes import memory as memory_routes
from routes import scheduler as scheduler_routes

router = APIRouter()


@router.get('/health')
def health():
    return {'status': 'ok'}


router.include_router(memory_routes.router)
router.include_router(scheduler_routes.router)
