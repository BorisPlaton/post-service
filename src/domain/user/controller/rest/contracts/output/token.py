from pydantic import BaseModel
from pydantic import Field


class UserJWTOutput(BaseModel):
    """
    Returns a user's JWT after the successful authentication.
    """
    access_token: str = Field(
        description="The user's JWT.",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VyX2lkIjoiMTIzNDU2Nzg5MCJ9."
            "HhclBU1hdg0RynbUgnLXtm9rhm0m4yuWJF0jjVaZ_u0"
        ],
    )
    token_type: str = Field(
        description="The token type. It is always `Bearer`.",
        examples=["Bearer"]
    )

