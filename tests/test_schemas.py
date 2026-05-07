from datetime import datetime, timezone

from app.models import VoteType
from app.schemas import IdeaDisplay, ThumbDisplay


def test_idea_display_computed_thumbs_counts():
    thumbs = [
        ThumbDisplay(
            id=1,
            user_id=1,
            idea_id=1,
            type=VoteType.UP,
            created_at=datetime.now(timezone.utc),
        ),
        ThumbDisplay(
            id=2,
            user_id=2,
            idea_id=1,
            type=VoteType.UP,
            created_at=datetime.now(timezone.utc),
        ),
        ThumbDisplay(
            id=3,
            user_id=3,
            idea_id=1,
            type=VoteType.DOWN,
            created_at=datetime.now(timezone.utc),
        ),
    ]

    idea = IdeaDisplay(
        id=1,
        concept="Test concept",
        created_at=datetime.now(timezone.utc),
        user=None,
        thumbs=thumbs,
    )

    assert idea.thumbs_up == 2
    assert idea.thumbs_down == 1
