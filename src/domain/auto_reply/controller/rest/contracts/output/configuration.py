from pydantic import BaseModel
from pydantic import Field


class CommentAutoReplyConfigurationOutputContract(BaseModel):
    """
    Returns the information about user's auto reply configuration.
    """
    enabled: bool = Field(
        description="If the auto response functionality is enabled.",
        examples=[True],
    )
    auto_reply_delay: int = Field(
        description="The auto response delay in seconds.",
        examples=[60],
        gt=0,
        le=86400,
    )
