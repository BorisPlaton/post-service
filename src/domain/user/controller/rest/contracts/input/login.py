from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field

from domain.user.command.login.command import LogInUserCommand


class UserLoginInput(BaseModel):
    """
    Contains to log in user.
    """
    login: str = Field(
        description="The user login.",
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

    def to_command(self) -> LogInUserCommand:
        """
        Creates a command from the client's input values.

        @return:
            The initialized command with input values.
        """
        return LogInUserCommand(
            login=self.login,
            password=self.password,
        )
