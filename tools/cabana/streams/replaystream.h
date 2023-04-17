#pragma once

#include "tools/cabana/streams/abstractstream.h"
#include "tools/cabana/settings.h"

class ReplayStream : public AbstractStream {
  Q_OBJECT

public:
  ReplayStream(QObject *parent);
  ~ReplayStream();
  bool loadRoute(const QString &route, const QString &data_dir, uint32_t replay_flags = REPLAY_FLAG_NONE);
  bool eventFilter(const Event *event);
  void seekTo(double ts) override { replay->seekTo(std::max(double(0), ts), false); };
  inline QString routeName() const override { return replay->route()->name(); }
  inline QString carFingerprint() const override { return replay->carFingerprint().c_str(); }
  inline VisionStreamType visionStreamType() const override { return replay->hasFlag(REPLAY_FLAG_ECAM) ? VISION_STREAM_WIDE_ROAD : VISION_STREAM_ROAD; }
  inline double totalSeconds() const override { return replay->totalSeconds(); }
  inline double routeStartTime() const override { return replay->routeStartTime() / (double)1e9; }
  inline double currentSec() const override { return replay->currentSeconds(); }
  inline QDateTime currentDateTime() const override { return replay->currentDateTime(); }
  inline const Route *route() const override { return replay->route(); }
  inline void setSpeed(float speed) override { replay->setSpeed(speed); }
  inline bool isPaused() const override { return replay->isPaused(); }
  void pause(bool pause) override;
  const std::vector<Event*> *rawEvents() const override { return replay->events(); }
  inline const std::vector<std::tuple<int, int, TimelineType>> getTimeline() override { return replay->getTimeline(); }

private:
  void mergeSegments();
  std::unique_ptr<Replay> replay = nullptr;
  std::set<int> processed_segments;
};

class OpenReplayWidget : public AbstractOpenStreamWidget {
  Q_OBJECT

public:
  OpenReplayWidget(AbstractStream **stream, QWidget *parent);
  bool open() override;
  QString title() override { return tr("Replay"); }
  inline bool failedToLoad() const { return failed_to_load; }

private:
  QLineEdit *route_edit;
  QComboBox *choose_video_cb;
  bool failed_to_load = false;
};


class OpenRouteDialog : public QDialog {
  Q_OBJECT

 public:
  OpenRouteDialog(QWidget *parent);
  inline bool failedToLoad() const { return replay_widget->failedToLoad(); }

 private:
  OpenReplayWidget *replay_widget;
};
