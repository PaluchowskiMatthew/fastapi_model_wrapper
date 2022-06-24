from unittest import TestCase
from urllib import response
from fastapi import FastAPI
import json
import logging
import uuid
import pandas as pd

# Define global variables
SERVICE_NAME = "Test Model API"
MODEL_ARTIFACT_PATH = "./model_artifacts"

# Initialize the FastAPI app
app = FastAPI(title=SERVICE_NAME, docs_url="/")

# Configure logger
log = logging.getLogger("uvicorn")
log.setLevel(logging.INFO)


@app.on_event("startup")
async def startup_load_model():
    global MODEL
    # MODEL = load_model(MODEL_ARTIFACT_PATH)

@app.get("/test")
async def read_main():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(data: str):
    # Parse data
    input_df = pd.DataFrame(json.load(data))

    # Define UUID for the request
    request_id = uuid.uuid4().hex

    # Log input data
    log.info(json.dumps({
        "service_name": SERVICE_NAME,
        "type": "InputData",
        "request_id": request_id,
        "data": input_df.to_json(orient='records'),
    }))

    # Make predictions and log
    # model_output = MODEL.predict(input_df)
    model_output = {
        # "model_version": MODEL.version
        "model_version": "1.0.0",
        "inference": {
            "doc_1": ["War Exclusion"],
            "doc_2": ["Cyber", "War Exclusion"]
        }
    }

    # Log output data
    log.info(json.dumps({
        "service_name": SERVICE_NAME,
        "type": "OutputData",
        "request_id": request_id,
        "data": model_output
    }))

    # Make response payload
    response_payload = json.dumps(model_output)

    return response_payload