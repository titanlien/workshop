#import short_url as shurl

from sqlalchemy.orm import Session

from . import models, schemas


def get_url_by_id(db: Session, url_id: int):

    return db.query(models.Url).filter(models.Url.id == url_id).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Url).offset(skip).limit(limit).all()


def get_url_by_short_url(db: Session, short_url: str):

    return db.query(models.Url).filter(models.Url.short_url == short_url).first()


def get_url_by_long_url(db: Session, long_url: str):

    return db.query(models.Url).filter(models.Url.long_url == long_url).first()


def create_url(db: Session, long_url: str):
    #short_url = shurl.encode_url(long_url)
    db_url = models.Url(long_url=long_url, short_url=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
