import logging
import os
import requests
from fastapi import FastAPI

ENDPOINT_RETURN_MESSAGE = "/"
API_ENDPOINT = "http://webapp-1/"

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger("DevOps")

app = FastAPI(title="webapp 2", description="return a json object.")


@app.get(ENDPOINT_RETURN_MESSAGE)
async def get_message():
    logger.debug(f"Called web-1 /")
    r = requests.get(url = API_ENDPOINT)
    data = r.json()
    return {"id": "1", "message": data['message'][::-1]}
