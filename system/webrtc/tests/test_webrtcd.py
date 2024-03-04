#!/usr/bin/env python
import asyncio
import json
import unittest
from unittest.mock import MagicMock, AsyncMock
# for aiortc and its dependencies
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from openpilot.system.webrtc.webrtcd import get_stream

import aiortc
from teleoprtc import WebRTCOfferBuilder
from parameterized import parameterized


class TestWebrtcdProc(unittest.IsolatedAsyncioTestCase):
  async def assertCompletesWithTimeout(self, awaitable, timeout=1):
    try:
      async with asyncio.timeout(timeout):
        await awaitable
    except TimeoutError:
      self.fail("Timeout while waiting for awaitable to complete")

  @parameterized.expand([
    (["testJoystick"], ["carState"]),
    ([], ["carState"]),
    (["testJoystick"], []),
    ([], []),
  ])
  async def test_webrtcd(self, in_services, out_services):
    mock_request = MagicMock()
    async def connect(offer):
      body = {'sdp': offer.sdp, 'cameras': offer.video, 'bridge_services_in': in_services, 'bridge_services_out': out_services}
      mock_request.json.side_effect = AsyncMock(return_value=body)
      response = await get_stream(mock_request)
      response_json = json.loads(response.text)
      return aiortc.RTCSessionDescription(**response_json)

    builder = WebRTCOfferBuilder(connect)
    builder.offer_to_receive_video_stream("road")
    builder.offer_to_receive_audio_stream()
    if len(in_services) > 0 or len(out_services) > 0:
      builder.add_messaging()

    stream = builder.stream()

    await self.assertCompletesWithTimeout(stream.start())
    await self.assertCompletesWithTimeout(stream.wait_for_connection())

    self.assertTrue(stream.has_incoming_video_track("road"))
    self.assertTrue(stream.has_incoming_audio_track())
    self.assertEqual(stream.has_messaging_channel(), len(in_services) > 0 or len(out_services) > 0)

    video_track, audio_track = stream.get_incoming_video_track("road"), stream.get_incoming_audio_track()
    await self.assertCompletesWithTimeout(video_track.recv())
    await self.assertCompletesWithTimeout(audio_track.recv())

    await self.assertCompletesWithTimeout(stream.stop())

    # cleanup, very implementation specific, test may break if it changes
    self.assertTrue(mock_request.app["streams"].__setitem__.called, "Implementation changed, please update this test")
    _, session = mock_request.app["streams"].__setitem__.call_args.args
    await self.assertCompletesWithTimeout(session.post_run_cleanup())


if __name__ == "__main__":
  unittest.main()
