Module aiochar.client.bot
=========================

Classes
-------

`Bot(token: str, session: aiochar.client.session.base.BaseSession | None = None)`
:   Bot class.
    
    :param token: Char Bot token `Obtained from profile editor <https://char.social/ID_HERE>`_
    :raise TokenValidationError: When token has invalid format this exception will be raised

    ### Instance variables

    `token`
    :

    ### Methods

    `close(self) ‑> None`
    :   Method to close session and bot.
        
        :param self:
        :return:

    `get_me(self) ‑> int`
    :   Get id by token.
        
        :return: Profile's ID