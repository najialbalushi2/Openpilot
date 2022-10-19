#pragma once

#include <QAbstractTableModel>
#include <QComboBox>
#include <QDialog>
#include <QTableView>
#include <QTextEdit>

#include "tools/cabana/canmessages.h"

class LoadDBCDialog : public QDialog {
  Q_OBJECT

public:
  LoadDBCDialog(QWidget *parent);
  QTextEdit *dbc_edit;
};

class MessageListModel : public QAbstractTableModel {
Q_OBJECT

public:
  MessageListModel(QObject *parent) : QAbstractTableModel(parent) {}
  QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;
  int columnCount(const QModelIndex &parent = QModelIndex()) const override { return 4; }
  QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
  int rowCount(const QModelIndex &parent = QModelIndex()) const override { return row_count; }
  void updateState();

private:
  int row_count = 0;
};

class MessagesWidget : public QWidget {
  Q_OBJECT

public:
  MessagesWidget(QWidget *parent);
  inline QString currentMessageId() const { return current_msg_id; }
  inline void setCurrentMessageId(const QString &msg_id) { current_msg_id = msg_id; }

public slots:
  void openDBC(const QString &dbc_file);
  void loadFromPaste();

signals:
  void msgSelectionChanged(const QString &message_id);

protected:
  void restoreLastSelected();
  QString current_msg_id;
  QTableView *table_widget;
  QComboBox *dbc_combo;
  MessageListModel *model;
};
