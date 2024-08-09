from shared.exception.not_found import NotFound


class ConfigurationDoesNotExist(NotFound):

    def __init__(self):
        super().__init__("Delayed response configuration doesnt exist for this user.")
