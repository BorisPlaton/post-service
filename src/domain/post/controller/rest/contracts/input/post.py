from pydantic import BaseModel
from pydantic import Field

from domain.post.commad.create_post.command import CreatePostCommand


class NewPostInput(BaseModel):
    """
    Contains necessary fields for creating a new post.
    """
    title: str = Field(
        examples=['Cooking'],
        description="The title of the post."
    )
    content: str = Field(
        examples=['This post is about cooking!'],
        description="The content of the post."
    )

    def to_command(
        self,
        user_id: int,
    ) -> CreatePostCommand:
        """
        Converts the input to the command.

        @param user_id:
            The user id who creates a post.
        @return:
            The initialized command.
        """
        return CreatePostCommand(
            title=self.title,
            content=self.content,
            author_id=user_id,
        )
