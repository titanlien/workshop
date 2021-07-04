from sqlalchemy import Column, Integer, String, Date

from .database import Base


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(Date, unique=True, index=False)
    long_url = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)
    last_access_date = Column(Date, unique=True, index=False)
    visit_times = Column(Integer, default=0)
