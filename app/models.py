import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .database import Base


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(
        DateTime(timezone=True), unique=True, index=False, server_default=func.now()
    )
    long_url = Column(String, unique=True, index=True)
    short_code = Column(String, unique=True, index=True)
    last_access_date = Column(
        DateTime(timezone=True), unique=True, index=False, onupdate=func.now()
    )
    visit_counter = Column(Integer, default=0)

    history = relationship("short_url_history", back_populates="url")

class short_url_history(Base):
    __tablename__ = "short_url_history"
    
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey(Url.id))
    access_date = Column(
        DateTime(timezone=True), unique=True, index=False, server_default=func.now()
    )

    url = relationship("Url", back_populates="history")
