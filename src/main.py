from fastapi import FastAPI

from src.modules.spiders.entrypoints.api.spider_routes import router as scraper_router

app = FastAPI()
app.include_router(scraper_router)
