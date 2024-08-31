from datetime import datetime
from datetime import timedelta

import jwt

from domain.jwt_token.command.issue_jwt.command import IssueJWTCommand
from domain.jwt_token.types.jwt_payload import JWTPayload
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class IssueJWTCommandHandler(ICommandHandler[IssueJWTCommand, str]):
    """
    The command handler to generate a new JWT.
    """

    def __init__(
        self,
        secret_key: str
    ):
        """
        @param secret_key:
            The secret key used to sign the JWT.
        """
        self._secret_key = secret_key

    async def __call__(
        self,
        message: IssueJWTCommand,
    ) -> str:
        """
        Generates and returns a new JWT with provided payload.

        @param message:
            Contains payload that will contain a JWT.
        @return:
            The new generated JWT.
        """
        payload = JWTPayload(
            exp=datetime.now() + timedelta(hours=1),
            body=message.payload,
        )

        return jwt.encode(
            payload=payload.to_json(),
            key=self._secret_key,
            algorithm="HS256"
        )
