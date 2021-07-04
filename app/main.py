import os, logging

from typing import List
from sqlalchemy.orm import Session
from fastapi import Body, FastAPI, HTTPException, Query, Depends
from decouple import config

import logging
from . import crud, models
from .schemas import UrlSchema
from .database import SessionLocal, engine

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.get_users(db, skip=skip, limit=limit)
#    return users


@app.post("/add_url/", response_model=dict, status_code=201)
async def create_url(url: UrlSchema, db: Session = Depends(get_db)):
    db_long_url = crud.get_url_by_long_url(db, long_url=url.long_url)
    if db_long_url:
        raise HTTPException(status_code=400, detail="URL already created")
    ret = crud.create_url(db=db, long_url=url.long_url)
    if ret is None:
        raise HTTPException(status_code=400, detail="URL can't be created")
    return {"url": os.path.join(config("BASE_URL"), ret.short_code)}
