from typing import Optional, List, Dict
from pydantic import BaseModel, Field

# Pagination models for JSON API
class PageParams(BaseModel):
    number: int = 1
    size: int = 100

class JsonApiLinks(BaseModel):
    first: Optional[str] = None
    next: Optional[str] = None
    prev: Optional[str] = None
    last: Optional[str] = None
