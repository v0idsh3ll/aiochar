class BaseAiocharException(Exception):
    pass

class InvalidKey(BaseAiocharException):
    def __init__(self):
        super().__init__("API key is missing or invalid.")

class NotFoundPost(BaseAiocharException):
    def __init__(self):
        super().__init__("Post not found.")

class NoEnoughData(BaseAiocharException):
    def __init__(self):
        super().__init__("Not enough data. Check if you provided all needed data.")

class APIError(BaseAiocharException):
    def __init__(self, *args):
        super().__init__(*args)
class CharBadRequest(BaseAiocharException):
    pass