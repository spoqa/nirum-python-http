import asyncio
import contextlib

from aiohttp import ClientSession as Session, web
from aiohttp.test_utils import unused_port
from aiotools import async_ctx_manager
from nirum.exc import UnexpectedNirumResponseError
from pytest import raises

from nirum_http.async_http import AsyncHttpTransport


@async_ctx_manager
async def new_session(method_name, callback):
    loop = asyncio.get_event_loop()
    port = unused_port()

    def rpc_callback(request: web.Request):
        if method_name == request.query.get("method"):
            return callback(request)

        return web.Response(status=404)

    app = web.Application()
    app.router.add_post('/', rpc_callback)
    handler = app.make_handler(loop=loop)

    base_url = f'http://127.0.0.1:{port}/'

    server = await loop.create_server(handler, host="127.0.0.1", port=port)
    with contextlib.closing(server):
        session = Session()
        t = AsyncHttpTransport(base_url, session)

        try:
            yield t
        finally:
            await app.cleanup()
            server.close()


async def test_call():
    def callback(request):
        return web.json_response({'_type': 'point', 'x': 1.0, 'top': 2.0})

    method_name = 'hello_world'
    async with new_session(method_name, callback) as t:
        successful, result = await t.call(
            method_name, payload={'name': 'John'},
            service_annotations={},
            method_annotations={},
            parameter_annotations={}
        )
        assert successful
        assert result == {'_type': 'point', 'x': 1.0, 'top': 2.0}


async def test_unexpected_nirum_response_error():
    def callback(request):
        return web.Response(text='Error message')

    method_name = 'hello_world'
    async with new_session(method_name, callback) as t:
        with raises(UnexpectedNirumResponseError) as exc_info:
            await t.call(
                method_name, payload={'name': 'John'},
                service_annotations={},
                method_annotations={},
                parameter_annotations={}
            )
        exc = exc_info.value
        assert exc.args == ('Error message',)
        assert isinstance(exc.args[0], str)
