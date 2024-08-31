from dataclasses import dataclass

from infrastructure.message_bus.event_bus.event import IEvent


@dataclass(kw_only=True, slots=True, frozen=True)
class NewCommentCreatedEvent(IEvent):
    """
    When new comment is created, this event happens.
    """
    post_id: int
    comment_id: int
    comment_author_id: int
    post_author_id: int
    blocked: bool
