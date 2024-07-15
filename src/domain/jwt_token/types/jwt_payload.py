from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True, kw_only=True)
class JWTPayload:
    """
    Represents a JWT payload.
    """
    exp: datetime
    body: JWTPayloadBody

    def to_json(self) -> dict[str, Any]:
        """
        Converts to the JWT before encoding.

        @return:
            The JSON representation of the payload.
        """
        return {
            'exp': self.exp,
            'body': self.body.to_json()
        }

    @classmethod
    def from_json(cls, body: dict[str, Any]) -> JWTPayload:
        """
        Converts the JSON representation of the payload into a class instance.

        @param body:
            The JSON representation of the payload.
        @return:
            The initialized instance of class.
        """
        return cls(
            exp=body['exp'],
            body=JWTPayloadBody.from_json(body['body'])
        )


@dataclass(slots=True, kw_only=True)
class JWTPayloadBody:
    """
    The class representation of the `body` field of JWT.
    """
    user_id: int

    def to_json(self) -> dict[str, Any]:
        """
        Converts to the JWT before encoding.

        @return:
            The json representation of the payload.
        """
        return {'user_id': self.user_id}

    @classmethod
    def from_json(cls, body: dict[str, Any]) -> JWTPayloadBody:
        """
        Converts the JSON representation of the payload into a class instance.

        @param body:
            The `body` field content.
        @return:
            The initialized instance of class.
        """
        return cls(
            user_id=body['user_id']
        )
