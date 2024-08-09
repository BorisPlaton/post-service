from functools import cached_property

import jwt
from jwt import DecodeError
from jwt import ExpiredSignatureError

from domain.jwt_token.command.validate_jwt.command import ValidateJWTCommand
from domain.jwt_token.exception.expired_token_provided import ExpiredTokenProvided
from domain.jwt_token.exception.invalid_token_provided import InvalidTokenProvided
from domain.jwt_token.types.jwt_payload import JWTPayload
from domain.jwt_token.types.jwt_payload import JWTPayloadBody
from shared.message_bus.command_bus.config.mixin import IConfigurableCommand
from shared.message_bus.command_bus.config.options.transactional import TransactionalOption
from shared.message_bus.command_bus.handler.interface import ICommandHandler


class ValidateJWTCommandHandler(
    ICommandHandler[int, ValidateJWTCommand],
    IConfigurableCommand,
):
    """
    Validates that the provided JWT is valid and returns its body payload.
    """

    def __init__(
        self,
        secret_key: str,
    ):
        """
        @param secret_key:
            The secret key used to sign the JWT.
        """
        self._secret_key = secret_key

    async def __call__(
        self,
        message: ValidateJWTCommand,
    ) -> JWTPayloadBody:
        """
        Validates the JWT and returns payload.

        @param message:
            The message with the JWT to validate.
        @raise ExpiredSignatureError:
            If the provided JWT is expired, raises an exception.
        @return:
            Returns the payload of `body` field.
        """
        try:
            decoded_token = jwt.decode(
                jwt=message.token,
                key=self._secret_key,
                algorithms=["HS256"],
            )
        except ExpiredSignatureError:
            raise ExpiredTokenProvided()
        except DecodeError:
            raise InvalidTokenProvided()

        return JWTPayload.from_json(decoded_token).body

    @cached_property
    def config(self) -> dict[type[TransactionalOption], TransactionalOption]:
        return {
            TransactionalOption: TransactionalOption(
                is_transactional=False,
            )
        }
