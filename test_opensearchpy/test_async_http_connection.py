from unittest import IsolatedAsyncioTestCase

import pytest
from asynctest import MagicMock, patch, CoroutineMock

from opensearchpy import AsyncHttpConnection
from opensearchpy._async._extra_imports import aiohttp
from opensearchpy._async.compat import get_running_loop


class AsyncContextManagerMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        type(self).__aenter__ = CoroutineMock(
            return_value=MagicMock(
                text=CoroutineMock(return_value='test'),
                status=200,
            )
        )
        type(self).__aexit__ = CoroutineMock(return_value=MagicMock())


@pytest.mark.asyncio
class TestAsyncHttpConnection(IsolatedAsyncioTestCase):
    def test_auth_as_tuple(self):
        c = AsyncHttpConnection(http_auth=('username', 'password'))
        self.assertIsInstance(c._http_auth, aiohttp.BasicAuth)
        self.assertEqual(c._http_auth.login, 'username')
        self.assertEqual(c._http_auth.password, 'password')

    def test_auth_as_string(self):
        c = AsyncHttpConnection(http_auth='username:password')
        self.assertIsInstance(c._http_auth, aiohttp.BasicAuth)
        self.assertEqual(c._http_auth.login, 'username')
        self.assertEqual(c._http_auth.password, 'password')

    def test_auth_as_callable(self):
        def auth_fn():
            pass

        c = AsyncHttpConnection(http_auth=auth_fn)
        self.assertTrue(callable(c._http_auth))

    @patch('aiohttp.ClientSession.request', new_callable=AsyncContextManagerMock)
    async def test_basicauth_in_request_session(self, mock_request):
        c = AsyncHttpConnection(http_auth=('username', 'password'), loop=get_running_loop())
        c.headers = {}
        await c.perform_request('post', '/test')
        mock_request.assert_called_with(
            'post',
            'http://localhost:9200/test',
            data=None,
            auth=c._http_auth,
            headers={},
            timeout=aiohttp.ClientTimeout(total=10, connect=None, sock_read=None, sock_connect=None),
            fingerprint=None,
        )

    @patch('aiohttp.ClientSession.request', new_callable=AsyncContextManagerMock)
    async def test_callable_in_request_session(self, mock_request):
        def auth_fn(*args, **kwargs):
            return {
                'Test': 'PASSED'
            }

        c = AsyncHttpConnection(http_auth=auth_fn, loop=get_running_loop())
        c.headers = {}
        await c.perform_request('post', '/test')

        mock_request.assert_called_with(
            'post',
            'http://localhost:9200/test',
            data=None,
            auth=None,
            headers={'Test': 'PASSED'},
            timeout=aiohttp.ClientTimeout(total=10, connect=None, sock_read=None, sock_connect=None),
            fingerprint=None,
        )
