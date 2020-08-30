import logging
import os
from fastapi import FastAPI

ENDPOINT_GET_TREE = "/tree"

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger("DevOps")

app = FastAPI(title="DevOps task", description="return a json object.")


@app.get(ENDPOINT_GET_TREE)
async def get_tree():
    logger.debug(f"Called {ENDPOINT_GET_TREE}")
    return {"myFavouriteTree": "Cypress"}
