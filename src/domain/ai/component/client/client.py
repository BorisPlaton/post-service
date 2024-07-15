from google.generativeai import GenerativeModel

from domain.ai.component.client.interface import IAIClient


class AIClient(IAIClient):

    def __init__(self):
        self._model = GenerativeModel('gemini-1.5-flash')

    def send(
        self,
        message: str,
    ) -> str:
        return self._model.generate_content(message).text.strip()

