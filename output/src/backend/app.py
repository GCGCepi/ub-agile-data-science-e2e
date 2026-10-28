import os
from typing import List

import mlflow.sklearn
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

app = FastAPI(title="Minimal MLflow + FastAPI", version="0.1.0")

model = None


class PredictRequest(BaseModel):
    features: List[float]


class PredictResponse(BaseModel):
    predicted_class: int
    probability: float


@app.on_event("startup")
def load_model() -> None:
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("Model not found. Run the training script first: python train.py")
    model = mlflow.sklearn.load_model(MODEL_PATH)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    if len(request.features) != 4:
        raise HTTPException(status_code=422, detail="Expected 4 features")
    try:
        x = np.array(request.features, dtype=float).reshape(1, -1)
        probability = float(model.predict_proba(x)[0, 1])
        predicted_class = int(model.predict(x)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {e}")
    return PredictResponse(predicted_class=predicted_class, probability=probability)
