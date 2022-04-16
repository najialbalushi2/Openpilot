#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import unittest

import psutil

from common.params import Params
from selfdrive.manager import manager
from selfdrive.manager.process import DaemonProcess
from selfdrive.manager.process_config import managed_processes
from tools.sim import bridge
from tools.sim.bridge import connect_carla_client


class TestCarlaIntegration(unittest.TestCase):
  """
  Tests need Carla simulator to run
  """
  subprocess = None

  def test_connect_with_carla(self):
    # Test connecting to Carla within 5 seconds and return no RuntimeError
    client = connect_carla_client()
    assert client is not None
    # Will raise an error if not connected
    client.load_world('Town04_Opt')

  def test_run_bridge(self):
    # Test bridge connect with carla and runs without any errors for 60 seconds
    test_duration = 60

    params = Params()
    args = sys.argv[2:]  # Remove test arguments when executing this test
    params.put_bool("DoShutdown", False)

    p = bridge.main(args, keep_alive=False)[0]
    time.sleep(test_duration)
    params.put_bool("DoShutdown", True)

    p.join()
    # Assert no exceptions
    self.assertEqual(p.exitcode, 0)

  def assert_processes_running(self, expected_p):
    running = {p: False for p in expected_p}
    for name in expected_p:
      for proc in psutil.process_iter():
        if proc.name().endswith(name):
          running[name] = True
          break

    not_running = [key for (key, val) in running.items() if not val]
    self.assertEqual(len(not_running), 0, f"Manager processes are not running: {not_running}")

  def test_manager_and_bridge(self):
    # test manager.py processes and bridge.py to run correctly for 50 seconds
    startup_time = 10
    test_intervals_5sec = 10

    # Set params for simulation to be used for ignored_processes
    # todo could move these to separate file
    os.environ["PASSIVE"] = "0"
    os.environ["NOBOARD"] = "1"
    os.environ["SIMULATION"] = "1"
    os.environ["FINGERPRINT"] = "HONDA CIVIC 2016"
    os.environ["BLOCK"] = "camerad,loggerd"

    # Start manager and bridge
    self.subprocess = subprocess.Popen("../../../selfdrive/manager/manager.py")

    args = sys.argv[2:]  # Remove test arguments when executing this test
    p_bridge = bridge.main(args, keep_alive=False)[0]

    time.sleep(startup_time)

    params = Params()
    ignore_processes = manager.ignored_processes(params)
    all_processes = [p.name for p in managed_processes.values() if
                     (type(p) is not DaemonProcess) and p.enabled and (p.name not in ignore_processes)]

    # Test for 50 seconds
    for _ in range(test_intervals_5sec):
      self.assert_processes_running(all_processes)
      time.sleep(5)

    # Set shutdown to close manager and bridge processes
    params.put_bool("DoShutdown", True)
    # Process could already be closed
    if type(self.subprocess) is subprocess.Popen:
      self.subprocess.wait(timeout=10)
      # Closing gracefully
      self.assertEqual(self.subprocess.returncode, 0)
    p_bridge.join()

  def tearDown(self):
    print("Teardown")
    Params().put_bool("DoShutdown", True)
    manager.manager_cleanup()
    if self.subprocess:
      self.subprocess.wait(5)


if __name__ == "__main__":
  unittest.main()
