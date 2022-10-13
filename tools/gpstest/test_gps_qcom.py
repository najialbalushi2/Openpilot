#!/usr/bin/env python3
import time
import unittest
import subprocess as sp

from common.params import Params
from system.hardware import TICI
import cereal.messaging as messaging
from selfdrive.manager.process_config import managed_processes


def exec_mmcli(cmd):
  cmd = "mmcli -m 0 " + cmd
  p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  return p.communicate()


def wait_for_location(socket, timeout):
  while True:
    events = messaging.drain_sock(socket)
    for event in events:
      if  event.gpsLocation.flags % 2:
        return False

    timeout -= 1
    if timeout <= 0:
      return True

    time.sleep(0.1)
    continue



class TestGPS(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    if not TICI:
      raise unittest.SkipTest

    ublox_available = Params().get_bool("UbloxAvailable")
    if ublox_available:
      raise unittest.SkipTest

  @unittest.skip("Skip cold start test due to time")
  def test_quectel_cold_start(self):
    # delete assistance data to enforce cold start for GNSS
    # testing shows that this takes up to 20min

    # invalidate supl setting, cannot be reset
    _, err = exec_mmcli("--location-set-supl-server=unittest:1")

    _, err = exec_mmcli("--command='AT+QGPSDEL=0'")
    assert len(err) == 0, f"GPSDEL failed: {err}"

    managed_processes['rawgpsd'].start()
    start_time = time.monotonic()
    glo = messaging.sub_sock("gpsLocation", timeout=0.1)

    timeout = 10*60*25 # 25 minute
    timedout = wait_for_location(glo, timeout)
    managed_processes['rawgpsd'].stop()

    assert timedout is False, "Waiting for location timed out (25min)!"

    duration = time.monotonic() - start_time
    assert duration < 50, f"Received GPS location {duration}!"


  def test_quectel_cold_start_AGPS(self):
    _, err = exec_mmcli("--command='AT+QGPSDEL=0'")
    assert len(err) == 0, f"GPSDEL failed: {err}"

    # setup AGPS
    _, err = exec_mmcli("--location-set-supl-server=supl.google.com:7276")

    managed_processes['rawgpsd'].start()
    start_time = time.monotonic()
    glo = messaging.sub_sock("gpsLocation", timeout=0.1)

    timeout = 10*60*5 # 1 minute
    timedout = wait_for_location(glo, timeout)
    managed_processes['rawgpsd'].stop()

    assert timedout is False, "Waiting for location timed out (1min)!"

    duration = time.monotonic() - start_time
    assert duration < 60, f"Received GPS location {duration}!"


if __name__ == "__main__":
  unittest.main()