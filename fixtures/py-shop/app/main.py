"""FastAPI application entry point."""
from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="py-shop")
app.include_router(router)
