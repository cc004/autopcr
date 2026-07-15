import unittest

from autopcr.core.clientpool import ClientPool, PoolClientWrapper
from autopcr.core.sdkclient import account, platform
from autopcr.sdk.sdkclients import bsdkclient, twsdkclient


class ClientPoolTransportStateTests(unittest.IsolatedAsyncioTestCase):
    async def _reuse(self, first_sdk, second_sdk, dynamic_headers):
        pool = ClientPool()
        client = PoolClientWrapper(pool, first_sdk)
        client.session._logged = True
        client._headers.update(dynamic_headers)
        client.servers = ["https://routed-1/", "https://routed-2/"]
        client.active_server = 1
        client.viewer_id = 99887766
        original_headers = client._headers
        pool._pool[first_sdk.pool_key] = client

        reused = await pool.get_client(second_sdk)

        self.assertIs(client, reused)
        self.assertIs(original_headers, reused._headers)
        self.assertEqual(dynamic_headers.items() <= reused._headers.items(), True)
        self.assertEqual(
            ["https://routed-1/", "https://routed-2/"], reused.servers
        )
        self.assertEqual(1, reused.active_server)
        self.assertEqual(99887766, reused.viewer_id)
        self.assertTrue(reused.session._logged)
        self.assertTrue(reused.need_refresh)
        self.assertIs(second_sdk, reused._sdk)
        self.assertIs(second_sdk, reused.session.sdk)
        pool.active_uids.clear()

    async def test_cn_reuse_preserves_sid_manifest_and_routed_server(self):
        info = account("pool-cn", "token", platform.Android)
        await self._reuse(
            bsdkclient(info),
            bsdkclient(info),
            {
                "SID": "dynamic-cn-sid",
                "REQUEST-ID": "dynamic-request",
                "MANIFEST-VER": "123456",
            },
        )

    async def test_tw_reuse_preserves_authoritative_resource_headers(self):
        info = account(
            "2987654321",
            "00112233-4455-6677-8899-aabbccddeeff",
            platform.Android,
            viewer_id="2123456789",
            server_id=2,
        )
        await self._reuse(
            twsdkclient(info),
            twsdkclient(info),
            {
                "SID": "dynamic-tw-sid",
                "RES-VER": "00500030",
                "BUNDLE-VER": "00570001",
            },
        )


if __name__ == "__main__":
    unittest.main()
