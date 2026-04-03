from functools import lru_cache
from string import ascii_letters, digits


class TokenValidationError(Exception):
    pass


VALID_CHARACTERS = ascii_letters + digits + "_"

@lru_cache
def validate_token(token: str) -> bool:
    """
    Validate Char token

    :param token: Char Bot token `Obtained from profile editor <https://char.social/ID_HERE>`_
    :return: Is the token valid
    """
    if not isinstance(token, str):
        message = f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        raise TokenValidationError(message)

    if any(x.isspace() for x in token):
        message = "Token is invalid! It can't contains spaces."
        raise TokenValidationError(message)

    if len(token) != 43:
        message = "Token is invalid! It must be 43 characters length."
        raise TokenValidationError(message)

    if any(x not in VALID_CHARACTERS for x in token):
        message = "Token is invalid! It must contain only a-Z and 0-9 and _."
        raise TokenValidationError(message)

    return True