from groq import Groq

from domain.ai.component.client.interface import IAIClient
from settings.config.ai import AISettings


class AIClient(IAIClient):
    """
    Class for interaction with Gemini AI.
    """

    def __init__(
        self,
        settings: AISettings,
    ):
        self._client = Groq(
            api_key=settings.API_KEY,
        )

    def send(
        self,
        message: str,
    ) -> str:
        """
        Send a message to the AI and returns its response.

        @param message:
            The message that is sent to the AI.
        @return:
            The response from the AI.
        """
        chat_completion = self._client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message,
            }],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content.strip()
