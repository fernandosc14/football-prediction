from fastapi import APIRouter, Request, Response, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

import os
import json
import config

router = APIRouter()

ENDPOINT_API_KEY = os.environ.get("ENDPOINT_API_KEY")


class Odds(BaseModel):
    home: float
    draw: float
    away: float


class MatchInput(BaseModel):
    match_id: int
    date: str
    time: str
    league: str
    home_team: str
    away_team: str
    odds: Optional[Odds] = None


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != ENDPOINT_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/predictions", tags=["Predictions"], dependencies=[Depends(verify_api_key)])
def get_predictions(request: Request):
    """Get all predictions"""
    return request.app.state.predictions


@router.get(
    "/predictions/{match_id}",
    tags=["Predictions"],
    summary="Get prediction for a specific match",
    dependencies=[Depends(verify_api_key)],
)
def get_prediction_by_id(match_id: int, request: Request):
    """Get prediction for a specific match by match_id"""
    for match in request.app.state.predictions:
        if str(match.get("match_id")) == str(match_id):
            return match
    raise HTTPException(status_code=404, detail="Prediction for this match_id not found.")


@router.get("/stats", response_class=Response, dependencies=[Depends(verify_api_key)])
def get_prediction_stats():
    stats_path = os.path.join("data", "stats", "prediction_stats.json")
    try:
        with open(stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
        return Response(content=json.dumps(stats), media_type="application/json")
    except FileNotFoundError:
        return Response(
            content=json.dumps({"error": "Stats file not found"}),
            media_type="application/json",
            status_code=404,
        )
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}), media_type="application/json", status_code=500
        )


@router.get("/meta/last-update", dependencies=[Depends(verify_api_key)])
def get_last_update():
    timestamp = config.redis_client.get(config.LAST_UPDATE_KEY)
    if timestamp is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {"last_update": timestamp.decode("utf-8")}
