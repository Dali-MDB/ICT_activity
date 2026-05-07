from sqlalchemy import Table, Column, Integer, String,  Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime , timezone
import enum
from .db import Base
from sqlalchemy import Enum


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)

    #relationships
    ideas = relationship("Idea", back_populates="user")
    thumbs = relationship("Thumb", back_populates="user")
   

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    concept = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    #foreign_key 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False )

    #relationships
    user = relationship(User, back_populates="ideas")
    thumbs = relationship("Thumb", back_populates="idea")


class VoteType(enum.Enum):
    UP = "up"
    DOWN = "down"


class Thumb(Base):
    __tablename__ = "thumbs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)

    type = Column(Enum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    #relationships 
    user = relationship("User", back_populates="thumbs")
    idea = relationship("Idea", back_populates="thumbs")

