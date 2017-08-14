from nirum.exc import UnexpectedNirumResponseError
from pytest import fixture, raises
from requests import Session
from requests_mock import Adapter

from nirum_http import HttpTransport


@fixture
def fx_adapter():
    return Adapter()


@fixture
def fx_session(fx_adapter):
    s = Session()
    s.mount('http://', fx_adapter)
    s.mount('https://', fx_adapter)
    return s


def test_call(fx_adapter, fx_session):
    def callback(request, context):
        return {'_type': 'point', 'x': 1.0, 'top': 2.0}
    method_name = 'hello_world'
    base_url = 'http://example.com/'
    url = '{0}?method={1}'.format(base_url, method_name)
    fx_adapter.register_uri('POST', url, json=callback)
    t = HttpTransport(base_url, session=fx_session)
    successful, result = t.call(
        method_name, payload={'name': 'John'},
        service_annotations={},
        method_annotations={},
        parameter_annotations={}
    )
    assert successful
    assert result == {'_type': 'point', 'x': 1.0, 'top': 2.0}


def test_unexpected_nirum_response_error(fx_adapter, fx_session):
    method_name = 'hello_world'
    base_url = 'http://example.com/'
    url = '{0}?method={1}'.format(base_url, method_name)
    fx_adapter.register_uri('POST', url, text='Error message')
    t = HttpTransport(base_url, session=fx_session)
    with raises(UnexpectedNirumResponseError) as exc_info:
        t.call(
            method_name, payload={'name': 'John'},
            service_annotations={},
            method_annotations={},
            parameter_annotations={}
        )
    exc = exc_info.value
    assert exc.args == ('Error message',)
    assert isinstance(exc.args[0], str)
