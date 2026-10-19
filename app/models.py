
from sqlalchemy.orm import relationship 
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, Nullable, String, Boolean, null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, primary_key= False, nullable = False, unique=True)
    password = Column (String, primary_key=False, nullable=False)
    created_at = Column (TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))

class Entry(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, primary_key= False, nullable=False)
    kind = Column(String, primary_key=False, nullable=False)
    status = Column(String, primary_key= False, nullable= False)
    user_id = Column(Integer, ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False)
    rating = Column (Integer, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)
    tmdb_id = Column(Integer, nullable=True)
  



