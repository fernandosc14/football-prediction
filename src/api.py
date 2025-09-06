from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_routes import predict, health
from contextlib import asynccontextmanager

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
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(predict.router)
