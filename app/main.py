import sqlite3
import short_url as shurl

#from urlparse import urlparse
from fastapi import Body, FastAPI, HTTPException, Query
from sqlite3 import OperationalError

app = FastAPI()
