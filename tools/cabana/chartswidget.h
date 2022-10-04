#pragma once

#include <map>

#include <QLabel>
#include <QVBoxLayout>
#include <QWidget>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>

#include "tools/cabana/parser.h"

using namespace QtCharts;

class ChartWidget : public QWidget {
Q_OBJECT

public:
  ChartWidget(const QString &id, const QString &sig_name, QWidget *parent);
  inline QChart *chart() const { return chart_view->chart(); }

signals:
  void remove(const QString &id, const QString &sig_name);

protected:
  void updateState();
  void addData(const CanData &can_data, const Signal &sig);
  void zoom(float factor);

  float zoom_factor = 1.0;
  QString id;
  QString sig_name;
  int max_y = 0;
  int min_y = 0;
  QList<QPointF> data;
  QLabel *zoom_label;
  QChartView *chart_view = nullptr;
};

class ChartsWidget : public QWidget {
  Q_OBJECT

public:
  ChartsWidget(QWidget *parent = nullptr);
  inline bool hasChart(const QString &id, const QString &sig_name) {
    return charts.find(id+sig_name) != charts.end();
  }
  void addChart(const QString &id, const QString &sig_name);
  void removeChart(const QString &id, const QString &sig_name);
  void updateState();

protected:
  QVBoxLayout *main_layout;
  std::map<QString, ChartWidget *> charts;
};
