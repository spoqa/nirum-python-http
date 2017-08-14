from aiohttp import ClientResponseError, ClientSession as Session
from nirum.exc import UnexpectedNirumResponseError
from nirum.transport import Transport

from .util import url_endswith_slash

__all__ = 'AsyncHttpTransport',


class AsyncHttpTransport(Transport):

    def __init__(self, url, session=None):
        if session is None:
            session = Session()
        elif not isinstance(session, Session):
            raise TypeError('session must be {0.__module__}.{0.__name__}, not '
                            '{1!r}'.format(Session, session))
        self.url = url_endswith_slash(url)
        self.session = session

    async def call(self,
                   method_name,
                   payload,
                   service_annotations,
                   method_annotations,
                   parameter_annotations):
        response = await self.session.post(
            self.url,
            params={'method': method_name},
            headers={'Accept': 'application/json'},
            json=payload
        )
        try:
            content = await response.json()
        except (ValueError, ClientResponseError):
            raise UnexpectedNirumResponseError(
                await response.text()  # TODO: encoding error?
            )
        return response.status == 200, content
