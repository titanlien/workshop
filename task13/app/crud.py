import logging, os
import shortuuid

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


from . import models, schemas

logger = logging.getLogger(__name__)


def get_url_by_short_code(db: Session, short_code: str):

    return db.query(models.Url).filter(models.Url.short_code == short_code).first()


def get_url_by_long_url(db: Session, long_url: str):
    try:
        return db.query(models.Url).filter(models.Url.long_url == long_url).first()
    except NoResultFound as err:
        logger.error(f"{err}")
    return None


def create_url(db: Session, url: schemas.UrlSchema):
    long_url = url.long_url
    if url.customCode:
        short_code = url.customCode
    else:
        short_code = shortuuid.ShortUUID().random(length=8)
    db_url = models.Url(long_url=long_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def constrcut_url_history(db: Session, url_id: int):

    return db.add(models.short_url_history(url_id=url_id))


def get_short_history_by_short_code(db: Session, short_code: str):
    history = (
        db.query(models.short_url_history)
        .join(models.Url, models.short_url_history.url_id == models.Url.id)
        .filter(models.Url.short_code == short_code)
        .all()
    )
    return [access_date.access_date for access_date in history]
