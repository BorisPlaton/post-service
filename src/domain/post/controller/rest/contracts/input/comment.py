from pydantic import BaseModel
from pydantic import Field

from domain.post.commad.add_comment.command import AddPostCommentCommand


class NewPostCommentInput(BaseModel):
    """
    Contains necessary fields for adding a comment to the post.
    """
    content: str = Field(
        examples=["It's a very interesting post! Keep doing."],
        description="The text of comment.",
    )

    def to_command(
        self,
        user_id: int,
        post_id: int,
    ) -> AddPostCommentCommand:
        """
        Converts the input to the command.

        @param user_id:
            The user id who wrote a comment.
        @param post_id:
            The post id to which the comment belongs.
        @return:
            The initialized command.
        """
        return AddPostCommentCommand(
            content=self.content,
            post_id=post_id,
            author_id=user_id,
        )
