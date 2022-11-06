#pragma once

#include <QProgressBar>
#include <QSplitter>
#include <QStatusBar>

#include "tools/cabana/chartswidget.h"
#include "tools/cabana/detailwidget.h"
#include "tools/cabana/messageswidget.h"
#include "tools/cabana/videowidget.h"

class MainWindow : public QWidget {
  Q_OBJECT

public:
  MainWindow();
  void showStatusMessage(const QString &msg, int timeout = 0) { status_bar->showMessage(msg, timeout); }

signals:
  void showMessage(const QString &msg, int timeout);
  void updateProgressBar(uint64_t cur, uint64_t total, bool success);

protected:
  void updateDownloadProgress(uint64_t cur, uint64_t total, bool success);
  void setOption();

  VideoWidget *video_widget;
  MessagesWidget *messages_widget;
  DetailWidget *detail_widget;
  ChartsWidget *charts_widget;
  QSplitter *splitter;
  QVBoxLayout *r_layout;
  QProgressBar *progress_bar;
  QStatusBar *status_bar;
};
