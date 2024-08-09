from dataclasses import dataclass

from shared.task.interface.dto import ITaskDTO


@dataclass(kw_only=True, slots=True, frozen=True)
class NewCommentCreatedTaskDTO(ITaskDTO):
    """
    When new comment is created, this event happens.
    """
    post_id: int
    comment_id: int
    comment_author_id: int
    post_author_id: int
