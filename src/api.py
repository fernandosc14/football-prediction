from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api_routes import health, predict

import os
import json


PREDICTIONS_PATH = os.path.abspath(os.getenv("PREDICTIONS_PATH", "data/predict/predictions.json"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with open(PREDICTIONS_PATH, encoding="utf-8") as f:
            app.state.predictions = json.load(f)
    except FileNotFoundError:
        app.state.predictions = []
    yield


app = FastAPI(
    title="Football Prediction API",
    description="API for football match predictions",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://football-prediction-murex.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)

app.include_router(health.router)
app.include_router(predict.router)
