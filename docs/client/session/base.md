Module aiochar.client.session.base
==================================

Classes
-------

`BaseSession(base_url='https://char.social/api/v1/', base_headers=None)`
:   

    ### Methods

    `close(self)`
    :

    `get(self, path: str, **kwargs) ‑> dict[str, ...]`
    :   Get request
        :param path: Path after https://char.social/api/v1/
        :return: Response

    `get_session(self) ‑> aiohttp.client.ClientSession`
    :