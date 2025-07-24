from fastapi import FastAPI

from app.api.test.routes import router as api_router
from app.core.api import lifespan_factory

app = FastAPI(lifespan=lifespan_factory("app/api/test"))
app.include_router(api_router)

