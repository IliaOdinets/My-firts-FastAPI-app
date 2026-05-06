# main.py
from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI(
    title="My First API",
    description="Learning FastAPI step by step",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем роутеры
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "version": "0.1.0"}