#pragma once

#include <map>
#include <QList>
#include <QMetaType>
#include <QObject>
#include <QString>
#include <QSet>
#include <QDebug>

#include "tools/cabana/dbc.h"
#include "tools/cabana/dbcfile.h"

typedef QSet<uint8_t> SourceSet;
const SourceSet SOURCE_ALL = {};

class DBCManager : public QObject {
  Q_OBJECT

public:
  DBCManager(QObject *parent) {}
  ~DBCManager() {}
  bool open(SourceSet s, const QString &dbc_file_name, QString *error = nullptr);
  bool open(SourceSet s, const QString &name, const QString &content, QString *error = nullptr);
  void closeAll();
  QString generateDBC();

  void addSignal(const MessageId &id, const cabana::Signal &sig);
  void updateSignal(const MessageId &id, const QString &sig_name, const cabana::Signal &sig);
  void removeSignal(const MessageId &id, const QString &sig_name);

  void updateMsg(const MessageId &id, const QString &name, uint32_t size);
  void removeMsg(const MessageId &id);

  std::map<MessageId, cabana::Msg> getMessages(uint8_t source);
  const cabana::Msg *msg(const MessageId &id) const;
  const cabana::Msg* msg(uint8_t source, const QString &name);

  QStringList signalNames() const;
  int msgCount() const;

private:
  std::optional<std::pair<SourceSet, DBCFile*>> findDBCFile(const MessageId &id) const;
  SourceSet sources;
  QList<std::pair<SourceSet, DBCFile*>> dbc_files;

public slots:
  void updateSources(const SourceSet &s);

signals:
  void signalAdded(MessageId id, const cabana::Signal *sig);
  void signalRemoved(const cabana::Signal *sig);
  void signalUpdated(const cabana::Signal *sig);
  void msgUpdated(MessageId id);
  void msgRemoved(MessageId id);
  void DBCFileChanged();
};

DBCManager *dbc();

inline QString msgName(const MessageId &id) {
  auto msg = dbc()->msg(id);
  return msg ? msg->name : UNTITLED;
}
