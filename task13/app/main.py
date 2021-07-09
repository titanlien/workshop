import os, logging

from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from decouple import config
from starlette.responses import RedirectResponse

import logging
from . import crud, models
from .schemas import UrlSchema
from .database import SessionLocal, engine

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/{short_code}/graph")
async def get_short_url_hostory(short_code: str, db: Session = Depends(get_db)):
    # Query the database for the document that matches the short_code from the path param
    db_url_history = crud.get_short_history_by_short_code(db, short_code=short_code)
    # 404 ERROR if no url is found
    if not db_url_history:
        raise HTTPException(status_code=404, detail="URL not found !")
    else:
        return db_url_history


@app.get("/{short_code}/stats")
async def get_url_status(short_code: str, db: Session = Depends(get_db)):
    # Query the database for the document that matches the short_code from the path param
    db_url = crud.get_url_by_short_code(db, short_code=short_code)
    # 404 ERROR if no url is found
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found !")
    else:
        return db_url.__dict__


@app.get("/{short_code}/")
async def redirect_url(short_code: str, db: Session = Depends(get_db)):
    # Query the database for the document that matches the short_code from the path param
    db_url = crud.get_url_by_short_code(db, short_code=short_code)
    # 404 ERROR if no url is found
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found !")
    else:
        # Increment visitor count by 1
        db_url.visit_counter += 1
        crud.constrcut_url_history(db, url_id=db_url.id)
        db.commit()
        # Redirect to the long_url
        response = RedirectResponse(db_url.long_url)
        return response


@app.post("/add_url/", response_model=dict, status_code=201)
async def create_url(url: UrlSchema, db: Session = Depends(get_db)):
    db_long_url = crud.get_url_by_long_url(db, long_url=url.long_url)
    if db_long_url:
        raise HTTPException(status_code=400, detail="URL already created")
    ret = crud.create_url(db=db, url=url)
    if ret is None:
        raise HTTPException(status_code=400, detail="URL can't be created")
    return {"url": os.path.join(config("BASE_URL"), ret.short_code)}
