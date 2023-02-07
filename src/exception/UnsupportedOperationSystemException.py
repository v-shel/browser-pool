class UnsupportedOperationSystemException(Exception):
    """Exception raised when code runs on unsupported OS."""

    def __init__(self, message='Current OS is unsupported.'):
        self.message = message
        super().__init__(self.message)
