from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import DATETIME
from enum import Enum


# USER SCHEMAS

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config():
        from_attributes: True





# TOKEN SCHEMAS

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int





# ENTRY SCHEMAS

class EntryKind(str, Enum):
    movie = "movie"
    show = "show"

class EntryStatus(str, Enum):
    watching = "watching"
    completed = "completed"
    dropped = "dropped"
    watchlist = "watchlist"


class EntryBase(BaseModel):
    title: str
    kind: EntryKind
    status: EntryStatus
    rating: Optional[float] = None
    notes: Optional[str] = None

class EntryCreate(EntryBase):
    pass

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    kind: Optional[EntryKind] = None
    status: Optional[EntryStatus] = None
    rating: Optional[float] = None
    notes: Optional[str] = None


class EntryOut(EntryBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    class Config():
        from_attributes = True



