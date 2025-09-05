from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
import os
import json

router = APIRouter()


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


@router.get("/predictions", tags=["Predictions"])
def get_predictions(request: Request):
    """Get all predictions"""
    return request.app.state.predictions


@router.get(
    "/predictions/{match_id}", tags=["Predictions"], summary="Get prediction for a specific match"
)
def get_prediction_by_id(match_id: int, request: Request):
    """Get prediction for a specific match by match_id"""
    for match in request.app.state.predictions:
        if str(match.get("match_id")) == str(match_id):
            return match
    raise HTTPException(status_code=404, detail="Prediction for this match_id not found.")


@router.get("/stats", response_class=Response)
def get_prediction_stats():
    stats_path = os.path.join("data", "stats", "prediction_stats.json")
    try:
        with open(stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
        return Response(content=json.dumps(stats), media_type="application/json")
    except Exception as e:
        return Response(
            content=json.dumps({"error": str(e)}), media_type="application/json", status_code=500
        )
