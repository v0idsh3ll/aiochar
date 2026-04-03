class BaseAiocharException(Exception):
    pass

class InvalidKey(BaseAiocharException):
    def __init__(self):
        super().__init__("API key is missing or invalid.")

class NotFoundPost(BaseAiocharException):
    def __init__(self):
        super().__init__("Post not found.")