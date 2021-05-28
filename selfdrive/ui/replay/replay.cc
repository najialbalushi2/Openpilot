#include "selfdrive/ui/replay/replay.h"

#include <QDir>
#include <QJsonDocument>
#include <QJsonObject>

#include "cereal/services.h"
#include "selfdrive/camerad/cameras/camera_common.h"
#include "selfdrive/common/timing.h"
#include "selfdrive/hardware/hw.h"

const int SEGMENT_LENGTH = 60;  // 60s
const int FORWARD_SEGS = 2;
const int BACKWARD_SEGS = 2;
const std::string LOG_ROOT =
    Hardware::PC() ? util::getenv_default("HOME", "/.comma/media/0/realdata", "/data/media/0/realdata")
                   : "/data/media/0/realdata";

int getch() {
  int ch;
  struct termios oldt;
  struct termios newt;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);

  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  ch = getchar();
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);

  return ch;
}

Replay::Replay(const QString &route, SubMaster *sm, QObject *parent) : route_(route), sm_(sm), QObject(parent) {
  QStringList block = QString(getenv("BLOCK")).split(",");
  qDebug() << "blocklist" << block;

  QStringList allow = QString(getenv("ALLOW")).split(",");
  qDebug() << "allowlist" << allow;

  std::vector<const char *> s;
  for (const auto &it : services) {
    if ((allow[0].size() == 0 || allow.contains(it.name)) &&
        !block.contains(it.name)) {
      s.push_back(it.name);
      socks_.insert(it.name);
    }
  }
  qDebug() << "services " << s;

  if (sm_ == nullptr) {
    pm_ = new PubMaster(s);
  }

  device_id_ = cl_get_device_id(CL_DEVICE_TYPE_DEFAULT);
  context_ = CL_CHECK_ERR(clCreateContext(NULL, 1, &device_id_, NULL, NULL, &err));
}

Replay::~Replay() {
  segments_.clear();
  delete pm_;
  CL_CHECK(clReleaseContext(context_));
}

void Replay::load() {
  if (!loadFromLocal()) {
    loadFromServer();
  }
}

void Replay::loadFromServer() {
  const QString url = "https://api.commadotai.com/v1/route/" + route_ + "/files";
  http_ = new HttpRequest(this, url, "", !Hardware::PC());
  QObject::connect(http_, &HttpRequest::receivedResponse, this, &Replay::loadFromJson);
}

bool Replay::loadFromLocal() {
  QStringList list = route_.split('|');
  if (list.size() != 2) return false;

  QJsonArray cameras, dcameras, ecameras, qcameras;
  QJsonArray logs, qlogs;

  QDir log_root(LOG_ROOT.c_str());
  QStringList folders = log_root.entryList(QStringList() << list[1] + "*", QDir::Dirs | QDir::NoDot, QDir::NoSort);
  if (folders.isEmpty()) return false;

  std::sort(folders.begin(), folders.end(), [](const QString &file1, const QString &file2) {
    return file1.split("--")[2].toInt() < file2.split("--")[2].toInt();
  });

  for (auto folder : folders) {
    QDir segment(log_root.filePath(folder));
    const QStringList files = segment.entryList(QDir::Files);
    for (auto f : files) {
      const QString file_path = "file://" + segment.filePath(f);
      if (f.startsWith("fcamera")) {
        cameras << file_path;
      } else if (f.startsWith("dcamera")) {
        dcameras << file_path;
      } else if (f.startsWith("ecamera")) {
        ecameras << file_path;
      } else if (f.startsWith("qcamera")) {
        qcameras << file_path;
      } else if (f.startsWith("rlog")) {
        logs << file_path;
      } else if (f.startsWith("qlog")) {
        qlogs << file_path;
      }
    }
  }
  QJsonObject obj;
  obj["cameras"] = cameras;
  obj["dcameras"] = dcameras;
  obj["ecameras"] = ecameras;
  obj["qcameras"] = qcameras;
  obj["logs"] = logs;
  obj["qlogs"] = qlogs;

  QJsonDocument doc(obj);
  QString json = doc.toJson(QJsonDocument::Compact);
  return loadFromJson(json);
}

bool Replay::loadFromJson(const QString &json) {
  QJsonDocument doc = QJsonDocument::fromJson(json.trimmed().toUtf8());
  if (doc.isNull()) {
    qInfo() << "JSON Parse failed";
    return false;
  }

  frame_paths_[RoadCamFrame] = doc["cameras"].toVariant().toStringList();
  if (frame_paths_[RoadCamFrame].isEmpty()) {
    // fallback to qcameras
    frame_paths_[RoadCamFrame] = doc["qcameras"].toVariant().toStringList();
  }
  frame_paths_[DriverCamFrame] = doc["dcameras"].toVariant().toStringList();
  frame_paths_[WideRoadCamFrame] = doc["ecameras"].toVariant().toStringList();

  log_paths_ = doc["logs"].toVariant().toStringList();
  if (log_paths_.isEmpty()) {
    // fallback to qlogs
    log_paths_ = doc["qlogs"].toVariant().toStringList();
  }

  if (log_paths_.isEmpty()) {
    qInfo() << "no logs found in route " << route_;
    return false;
  }

  qInfo() << "replay route " << route_ << ", total segments:" << log_paths_.size();

  // start threads
  typedef void (Replay::*threadFunc)();
  threadFunc thread_func[] = {&Replay::segmentQueueThread, &Replay::keyboardThread, &Replay::streamThread};
  for (int i = 0; i < std::size(thread_func); ++i) {
    QThread *t = QThread::create(thread_func[i], this);
    connect(t, &QThread::finished, t, &QThread::deleteLater);
    t->start();
  }
  return true;
}

void Replay::addSegment(int n) {
  std::unique_lock lk(segment_lock_);
  if (segments_.find(n) != segments_.end()) return;

  std::shared_ptr<Segment> seg = std::make_shared<Segment>(n);
  seg->loading = 1;
  segments_[n] = seg;
  lk.unlock();

  // read log
  seg->log = new LogReader(log_paths_[n]);
  connect(seg->log, &LogReader::finished, [s = seg.get()](bool success) { --s->loading; });
  seg->log->start();

  // read frames
  for (int i = 0; i < std::size(frame_paths_); ++i) {
    if (n < frame_paths_[i].size()) {
      seg->loading += 1;
      seg->frames[i] = new FrameReader(frame_paths_[i][n].toStdString(), VISION_STREAM_RGB_BACK);
      connect(seg->frames[i], &FrameReader::finished, [s = seg.get()](bool success) { --s->loading; });
      seg->frames[i]->start();
    }
  }
}

// return nullptr if segment is not loaded
std::shared_ptr<Segment> Replay::getSegment(int n) {
  std::unique_lock lk(segment_lock_);
  if (auto it = segments_.find(n); it != segments_.end()) {
    return !it->second->loading ? it->second : nullptr;
  } else {
    return nullptr;
  }
}

void Replay::removeSegment(int n) {
  std::unique_lock lk(segment_lock_);
  segments_.erase(n);
}

void Replay::startVipcServer(const Segment *seg) {
  for (auto f : seg->frames) {
    if (f && f->valid()) {
      if (!vipc_server_) {
        vipc_server_ = new VisionIpcServer("camerad", device_id_, context_);
      }
      vipc_server_->create_buffers(f->stream_type, UI_BUF_COUNT, true, f->width, f->height);
    }
  }
  if (vipc_server_) {
    QThread *t = QThread::create(&Replay::cameraThread, this);
    connect(t, &QThread::finished, t, &QThread::deleteLater);
    t->start();
    qDebug() << "start vipc server";
  }
}

std::optional<std::pair<std::shared_ptr<Segment>, uint32_t>> Replay::getFrameSegment(int seg_id, FrameType type, uint32_t frame_id) {
  auto seg = getSegment(seg_id);
  if (!seg) return std::nullopt;

  const EncodeIdx *eidx = seg->log->getFrameEncodeIdx(type, frame_id);
  if (!eidx) return std::nullopt;

  if (seg_id != eidx->segmentNum) {
    // frame is in anther segment
    seg = getSegment(eidx->segmentNum);
    if (!seg) return std::nullopt;
  }
  return std::make_pair(seg, eidx->segmentId);
};

void Replay::seekTime(int ts) {
  ts = std::clamp(ts, 0, log_paths_.size() * SEGMENT_LENGTH);
  qInfo() << "seeking to " << ts;

  seek_ts_ = ts;
  current_segment_ = ts / SEGMENT_LENGTH;
}

// threads

void Replay::segmentQueueThread() {
  // maintain the segment window
  while (!exit_) {
    for (int i = 0; i < log_paths_.size(); i++) {
      int start_idx = std::max(current_segment_ - BACKWARD_SEGS, 0);
      int end_idx = std::min(current_segment_ + FORWARD_SEGS, log_paths_.size());
      if (i >= start_idx && i <= end_idx) {
        addSegment(i);
      } else {
        removeSegment(i);
      }
    }
    QThread::msleep(100);
  }
}

void Replay::cameraThread() {
  vipc_server_->start_listener();

  while (!exit_) {
    std::tuple<int, FrameType, uint32_t> frame;
    if (!frame_queue_.try_pop(frame, 50)) continue;

    auto [seg_id, frame_type, frame_id] = frame;
    // search frame's encodIdx in adjacent segments_.
    int search_in[] = {seg_id, seg_id - 1, seg_id + 1};
    for (auto i : search_in) {
      if (auto f = getFrameSegment(i, frame_type, frame_id)) {
        auto [seg, fid] = *f;
        FrameReader *frm = seg->frames[frame_type];
        uint8_t *data = nullptr;
        if (frm && (data = frm->get(fid))) {
          VisionIpcBufExtra extra = {};
          VisionBuf *buf = vipc_server_->get_buffer(frm->stream_type);
          memcpy(buf->addr, data, frm->getRGBSize());
          vipc_server_->send(buf, &extra, false);
        } else {
          qDebug() << "failed to get frame " << frame_id << " from segment " << i;
        }
        break;
      }
    }
  }

  delete vipc_server_;
  vipc_server_ = nullptr;
}

void Replay::keyboardThread() {
  char c;
  while (!exit_) {
    c = getch();
    if (c == '\n') {
      printf("Enter seek request: ");
      std::string r;
      std::cin >> r;

      try {
        if (r[0] == '#') {
          r.erase(0, 1);
          seekTime(std::stoi(r) * 60);
        } else {
          seekTime(std::stoi(r));
        }
      } catch (std::invalid_argument) {
        qDebug() << "invalid argument";
      }
      getch();  // remove \n from entering seek
    } else if (c == 'm') {
      seekTime(current_ts_ + 60);
    } else if (c == 'M') {
      seekTime(current_ts_ - 60);
    } else if (c == 's') {
      seekTime(current_ts_ + 10);
    } else if (c == 'S') {
      seekTime(current_ts_ - 10);
    } else if (c == 'G') {
      seekTime(0);
    }
  }
}

void Replay::streamThread() {
  QElapsedTimer timer;
  timer.start();

  seekTime(0);
  uint64_t route_start_ts = 0;
  int64_t last_print = 0;
  while (!exit_) {
    std::shared_ptr<Segment> seg = getSegment(current_segment_);
    if (!seg) {
      qDebug() << "waiting for events";
      QThread::msleep(100);
      continue;
    }

    if (vipc_server_ == nullptr) {
      startVipcServer(seg.get());
    }
    const Events &events = seg->log->events();

    // TODO: use initData's logMonoTime
    if (route_start_ts == 0) {
      route_start_ts = events.firstKey();
    }

    uint64_t t0 = route_start_ts + (seek_ts_ * 1e9);
    qDebug() << "unlogging at" << (t0 - route_start_ts) / 1e9;

    auto eit = events.lowerBound(t0);
    uint64_t t0r = timer.nsecsElapsed();
    int current_seek_ts_ = seek_ts_;
    while (!exit_ && current_seek_ts_ == seek_ts_ && eit != events.end()) {
      cereal::Event::Reader e = (*eit)->msg.getRoot<cereal::Event>();
      std::string type;
      KJ_IF_MAYBE(e_, static_cast<capnp::DynamicStruct::Reader>(e).which()) {
        type = e_->getProto().getName();
      }

      uint64_t tm = e.getLogMonoTime();
      current_ts_ = std::max(tm - route_start_ts, (unsigned long)0) / 1e9;

      if (socks_.find(type) != socks_.end()) {
        if (std::abs(current_ts_ - last_print) > 5.0) {
          last_print = current_ts_;
          qInfo() << "at " << last_print << "| segment:" << seg->id;
        }

        // keep time
        long etime = tm - t0;
        long rtime = timer.nsecsElapsed() - t0r;
        long us_behind = ((etime - rtime) * 1e-3) + 0.5;
        if (us_behind > 0 && us_behind < 1e6) {
          QThread::usleep(us_behind);
          //qDebug() << "sleeping" << us_behind << etime << timer.nsecsElapsed();
        }

        // publish frames
        if (e.which() == cereal::Event::ROAD_CAMERA_STATE) {
          frame_queue_.push({seg->id, RoadCamFrame, e.getRoadCameraState().getFrameId()});
        } else if (e.which() == cereal::Event::DRIVER_CAMERA_STATE) {
          frame_queue_.push({seg->id, DriverCamFrame, e.getDriverCameraState().getFrameId()});
        } else if (e.which() == cereal::Event::WIDE_ROAD_CAMERA_STATE) {
          frame_queue_.push({seg->id, WideRoadCamFrame, e.getWideRoadCameraState().getFrameId()});
        }

        // publish msg
        if (sm_ == nullptr) {
          const auto bytes = (*eit)->words.asBytes();
          pm_->send(type.c_str(), (capnp::byte *)bytes.begin(), bytes.size());
        } else {
          sm_->update_msgs(nanos_since_boot(), {{type, e}});
        }
      }

      ++eit;
    }

    if (current_seek_ts_ == seek_ts_ && eit == events.end()) {
      // move to the next segment
      current_segment_ += 1;
      qDebug() << "move to next segment " << current_segment_;
      seek_ts_ = current_ts_.load();
    } else {
    }
  }
}
