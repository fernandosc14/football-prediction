from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException

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
def get_predictions():
    """Get all predictions"""
    try:
        with open("data/predict/predictions.json", encoding="utf-8") as f:
            predictions = json.load(f)
        return predictions
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Predictions file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading predictions file: {e}")


@router.get(
    "/predictions/{match_id}", tags=["Predictions"], summary="Get prediction for a specific match"
)
def get_prediction_by_id(match_id: int):
    """Get prediction for a specific match by match_id"""
    try:
        with open("data/predict/predictions.json", encoding="utf-8") as f:
            predictions = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Predictions file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading predictions file: {e}")

    for match in predictions:
        if match.get("match_id") == match_id:
            return match
    raise HTTPException(status_code=404, detail="Prediction for this match_id not found.")
