class DateRangeError(Exception):
    """Raised when date_from is after date_to"""
    def __init__(self, message: str):
        self.message = message
