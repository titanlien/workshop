import logging, os
import shortuuid

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from decouple import config

from . import models, schemas

logger = logging.getLogger(__name__)

def get_url_by_id(db: Session, url_id: int):

    return db.query(models.Url).filter(models.Url.id == url_id).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Url).offset(skip).limit(limit).all()


def get_url_by_short_url(db: Session, short_url: str):

    return db.query(models.Url).filter(models.Url.short_url == short_url).first()


def get_url_by_long_url(db: Session, long_url: str):
    try:
        return db.query(models.Url).filter(models.Url.long_url == long_url).first()
    except NoResultFound as err:
        logger.info(f"err: {err}")
    return None

def create_url(db: Session, long_url: str):
    shortCode = shortuuid.ShortUUID().random(length = 8)
    short_url = os.path.join(config("BASE_URL"), shortCode)
    db_url = models.Url(long_url=long_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
