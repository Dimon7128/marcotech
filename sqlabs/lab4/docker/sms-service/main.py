from pathlib import Path
from typing import Annotated

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

app = FastAPI(title="SMS Classifier")
pipeline = joblib.load(Path(__file__).with_name("model.joblib"))

class SMSRequest(BaseModel):
    message: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=2
    )]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: SMSRequest):
    label = str(pipeline.predict([payload.message])[0])
    return {"label": label}