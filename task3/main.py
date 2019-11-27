import logging
import os
from fastapi import FastAPI

ENDPOINT_GET_MESSAGE = "/"

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger("DevOps")

app = FastAPI(title="DevOps task", description="return a json object.")


@app.get(ENDPOINT_GET_MESSAGE)
async def get_message():
    logger.debug(f"Called {ENDPOINT_GET_MESSAGE}")
    return {"id": "1", "message": "Hello world"}
