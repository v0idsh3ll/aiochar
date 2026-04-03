from ..client.session.base import BaseSession

async def get_me(
        session: BaseSession,
        token: str
) -> int:
    """
    Get id by token

    :param session: Session used for request
    :param token: Char Bot token `Obtained from profile editor <https://char.social/ID_HERE>`_
    :return: Profile's ID
    """
    headers = {
        "Authorization": token
    }
    response = await session.request("GET", "/me", headers)
    return response["user_id"]