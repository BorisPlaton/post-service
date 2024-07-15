from dataclasses import dataclass

from domain.jwt_token.types.jwt_payload import JWTPayloadBody
from shared.message_bus.command_bus.interface.command import ICommand


@dataclass(kw_only=True, slots=True)
class IssueJWTCommand(ICommand):
    """
    The command to issue new JWT token.
    """
    payload: JWTPayloadBody
