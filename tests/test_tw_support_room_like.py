import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from autopcr.core.apiclient import ApiException
from autopcr.core.pcrclient import pcrclient
from autopcr.core.region import REGION_TW, reset_region, set_region
from autopcr.model.modelbase import Request
from autopcr.model.requests import RoomLikeRequest
from autopcr.module.modules.room import room_like_back


class TaiwanRoomLikeProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_client_sends_apk_room_like_post_param(self):
        target_viewer_id = 2_123_456_789
        response = object()
        client = SimpleNamespace(request=AsyncMock(return_value=response))

        actual = await pcrclient.room_like(client, target_viewer_id)

        self.assertIs(response, actual)
        request = client.request.await_args.args[0]
        self.assertIsInstance(request, RoomLikeRequest)
        self.assertEqual(target_viewer_id, request.target_viewer_id)
        self.assertIsInstance(request.target_viewer_id, int)
        self.assertEqual(
            {"target_viewer_id"},
            set(RoomLikeRequest.__fields__) - set(Request.__fields__),
        )

    async def test_status_five_uses_another_room_instead_of_aborting(self):
        users = iter(range(100, 108))

        async def visit(_viewer_id):
            viewer_id = next(users)
            return SimpleNamespace(
                room_user_info=SimpleNamespace(
                    today_like_flag=False,
                    viewer_id=viewer_id,
                    name=f"user-{viewer_id}",
                )
            )

        rewards = SimpleNamespace(reward_list=[])
        client = SimpleNamespace(
            room_start=AsyncMock(),
            room_like_history=AsyncMock(
                return_value=SimpleNamespace(
                    today_like_count=3,
                    today_be_liked_count=1,
                    be_liked_history=[SimpleNamespace(viewer_id=999)],
                )
            ),
            room_visit=AsyncMock(side_effect=visit),
            room_like=AsyncMock(
                side_effect=[ApiException("generic TW processing error", 5, 208)]
                + [rewards] * 7
            ),
            serialize_reward_summary=AsyncMock(return_value="rewards"),
        )
        parent = SimpleNamespace(
            id="tw-room-like-test",
            get_config=lambda _key, default=None: default,
        )

        token = set_region(REGION_TW)
        try:
            await room_like_back(parent).do_task(client)
        finally:
            reset_region(token)

        self.assertEqual(8, client.room_like.await_count)
        self.assertEqual(8, client.room_visit.await_count)
        self.assertEqual(999, client.room_visit.await_args_list[0].args[0])
        self.assertEqual(0, client.room_visit.await_args_list[1].args[0])

    async def test_other_room_like_errors_still_abort(self):
        user = SimpleNamespace(
            room_user_info=SimpleNamespace(
                today_like_flag=False,
                viewer_id=100,
                name="user",
            )
        )
        error = ApiException("different failure", 6, 1)
        client = SimpleNamespace(
            room_start=AsyncMock(),
            room_like_history=AsyncMock(
                return_value=SimpleNamespace(
                    today_like_count=0,
                    today_be_liked_count=0,
                    be_liked_history=[],
                )
            ),
            room_visit=AsyncMock(return_value=user),
            room_like=AsyncMock(side_effect=error),
        )
        parent = SimpleNamespace(
            id="tw-room-like-error-test",
            get_config=lambda _key, default=None: default,
        )

        with self.assertRaises(ApiException) as caught:
            await room_like_back(parent).do_task(client)

        self.assertIs(error, caught.exception)

    async def test_cn_status_five_is_not_silently_swallowed(self):
        user = SimpleNamespace(
            room_user_info=SimpleNamespace(
                today_like_flag=False,
                viewer_id=100,
                name="user",
            )
        )
        error = ApiException("generic CN processing error", 5, 208)
        client = SimpleNamespace(
            room_start=AsyncMock(),
            room_like_history=AsyncMock(return_value=SimpleNamespace(
                today_like_count=0,
                today_be_liked_count=0,
                be_liked_history=[],
            )),
            room_visit=AsyncMock(return_value=user),
            room_like=AsyncMock(side_effect=error),
        )
        parent = SimpleNamespace(
            id="cn-room-like-error-test",
            get_config=lambda _key, default=None: default,
        )

        with self.assertRaises(ApiException) as caught:
            await room_like_back(parent).do_task(client)

        self.assertIs(error, caught.exception)

    async def test_tw_unread_like_limit_result_code_uses_another_room(self):
        users = iter(range(200, 206))

        async def visit(_viewer_id):
            viewer_id = next(users)
            return SimpleNamespace(
                room_user_info=SimpleNamespace(
                    today_like_flag=False,
                    viewer_id=viewer_id,
                    name=f"user-{viewer_id}",
                )
            )

        rewards = SimpleNamespace(reward_list=[])
        client = SimpleNamespace(
            room_start=AsyncMock(),
            room_like_history=AsyncMock(
                return_value=SimpleNamespace(
                    today_like_count=5,
                    today_be_liked_count=0,
                    be_liked_history=[],
                )
            ),
            room_visit=AsyncMock(side_effect=visit),
            room_like=AsyncMock(
                side_effect=[
                    ApiException("TW unread LIKE limit", 6, 3114),
                    *([rewards] * 5),
                ]
            ),
            serialize_reward_summary=AsyncMock(return_value="rewards"),
        )
        parent = SimpleNamespace(
            id="tw-room-like-3114-test",
            get_config=lambda _key, default=None: default,
        )

        token = set_region(REGION_TW)
        try:
            await room_like_back(parent).do_task(client)
        finally:
            reset_region(token)

        self.assertEqual(6, client.room_visit.await_count)
        self.assertEqual(6, client.room_like.await_count)

    async def test_repeated_status_five_has_a_finite_attempt_limit(self):
        user = SimpleNamespace(
            room_user_info=SimpleNamespace(
                today_like_flag=False,
                viewer_id=100,
                name="user",
            )
        )
        client = SimpleNamespace(
            room_start=AsyncMock(),
            room_like_history=AsyncMock(
                return_value=SimpleNamespace(
                    today_like_count=0,
                    today_be_liked_count=0,
                    be_liked_history=[],
                )
            ),
            room_visit=AsyncMock(return_value=user),
            room_like=AsyncMock(
                side_effect=ApiException("generic TW processing error", 5, 208)
            ),
            serialize_reward_summary=AsyncMock(return_value="no rewards"),
        )
        parent = SimpleNamespace(
            id="tw-room-like-limit-test",
            get_config=lambda _key, default=None: default,
        )
        module = room_like_back(parent)

        token = set_region(REGION_TW)
        try:
            await module.do_task(client)
        finally:
            reset_region(token)

        self.assertEqual(30, client.room_visit.await_count)
        self.assertEqual(30, client.room_like.await_count)
        self.assertTrue(module.is_warn)
        self.assertIn("停止继续尝试", "\n".join(module.log))


if __name__ == "__main__":
    unittest.main()
