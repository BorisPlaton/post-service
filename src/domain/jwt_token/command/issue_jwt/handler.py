from datetime import datetime
from datetime import timedelta
from functools import cached_property

import jwt

from domain.jwt_token.command.issue_jwt.command import IssueJWTCommand
from domain.jwt_token.types.jwt_payload import JWTPayload
from shared.message_bus.command_bus.config.mixin import IConfigurableCommand
from shared.message_bus.command_bus.config.options.transactional import TransactionalOption
from shared.message_bus.command_bus.handler.interface import ICommandHandler


class IssueJWTCommandHandler(
    ICommandHandler[str, IssueJWTCommand],
    IConfigurableCommand,
):
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

    @cached_property
    def config(self) -> dict[type[TransactionalOption], TransactionalOption]:
        return {
            TransactionalOption: TransactionalOption(
                is_transactional=False,
            )
        }

