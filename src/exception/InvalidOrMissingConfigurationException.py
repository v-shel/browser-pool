class InvalidOrMissingConfigurationException(Exception):
    """Exception raised when incorrect config."""

    def __init__(self, message='Expected configuration value is missing or incorrect.'):
        self.message = message
        super().__init__(self.message)
