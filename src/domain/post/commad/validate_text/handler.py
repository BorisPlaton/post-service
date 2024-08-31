from domain.ai.component.client.interface import IAIClient
from domain.post.commad.validate_text.command import ValidateTextCommand
from infrastructure.message_bus.command_bus.handler.interface import ICommandHandler


class ValidateTextCommandHandler(ICommandHandler[ValidateTextCommand, bool]):
    """
    The command for moderating a text for availability of the obscene language,
    insults, etc. using AI.
    """

    def __init__(
        self,
        ai_client: IAIClient,
    ):
        """
        @param ai_client:
            The AI client for sending a message to it.
        """
        self._ai_client = ai_client

    async def __call__(
        self,
        message: ValidateTextCommand,
    ) -> bool:
        """
        Validates a provided text and returns boolean value that indicates if text
        doesn't have bad words.

        @param message:
            The text to be validated.
        @raise ValueError:
            If the AI client sends response that doesn't match expected answers.
        @return:
            If text has bad words, returns `False`, otherwise returns `True`.
        """
        doesnt_have_bad_words_answer = '+'
        has_bad_words_answer = '-'

        answer = self._ai_client.send(
            message=f"""
            You are a moderator, that checks the message for availability. You have to answer only with
            '{doesnt_have_bad_words_answer}' and '{has_bad_words_answer}'. If the message contains obscene
            language, insults, racial slurs, etc, you have to answer '{has_bad_words_answer}', otherwise
            you have to answer '{doesnt_have_bad_words_answer}'.

            Does the following text has obscene language, insults, etc: "{message.text}"?
            """,
        )

        if answer == doesnt_have_bad_words_answer:
            return True
        elif answer == has_bad_words_answer:
            return False

        raise ValueError(f"Unexpected answer from model '{answer}'")
