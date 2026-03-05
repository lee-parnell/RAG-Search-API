from fastapi import FastAPI
from .core.config import get_settings
from.api.v1 import search

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(search.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

