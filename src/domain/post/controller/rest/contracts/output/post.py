from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class PostOutput(BaseModel):
    """
    The output of the post.
    """
    post_id: int = Field(
        alias='id',
        examples=[1],
        ge=1,
    )
    author_id: int = Field(
        examples=[1],
        ge=1,
        description="The ID of the user who wrote the post."
    )
    title: str = Field(
        examples=['Cooking'],
        description="The title of the post."
    )
    content: str = Field(
        examples=['This post is about cooking!'],
        description="The content of the post."
    )
    created_at: datetime = Field(
        examples=[datetime.now()],
        description="The date and time when the post was created."
    )
