from fastapi import FastAPI

from src.lib.spiders.entrypoints.api.spider_routes import router as scraper_router

app = FastAPI()
app.include_router(scraper_router)
