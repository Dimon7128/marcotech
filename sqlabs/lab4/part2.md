
### LAB 2  |  Predict spam or ham

**15 minutes  |  After teaching Slide 18**

**Goal:** Connect FastAPI to the saved model and see both a prediction and a validation error.

1.  Replace main.py with the complete implementation below. Notice that model.joblib is loaded once as the application starts.

```python
from pathlib import Path
from typing import Annotated

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

app = FastAPI(title="SMS Classifier")
pipeline = joblib.load(Path(__file__).with_name("model.joblib"))

class SMSRequest(BaseModel):
    message: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=1
    )]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: SMSRequest):
    label = str(pipeline.predict([payload.message])[0])
    return {"label": label}
```

2.  Save the file. With --reload, Uvicorn restarts automatically; otherwise stop and run it again. Look for startup errors in the terminal.

3.  Open http://127.0.0.1:8000/docs. Select POST /predict → Try it out, enter the request below, and click Execute.

```json
{"message": "Free prize today"}
```

4.  Record the HTTP status code and predicted label. The label can be spam or ham; its exact value is not guaranteed.

5.  Repeat with two invalid requests, one at a time:

```json
{"message": ""}
{"message": "   "}
```

> **CHECK:** Valid SMS → HTTP 200 with {"label":"spam"} or {"label":"ham"}. Both invalid inputs → HTTP 422.

> **Why it works:** Pydantic validates the message; strip_whitespace removes spaces, and min_length=1 rejects an empty result. The whole fitted pipeline performs TF-IDF and classification.

> **Think about it:** Does making a prediction train the model again? What part of the code proves your answer?

## Part 4  |  Docker checkpoints

> Continue with the same sms-service/ folder. Do not change the model or retrain it.

