class BrowserPoolGeneralException(Exception):
    """General browser_pool pool exception.
    Can be raised in case when using pool has problems"""

    def __init__(self, message='Unexpected error in browser pool.'):
        self.message = message
        super().__init__(self.message)
