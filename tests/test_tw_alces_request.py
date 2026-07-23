import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from autopcr.core.pcrclient import pcrclient
from autopcr.model.requests import AlcesExecRequest, TwAlcesExecRequest


class TaiwanAlcesRequestTests(unittest.IsolatedAsyncioTestCase):
    async def _capture_request(self, is_tw: bool):
        client = pcrclient.__new__(pcrclient)
        client._sdk = SimpleNamespace(is_tw=is_tw)
        client.data = SimpleNamespace(
            get_inventory=lambda _: 12345,
            get_mana=lambda: 67890,
        )
        client.request = AsyncMock(return_value=object())
        await client.alces_exec(2468)
        return client.request.await_args.args[0]

    async def test_tw_exec_includes_fresh_roll_type(self):
        request = await self._capture_request(True)

        self.assertIsInstance(request, TwAlcesExecRequest)
        self.assertEqual("alces/exec", request.url)
        self.assertEqual(
            {
                "serial_id": 2468,
                "current_alces_point": 12345,
                "current_gold": 67890,
                "exec_type": 1,
            },
            request.dict(exclude_none=True),
        )

    async def test_cn_exec_body_is_unchanged(self):
        request = await self._capture_request(False)

        self.assertIsInstance(request, AlcesExecRequest)
        self.assertNotIsInstance(request, TwAlcesExecRequest)
        self.assertEqual("alces/exec", request.url)
        self.assertEqual(
            {
                "serial_id": 2468,
                "current_alces_point": 12345,
                "current_gold": 67890,
            },
            request.dict(exclude_none=True),
        )


if __name__ == "__main__":
    unittest.main()
