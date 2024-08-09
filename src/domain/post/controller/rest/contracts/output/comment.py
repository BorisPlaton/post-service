from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class PostCommentOutput(BaseModel):
    """
    Contains information about a comment to some post.
    """
    comment_id: int = Field(
        alias='id',
        examples=[1],
        ge=1,
        description="The ID of the post comment.",
    )
    post_id: int = Field(
        examples=[1],
        ge=1,
        description="The ID of the post to which the comment belongs.",
    )
    author_id: int = Field(
        examples=[1],
        ge=1,
        description="The ID of the user who commented the post.",
    )
    content: str = Field(
        examples=["It's a very interesting post! Keep doing."],
        description="The text of comment.",
    )
    created_at: datetime = Field(
        examples=[datetime.now()],
        description="The date and time when the comment was created."
    )

