from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

from domain.user.command.register.command import RegisterUserCommand


class RegisterUserInput(BaseModel):
    """
    Contains all necessary information to register a new user.
    """
    login: str = Field(
        description="The user's login.",
        examples=["qwerty123"],
        max_length=128,
        min_length=1,
    )
    password: str = Field(
        description="The user's password.",
        examples=["0000"],
        max_length=128,
        min_length=1,
    )

    def to_command(self) -> RegisterUserCommand:
        """
        Creates a command from the client's input values.

        @return:
            The initialized command with input values.
        """
        return RegisterUserCommand(
            login=self.login,
            password=self.password,
        )
