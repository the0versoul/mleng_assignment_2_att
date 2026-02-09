#!/usr/bin/env python3
"""
Headline sentiment scoring API.

Serves the same SVM + transformer setup from assignment 1 as a web service.
Models are loaded once at startup so we don't have to do it on every request.
"""

import logging
import os
from pathlib import Path
from typing import List

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# paths and config
# ---------------------------------------------------------------------------

# Model lives in the same folder as this script (relative path so it works on server)
_SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_PATH = os.environ.get("HEADLINE_MODEL_PATH", str(_SCRIPT_DIR / "svm.joblib"))
LOCAL_TRANSFORMER_PATH = "/opt/huggingface_models/all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# model loading (once at startup)
# ---------------------------------------------------------------------------

class ModelStore:
    """Holds the classifier and transformer so we load them once."""

    def __init__(self):
        self.classifier = None
        self.transformer_model = None

    def load(self):
        if not os.path.exists(MODEL_PATH):
            logger.critical("Model file not found: %s", MODEL_PATH)
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

        logger.info("Loading classifier from %s", MODEL_PATH)
        self.classifier = joblib.load(MODEL_PATH)

        if os.path.exists(LOCAL_TRANSFORMER_PATH):
            logger.info("Using local transformer at %s", LOCAL_TRANSFORMER_PATH)
            self.transformer_model = SentenceTransformer(LOCAL_TRANSFORMER_PATH)
        else:
            logger.info("Loading default transformer (all-MiniLM-L6-v2)")
            self.transformer_model = SentenceTransformer("all-MiniLM-L6-v2")

    def score(self, headlines):
        if not headlines:
            return []
        embeddings = self.transformer_model.encode(headlines)
        labels = self.classifier.predict(embeddings)
        return list(labels)


model_store = ModelStore()

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Headline Sentiment API",
    description="Score headlines and return sentiment labels only (client stitches back with text).",
)


@app.on_event("startup")
def startup():
    """Load models once when the service starts."""
    try:
        model_store.load()
    except FileNotFoundError as e:
        logger.error("Startup failed: %s", e)
        raise
    except Exception as e:
        logger.critical("Unexpected error during model load: %s", e)
        raise


# ---------------------------------------------------------------------------
# request/response schemas
# ---------------------------------------------------------------------------

class HeadlinesRequest(BaseModel):
    """POST body: list of headline strings."""

    headlines: List[str]


# ---------------------------------------------------------------------------
# endpoints
# ---------------------------------------------------------------------------

@app.get("/status")
def status():
    """
    Health check. Returns OK so we can confirm the service is up.
    """
    return JSONResponse(content={"status": "OK"})


@app.post("/score_headlines")
def score_headlines(request: HeadlinesRequest):
    """
    Score a list of headlines. Returns only the labels in order; client is
    responsible for matching them back to the original headlines.
    """
    headlines = request.headlines
    logger.info("score_headlines request: %d headlines", len(headlines))

    if not isinstance(headlines, list):
        logger.warning("Invalid request: headlines is not a list")
        raise HTTPException(status_code=400, detail="headlines must be a list")

    # allow non-string entries but coerce to string for the model
    try:
        text_list = [str(h).strip() for h in headlines]
    except Exception as e:
        logger.warning("Failed to convert headlines to strings: %s", e)
        raise HTTPException(status_code=400, detail="headlines must be convertible to strings") from e

    try:
        labels = model_store.score(text_list)
    except Exception as e:
        logger.error("Scoring failed: %s", e)
        raise HTTPException(status_code=500, detail="Scoring failed") from e

    return JSONResponse(content={"labels": labels})


# ---------------------------------------------------------------------------
# run with: uvicorn score_headlines_api:app --host 0.0.0.0 --port 8088  (port 8088 = alextsourmas)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "score_headlines_api:app",
        host="0.0.0.0",
        port=8088,
        reload=False,
    )
