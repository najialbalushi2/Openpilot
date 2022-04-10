#!/usr/bin/env python3
import os
import sys
import cereal.messaging as messaging
import multiprocessing
import numpy as np
from common.window import Window

NVIDIA = int(os.getenv("NVIDIA", "0"))
if not NVIDIA:
  import av # pylint: disable=import-error

def get_codec():
  # init from stock hevc
  fdat = open("/home/batman/Downloads/fcamera.hevc", "rb").read(243446)
  codec = av.codec.Codec('hevc').create()
  buf = av.packet.Packet(fdat)
  codec.decode(buf)
  return codec

# NVIDIA=1 LD_LIBRARY_PATH="/raid.dell2/PyNvCodec:$LD_LIBRARY_PATH" ./compressed.py 192.168.254.186
FIFO_NAME = "/tmp/decodepipe"
def decoder():
  w,h = 1928, 1208
  win = Window(w, h)
  sys.path.append("/raid.dell2/PyNvCodec")
  import PyNvCodec as nvc # pylint: disable=import-error
  decoder = nvc.PyNvDecoder(FIFO_NAME, 0)
  conv = nvc.PySurfaceConverter(w, h, nvc.PixelFormat.NV12, nvc.PixelFormat.RGB, 0)
  nvDwn = nvc.PySurfaceDownloader(w, h, nvc.PixelFormat.RGB, 0)
  cc1 = nvc.ColorspaceConversionContext(nvc.ColorSpace.BT_709, nvc.ColorRange.JPEG)
  print("got decoder")
  img = np.zeros((h,w,3), dtype=np.uint8)
  cnt = 0
  while 1:
    rawSurface = decoder.DecodeSingleSurface()
    if rawSurface.Empty():
      continue
    cnt += 1
    if cnt < 1200:
      continue
    convSurface = conv.Execute(rawSurface, cc1)
    #convSurface.PlanePtr(0).Export(img, w * 3, 0)
    nvDwn.DownloadSingleSurface(convSurface, img)
    win.draw(img)

def get_nvcodec():
  if os.path.exists(FIFO_NAME):
    os.unlink(FIFO_NAME)
  os.mkfifo(FIFO_NAME)
  multiprocessing.Process(target=decoder).start()
  fdat = open("/home/batman/Downloads/fcamera.hevc", "rb").read()
  fifo_file = open(FIFO_NAME, "wb")
  fifo_file.write(fdat)
  fifo_file.flush()
  return fifo_file

if __name__ == "__main__":

  if NVIDIA:
    codec = get_nvcodec()
  else:
    win = Window(1928, 1208)
    codec = get_codec()

  # connect to socket
  os.environ["ZMQ"] = "1"
  messaging.context = messaging.Context()

  cam = int(os.getenv("CAM", "0"))
  if cam == 0:
    sock = messaging.sub_sock("wideRoadEncodeData", None, addr=sys.argv[1], conflate=False)
    alt_sock = messaging.sub_sock("wideRoadEncodeIdx", None, addr=sys.argv[1], conflate=False)
  elif cam == 1:
    sock = messaging.sub_sock("roadEncodeData", None, addr=sys.argv[1], conflate=False)
    alt_sock = messaging.sub_sock("roadEncodeIdx", None, addr=sys.argv[1], conflate=False)
  elif cam == 2:
    sock = messaging.sub_sock("driverEncodeData", None, addr=sys.argv[1], conflate=False)
    alt_sock = messaging.sub_sock("driverEncodeIdx", None, addr=sys.argv[1], conflate=False)

  match = {}
  last_idx = -1
  while 1:
    msgs = messaging.drain_sock(sock, wait_for_one=True)
    alt_msgs = messaging.drain_sock(alt_sock, wait_for_one=False)
    if len(msgs) > 15:
      print("FRAME DROP")
      continue

    for evt in alt_msgs:
      evta = getattr(evt, evt.which())
      match[evta.timestampEof//1000] = evta

    for i,evt in enumerate(msgs):
      evta = getattr(evt, evt.which())
      dat = evta.data
      lat = ((evt.logMonoTime/1e9) - (evta.timestampEof/1e6))*1000
      print(len(msgs), "%4d %.3f %.3f latency %.2f ms" % (evta.idx, evt.logMonoTime/1e9, evta.timestampEof/1e6, lat), len(dat), evta.timestampEof in match) #, match[evta.timestamp] if evta.timestamp in match else "")
      if evta.idx != 0 and evta.idx != (last_idx+1):
        print("DROP!")
      last_idx = evta.idx

      if NVIDIA:
        codec.write(dat)
        codec.flush()
      else:
        buf = av.packet.Packet(dat)
        #print(buf)
        try:
          frame = codec.decode(buf)
        except av.error.EOFError:
          print("EOFError")
          codec = get_codec()
          continue
        if len(frame) == 0:
          continue
        # only draw last frame
        if i == len(msgs) - 1:
          img = frame[0].to_ndarray(format=av.video.format.VideoFormat('rgb24'))
          win.draw(img)

