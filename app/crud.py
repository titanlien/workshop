import logging, os
import shortuuid

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


from . import models, schemas

logger = logging.getLogger(__name__)

def get_url_by_id(db: Session, url_id: int):

    return db.query(models.Url).filter(models.Url.id == url_id).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Url).offset(skip).limit(limit).all()


def get_url_by_short_code(db: Session, short_code: str):

    return db.query(models.Url).filter(models.Url.short_code == short_code).first()


def get_url_by_long_url(db: Session, long_url: str):
    try:
        return db.query(models.Url).filter(models.Url.long_url == long_url).first()
    except NoResultFound as err:
        logger.info(f"err: {err}")
    return None

def create_url(db: Session, long_url: str):
    short_code = shortuuid.ShortUUID().random(length = 8)
    db_url = models.Url(long_url=long_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
