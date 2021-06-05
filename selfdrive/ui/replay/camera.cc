#include "selfdrive/ui/replay/camera.h"

#include <QDebug>

#include "selfdrive/camerad/cameras/camera_common.h"

static const VisionStreamType stream_types[] = {
    [RoadCam] = VISION_STREAM_RGB_BACK,
    [DriverCam] = VISION_STREAM_RGB_FRONT,
    [WideRoadCam] = VISION_STREAM_RGB_WIDE,
};

// class CameraServer::CameraState

class CameraServer::CameraState {
 public:
  CameraState(VisionIpcServer *server, CameraType type, const FrameReader *f)
      : vipc_server(server), width(f->width), height(f->height), stream_type(stream_types[type]) {
    vipc_server->create_buffers(stream_type, UI_BUF_COUNT, true, width, height);
    thread = std::thread(&CameraState::run, this);
  }

  ~CameraState() {
    exit = true;
    thread.join();
  }

  inline bool frameChanged(const FrameReader *f) const {
    return width != f->width || height != f->height;
  }

  void run() {
    while (!exit) {
      std::pair<FrameReader *, uint32_t> frame;
      if (!queue.try_pop(frame, 20)) continue;

      auto &[fr, segmentId] = frame;
      if (frameChanged(fr)) {
        // eidx is not in the same segment with different frame size
        continue;
      }

      VisionBuf *buf = vipc_server->get_buffer(stream_type);
      if (fr->get(segmentId, buf->addr)) {
        VisionIpcBufExtra extra = {};
        vipc_server->send(buf, &extra, false);
      }
    }
  }

  int width, height;
  VisionStreamType stream_type;
  SafeQueue<std::pair<FrameReader *, uint32_t>> queue;
  VisionIpcServer *vipc_server = nullptr;
  std::thread thread;
  std::atomic<bool> exit = false;
};

// class CameraServer

CameraServer::CameraServer() {
  device_id_ = cl_get_device_id(CL_DEVICE_TYPE_DEFAULT);
  context_ = CL_CHECK_ERR(clCreateContext(NULL, 1, &device_id_, NULL, NULL, &err));
}

CameraServer::~CameraServer() {
  stop();
  CL_CHECK(clReleaseContext(context_));
}

void CameraServer::ensure(FrameReader *frs[]) {
  if (vipc_server_) {
    // restart vipc server if frame changed. such as switched between qcameras and cameras.
    for (auto cam_type : ALL_CAMERAS) {
      const FrameReader *f = frs[cam_type];
      auto &cs = camera_states_[cam_type];
      if (f && (!cs || cs->frameChanged(f)) || (!f && cs)) {
        stop();
        break;
      }
    }
  }
  if (!vipc_server_) {
    for (auto cam_type : ALL_CAMERAS) {
      const FrameReader *f = frs[cam_type];
      if (!f || !f->valid()) continue;

      if (!vipc_server_) {
        vipc_server_ = new VisionIpcServer("camerad", device_id_, context_);
      }
      camera_states_[cam_type] = new CameraState(vipc_server_, cam_type, f);
    }
    if (vipc_server_) {
      vipc_server_->start_listener();
    }
  }
}

void CameraServer::pushFrame(CameraType type, FrameReader *fr, uint32_t encodeFrameId) {
  if (auto &cs = camera_states_[type]) {
    cs->queue.push({fr, encodeFrameId});
  }
}

void CameraServer::stop() {
  if (vipc_server_) {
    // stop camera threads
    for (auto &cs : camera_states_) {
      delete cs;
      cs = nullptr;
    }
    delete vipc_server_;
    vipc_server_ = nullptr;
  }
}
