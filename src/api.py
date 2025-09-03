from fastapi import FastAPI
from src.api_routes import predict, health

app = FastAPI(
    title="Football Prediction API",
    description="API for football match predictions",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(predict.router)
