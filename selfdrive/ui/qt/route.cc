#include "route.hpp"

#include <QDebug>

Route::Route(QString route_name_) : route_name(route_name_){
}

void Route::_get_segments_remote(){
  QString url = QString("https://api.commadotai.com/v1/route/" + route_name + "/files");

  RequestRepeater *repeater = new RequestRepeater(nullptr, url, 2, "ApiCache_Route");
  QObject::connect(repeater, SIGNAL(receivedResponse(QString)), this, SLOT(parseResponse(QString)));
}

void Route::parseResponse(QString response){
  response = response.trimmed();
  QJsonDocument doc = QJsonDocument::fromJson(response.toUtf8());

  if (doc.isNull()) {
    qDebug() << "JSON Parse failed on getting past drives statistics";
    return;
  }

	auto cams = doc["cameras"].toArray();
	auto logs = doc["logs"].toArray();

	for(int i = 0 ; i < cams.size() ; i++){
		segments.append(new RouteSegment(i, logs[i].toString(), cams[i].toString()));
	}

	for(auto i = 0 ; i < cams.size() ; i++)
		qDebug() << segments[i]->log_path;
}
