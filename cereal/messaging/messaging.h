#pragma once

#include <algorithm>
#include <cstddef>
#include <map>
#include <string>
#include <vector>
#include <utility>
#include <time.h>

#include <capnp/serialize.h>

#include "cereal/gen/cpp/log.capnp.h"
#include "msgq/ipc.h"

#ifdef __APPLE__
#define CLOCK_BOOTTIME CLOCK_MONOTONIC
#endif

#define MSG_MULTIPLE_PUBLISHERS 100


class SubMaster {
public:
  SubMaster(const std::vector<const char *> &service_list, const std::vector<const char *> &poll = {},
            const char *address = nullptr, const std::vector<const char *> &ignore_alive = {});
  void update(int timeout = 1000);
  void update_msgs(uint64_t current_time, const std::vector<std::pair<std::string, cereal::Event::Reader>> &messages);
  inline bool allAlive(const std::vector<const char *> &service_list = {}) { return all_(service_list, false, true); }
  inline bool allValid(const std::vector<const char *> &service_list = {}) { return all_(service_list, true, false); }
  inline bool allAliveAndValid(const std::vector<const char *> &service_list = {}) { return all_(service_list, true, true); }
  void drain();
  ~SubMaster();

  uint64_t frame = 0;
  bool updated(const char *name) const;
  bool alive(const char *name) const;
  bool valid(const char *name) const;
  uint64_t rcv_frame(const char *name) const;
  uint64_t rcv_time(const char *name) const;
  cereal::Event::Reader &operator[](const char *name) const;

private:
  bool all_(const std::vector<const char *> &service_list, bool valid, bool alive);
  Poller *poller_ = nullptr;
  struct SubMessage;
  std::map<SubSocket *, SubMessage *> messages_;
  std::map<std::string, SubMessage *> services_;
};

class MessageBuilder : public capnp::MallocMessageBuilder {
public:
  MessageBuilder() = default;

  cereal::Event::Builder initEvent(bool valid = true) {
    cereal::Event::Builder event = initRoot<cereal::Event>();
    struct timespec t;
    clock_gettime(CLOCK_BOOTTIME, &t);
    uint64_t current_time = t.tv_sec * 1000000000ULL + t.tv_nsec;
    event.setLogMonoTime(current_time);
    event.setValid(valid);
    return event;
  }

  kj::ArrayPtr<capnp::byte> toBytes() {
    heapArray_ = capnp::messageToFlatArray(*this);
    return heapArray_.asBytes();
  }

  size_t getSerializedSize() {
    return capnp::computeSerializedSizeInWords(*this) * sizeof(capnp::word);
  }

  int serializeToBuffer(unsigned char *buffer, size_t buffer_size) {
    size_t serialized_size = getSerializedSize();
    if (serialized_size > buffer_size) { return -1; }
    kj::ArrayOutputStream out(kj::ArrayPtr<capnp::byte>(buffer, buffer_size));
    capnp::writeMessage(out, *this);
    return serialized_size;
  }

private:
  kj::Array<capnp::word> heapArray_;
};

class PubMaster {
public:
  PubMaster(const std::vector<const char *> &service_list);
  inline int send(const char *name, capnp::byte *data, size_t size) { return sockets_.at(name)->send((char *)data, size); }
  int send(const char *name, MessageBuilder &msg);
  ~PubMaster();

private:
  std::map<std::string, PubSocket *> sockets_;
};

class AlignedBuffer {
public:
  kj::ArrayPtr<const capnp::word> align(const char *data, const size_t size) {
    const size_t word_count = size / sizeof(capnp::word);

    // Check if data is already aligned
    if (reinterpret_cast<uintptr_t>(data) % alignof(capnp::word) == 0) {
      return kj::arrayPtr(reinterpret_cast<const capnp::word *>(data), word_count);
    }

    // Data is not aligned, perform alignment
    if (aligned_buf.size() < word_count) {
      aligned_buf = kj::heapArray<capnp::word>(std::max(word_count, size_t(512)));
    }
    memcpy(aligned_buf.begin(), data, word_count * sizeof(capnp::word));
    return aligned_buf.slice(0, word_count);
  }

  inline kj::ArrayPtr<const capnp::word> align(Message *m) {
    return align(m->getData(), m->getSize());
  }

private:
  kj::Array<capnp::word> aligned_buf;
};
