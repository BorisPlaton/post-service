from dataclasses import dataclass

from domain.jwt_token.types.jwt_payload import JWTPayloadBody
from infrastructure.message_bus.command_bus.command import ICommand


@dataclass(kw_only=True, slots=True)
class IssueJWTCommand(ICommand):
    """
    The command to issue a new JWT token.
    """
    payload: JWTPayloadBody
