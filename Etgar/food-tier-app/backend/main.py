"""
API tier: FastAPI application that ties the frontend, the CSV data tier,
and the OpenAI external API together.

Endpoints:
    POST /api/food-tier         Classify a food (CSV cache, otherwise OpenAI).
    GET  /api/history/{food}    Look up a food in the CSV without calling OpenAI.
    GET  /health                Liveness check (used by docker-compose).

Run locally:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import food_storage
from openai_client import OpenAIClassificationError, classify

app = FastAPI(
    title="Food Tier API",
    description="Classifies foods into nutrition tiers A/B/C, with a CSV cache.",
    version="1.0.0",
)

# CORS: the frontend runs on http://localhost:8080 (nginx container) and we
# also allow 127.0.0.1 because some browsers treat the two as different
# origins. `allow_origins=["*"]` would also work but being explicit is a
# good teaching point.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        # Handy when a student opens index.html directly from disk.
        "null",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- Pydantic models (request / response contracts) ----------------------


class FoodRequest(BaseModel):
    """Body for POST /api/food-tier."""

    food: str = Field(..., min_length=1, max_length=100, examples=["egg"])


class FoodTierResponse(BaseModel):
    food: str
    tier: str
    explanation: str
    source: str  # "csv" or "openai"


class HistoryHit(BaseModel):
    exists: bool
    food: str
    tier: str
    explanation: str


class HistoryMiss(BaseModel):
    exists: bool
    food: str


# ----- Lifecycle -----------------------------------------------------------


@app.on_event("startup")
def _startup() -> None:
    """Make sure the CSV (with its header row) exists before serving traffic."""
    food_storage.ensure_csv_exists()


# ----- Routes --------------------------------------------------------------


@app.get("/health")
def health() -> dict:
    """Cheap liveness probe — used by docker-compose / monitoring tools."""
    return {"status": "ok"}


@app.post("/api/food-tier", response_model=FoodTierResponse)
def post_food_tier(req: FoodRequest) -> FoodTierResponse:
    """Classify a food.

    Flow:
        1. Look up the (normalized) food in the CSV.
        2. If found, return it with `source="csv"` (no OpenAI call).
        3. Otherwise call OpenAI, validate the response, save it to the
           CSV and return it with `source="openai"`.
    """
    food = req.food.strip()
    if not food:
        raise HTTPException(status_code=400, detail="Food name cannot be empty.")

    cached = food_storage.find(food)
    if cached is not None:
        return FoodTierResponse(
            food=cached["food"],
            tier=cached["tier"],
            explanation=cached["explanation"],
            source="csv",
        )

    try:
        tier, explanation = classify(food)
    except OpenAIClassificationError as exc:
        # 502 == we are an upstream-dependent service and the upstream
        # (OpenAI) failed us. The message is safe and student-friendly.
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    saved = food_storage.save(food, tier, explanation)
    return FoodTierResponse(
        food=saved["food"],
        tier=saved["tier"],
        explanation=saved["explanation"],
        source="openai",
    )


@app.get("/api/history/{food}")
def get_history(food: str) -> dict:
    """Look up a food in the CSV without ever calling OpenAI.

    Returns either:
        {"exists": true,  "food": ..., "tier": ..., "explanation": ...}
        {"exists": false, "food": ...}
    """
    normalized = food_storage.normalize(food)
    hit = food_storage.find(food)
    if hit is None:
        return {"exists": False, "food": normalized}
    return {
        "exists": True,
        "food": hit["food"],
        "tier": hit["tier"],
        "explanation": hit["explanation"],
    }
