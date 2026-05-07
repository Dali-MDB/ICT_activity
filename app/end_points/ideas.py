from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.db import SessionDep
from app.models import User, Idea
from app.schemas import UserDisplay, UserCreate, IdeaCreate, IdeaDisplay
from app.auth import current_user
from app.models import VoteType

# Create a router instance
router = APIRouter(
    prefix="/ideas",           # All routes will start with /users
    tags=["ideas"],            # Group in documentation
    responses={404: {"description": "Not found"}}  # Common responses
)

ideas_router = router

@router.get('', response_model=List[IdeaDisplay])
async def get_all_ideas(db:SessionDep):
    ideas = db.query(Idea).all()   
    ideas = sorted(
        ideas,
        key=lambda x: sum(1 for t in x.thumbs if t.type == VoteType.UP) 
                    - sum(1 for t in x.thumbs if t.type == VoteType.DOWN),
        reverse=True  
    )
    return ideas



@router.get('/{idea_id}', response_model=IdeaDisplay)
async def get_idea(idea_id:int , db:SessionDep):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.post('/new', response_model=IdeaDisplay, status_code=status.HTTP_201_CREATED)
async def new_idea( new_idea : IdeaCreate ,user: Annotated[User, Depends(current_user)], db:SessionDep):
    idea = Idea(**new_idea.model_dump(), user_id=user.id)
    try:
        db.add(idea)
        db.commit()
        db.refresh(idea)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return idea


@router.delete('/{idea_id}/delete')
async def delete_idea(idea_id:int , user: Annotated[User, Depends(current_user)], db:SessionDep):
    #fetch the idea
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.user_id != user.id:   #check if the user is the owner of the idea
        raise HTTPException(status_code=403, detail="You are not the owner of this idea")
    try:
        db.delete(idea)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return {"message": "Idea deleted successfully"}
