from fastapi import APIRouter,Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from typing import Annotated
from app.db import SessionDep
from app.models import User, Idea, Thumb
from app.schemas import IdeaDisplay
from app.auth import current_user
from app.models import VoteType


router = APIRouter(
    prefix="/thumbs",
    tags=["thumbs"],
    responses={404: {"description": "Not found"}}
)

thumbs_router = router
#add a thumb to an idea
@router.post('/{idea_id}/add_thumb', response_model=IdeaDisplay)  
async def add_thumb(idea_id:int , new_thumb_type: VoteType, user: Annotated[User, Depends(current_user)], db:SessionDep):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    #check if the user has already added a thumb to the idea
    thumb = db.query(Thumb).filter(Thumb.user_id == user.id, Thumb.idea_id == idea_id).first()
  
    if thumb: 
        old_thumb_type = thumb.type
        #delete the old thumb if it exists
        db.delete(thumb)
        db.commit()
        #we create a thumb only if the new thumb type is the opposite as the old thumb type
        if old_thumb_type != new_thumb_type:
            thumb = Thumb(user_id=user.id, idea_id=idea_id, type=new_thumb_type)
            try:
                db.add(thumb)
                db.commit()
                db.refresh(thumb)
                return idea
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail="Database error")
        else:
            return idea
    else:   #no thumb exists, we create a new one
        thumb = Thumb(user_id=user.id, idea_id=idea_id, type=new_thumb_type)
        
        try:
            db.add(thumb)
            db.commit()
            db.refresh(thumb)
            return idea
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error")