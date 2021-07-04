from typing import Optional
from pydantic import BaseModel, validator, constr
from datetime import datetime
import validators


class UrlSchema(BaseModel):
    long_url: str
    customCode: Optional[constr(max_length=8)] = None

    @validator("long_url")
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Long URL is invalid.")
        return v
