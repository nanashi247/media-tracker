from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import DATETIME
from enum import Enum



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config():
        from_attributes: True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int


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
    episode: Optional[int] = None
    season: Optional[int] = None


class EntryCreate(EntryBase):
    tmdb_id: Optional[int] = None
    pass

class EntryUpdate(BaseModel):
    title: Optional[str] = None
    kind: Optional[EntryKind] = None
    status: Optional[EntryStatus] = None
    rating: Optional[float] = None
    notes: Optional[str] = None
    class Config():
        from_attributes = True

class EntryCreateTMDB(BaseModel):
    tmdb_id: int
    title: str
    kind: EntryKind
    status: EntryStatus = EntryStatus.watchlist
    rating: Optional[float] = None
    notes: Optional[str] = None

class TagOut(BaseModel):
    id: int
    name: str
    class Config():
        from_attributes = True

class EntryOut(EntryBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    tags: list[TagOut] = []