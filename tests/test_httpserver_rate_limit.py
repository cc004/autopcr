import re
import unittest
from unittest.mock import patch

from autopcr.http_server import httpserver
from autopcr.module.accountmgr import UserException


class FakeUserManager:
    pathsyntax = re.compile(r'g?\d{5,12}')

    def __init__(self):
        self.created = []
        self.existing = set()
        self.password_checks = 0

    def validate_create(self, qid):
        if not self.pathsyntax.fullmatch(qid):
            raise UserException('无效的QQ号')
        if qid in self.existing:
            raise UserException('QQ号已存在')

    def create(self, qid, password):
        self.validate_create(qid)
        self.existing.add(qid)
        self.created.append((qid, password))

    def validate_password(self, qid, password):
        self.password_checks += 1
        return False

    def check_enabled(self, qid):
        return True


class HttpServerRateLimitTest(unittest.IsolatedAsyncioTestCase):
    def make_client(self, usermgr):
        patcher = patch.object(httpserver, 'usermgr', usermgr)
        patcher.start()
        self.addCleanup(patcher.stop)
        server = httpserver.HttpServer()
        server.quart.register_blueprint(server.app)
        return server.quart.test_client()

    async def test_invalid_registration_does_not_consume_rate_limit(self):
        usermgr = FakeUserManager()
        client = self.make_client(usermgr)
        headers = {'X-App-Version': '1.8.0'}

        invalid = await client.post(
            '/daily/api/register',
            json={'qq': '1234', 'password': 'password'},
            headers=headers,
        )
        corrected = await client.post(
            '/daily/api/register',
            json={'qq': '12345', 'password': 'password'},
            headers=headers,
        )

        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(corrected.status_code, 200)
        self.assertEqual(usermgr.created, [('12345', 'password')])

    async def test_successful_registration_consumes_rate_limit(self):
        usermgr = FakeUserManager()
        client = self.make_client(usermgr)
        headers = {'X-App-Version': '1.8.0'}

        first = await client.post(
            '/daily/api/register',
            json={'qq': '12345', 'password': 'password'},
            headers=headers,
        )
        second = await client.post(
            '/daily/api/register',
            json={'qq': '54321', 'password': 'password'},
            headers=headers,
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.headers['Retry-After'], '60')
        self.assertEqual(usermgr.created, [('12345', 'password')])

    async def test_login_rate_limit_preserves_retry_after(self):
        usermgr = FakeUserManager()
        client = self.make_client(usermgr)
        headers = {'X-App-Version': '1.8.0'}
        payload = {'qq': '12345', 'password': 'wrong'}

        first = await client.post('/daily/api/login/qq', json=payload, headers=headers)
        second = await client.post('/daily/api/login/qq', json=payload, headers=headers)

        self.assertEqual(first.status_code, 400)
        self.assertEqual(second.status_code, 429)
        self.assertGreaterEqual(int(second.headers['Retry-After']), 1)
        self.assertEqual(usermgr.password_checks, 1)


if __name__ == '__main__':
    unittest.main()
