from shared.message_bus.interface.exception import MessageBusException


class NoMessageHandlersFound(MessageBusException):

    def __init__(self):
        super().__init__("No handlers found for the message.")
