from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.models import VoteType
from pydantic import computed_field

class UserBase(BaseModel):
    username : str
    email : str
    

class UserCreate(UserBase):
    password : str


class UserDisplay(UserBase):
    id : int

    model_config = ConfigDict(from_attributes=True) 
    

class User(UserDisplay):
    model_config = ConfigDict(from_attributes=True) 


class ThumbDisplay(BaseModel):
    id: int
    user_id: int
    idea_id: int
    type: VoteType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class IdeaCreate(BaseModel):
    concept : str


class IdeaDisplay(IdeaCreate):
    id : int
    created_at : datetime
    user : Optional[User] = None
    thumbs : List[ThumbDisplay] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True) 

    @computed_field
    @property
    def thumbs_up(self) -> int:
        return sum(1 for t in self.thumbs if t.type == VoteType.UP)

    @computed_field
    @property
    def thumbs_down(self) -> int:
        return sum(1 for t in self.thumbs if t.type == VoteType.DOWN)
    