#define CATCH_CONFIG_MAIN
#include "catch2/catch.hpp"
#include "selfdrive/common/util.h"
#include "selfdrive/proclogd/proclog.h"

TEST_CASE("Parser::pidStat") {
  std::string self_stat = util::read_file("/proc/self/stat");
  SECTION("self stat") {
    auto stat = Parser::pidStat(self_stat);
    REQUIRE((stat && stat->name == "test_proclog" && stat->pid == getpid()));
  }
  SECTION("name with space") {
    std::string from = "(test_proclog)";
    size_t start_pos = self_stat.find(from);
    self_stat.replace(start_pos, from.length(), "(test proclog)");
    auto stat = Parser::pidStat(self_stat);
    REQUIRE((stat && stat->name == "test proclog" && stat->pid == getpid()));
  }
  SECTION("more") {
    auto stat = Parser::pidStat(self_stat + " 1 2 3 4 5");
    REQUIRE(stat);
    REQUIRE(stat->name == "test_proclog" && stat->pid == getpid());
  }
  SECTION("less") {
    auto stat = Parser::pidStat(self_stat.substr(0, 20));
    REQUIRE(!stat);
  }
  SECTION("from empty string") {
    auto stat = Parser::pidStat("");
    REQUIRE(!stat);
  }
}

TEST_CASE("Parser::procStat") {
  SECTION("from string") {
    std::string stat = "cpu 0 0 0 0 0 0 0 0 0\ncpu0 1 2 3 4 5 6 7 8\ncpu1 1 2 3 4 5 6 7 8\nothers";
    std::istringstream stream(stat);
    auto stats = Parser::procStat(stream);
    REQUIRE(stats.size() == 2);
    REQUIRE((stats[0].id == 0 && stats[0].utime == 1 && stats[0].ntime == 2));
    REQUIRE((stats[1].id == 1 && stats[0].utime == 1 && stats[0].ntime == 2));
  }
  SECTION("from /proc/stat") {
    std::istringstream stream(util::read_file("/proc/stat"));
    auto stats = Parser::procStat(stream);
    REQUIRE(stats.size() == sysconf(_SC_NPROCESSORS_ONLN));
    for (int i = 0; i < stats.size(); ++i) {
      REQUIRE(stats[i].id == i);
    }
  }
  SECTION("from empty string") {
    std::istringstream stream("");
    REQUIRE(Parser::procStat(stream).empty());
  }
}

TEST_CASE("Parser::memInfo") {
  SECTION("from string") {
    std::istringstream stream("MemTotal:    1024 kb\nMemFree:    10 kb\n");
    auto stats = Parser::memInfo(stream);
    REQUIRE((stats["MemTotal:"] = 1024 * 1024 && stats["MemFree:"] == 1024 * 10));
  }
  SECTION("from wrong string") {
    std::istringstream stream("MemTotal:   kb \nMemFree:    10 kb\n");
    auto stats = Parser::memInfo(stream);
    REQUIRE(stats.find("MemTotal:") == stats.end());
    REQUIRE(stats["MemFree:"] == 1024 * 10);
  }
  SECTION("from /proc/ProcStat") {
    std::istringstream stream(util::read_file("/proc/meminfo"));
    auto stats = Parser::memInfo(stream);
    std::string keys[] = {"MemTotal:", "MemFree:", "MemAvailable:", "Buffers:", "Cached:", "Active:", "Inactive:", "Shmem:"};
    for (auto &key : keys) {
      REQUIRE(stats.find(key) != stats.end());
    }
  }
  SECTION("from empty string") {
    std::istringstream stream("");
    auto stats = Parser::memInfo(stream);
    REQUIRE(stats.empty());
  }
}

TEST_CASE("Parser::cmdline") {
  SECTION("normal") {
    std::string str("a\0b\0c\0", 7);
    auto cmds = Parser::cmdline(str);
    REQUIRE(cmds.size() == 3);
    REQUIRE(cmds[0] == "a");
    REQUIRE(cmds[1] == "b");
    REQUIRE(cmds[2] == "c");
  }
  SECTION("multiple null") {
    std::string str("a\0\0b\0", 6);
    auto cmds = Parser::cmdline(str);
    REQUIRE(cmds.size() == 3);
    REQUIRE(cmds[0] == "a");
    REQUIRE(cmds[1] == "");
    REQUIRE(cmds[2] == "b");
  }
  SECTION("multiple null terminate") {
    std::string str("a\0b\0c\0\0\0", 9);
    auto cmds = Parser::cmdline(str);
    REQUIRE(cmds[0] == "a");
    REQUIRE(cmds[1] == "b");
    REQUIRE(cmds[2] == "c");
  }
  SECTION("from empty string") {
    auto cmds = Parser::cmdline("");
    REQUIRE(cmds.empty());
  }
}

TEST_CASE("buildProcLogerMessage") {
  MessageBuilder msg;
  buildProcLogerMessage(msg);

  kj::Array<capnp::word> buf = capnp::messageToFlatArray(msg);
  capnp::FlatArrayMessageReader reader(buf);
  auto log = reader.getRoot<cereal::Event>().getProcLog();

  // test cereal::ProcLog::CPUTimes
  auto cpu_times = log.getCpuTimes();
  REQUIRE(cpu_times.size() == sysconf(_SC_NPROCESSORS_ONLN));
  REQUIRE(cpu_times[cpu_times.size() - 1].getCpuNum() == cpu_times.size() - 1);

  // test cereal::ProcLog::Mem
  auto mem = log.getMem();
  // first & last items we read from /proc/mem
  REQUIRE(mem.getTotal() > 0);
  REQUIRE(mem.getShared() > 0);

  auto procs = log.getProcs();
  REQUIRE(procs.size() > 1);

  // test if self in procs
  bool found_self = false;
  int self_pid = getpid();
  for (auto p : procs) {
    if (p.getPid() == self_pid) {
      REQUIRE(p.getName() == "test_proclog");
      REQUIRE(p.getNumThreads() == 1);
      found_self = true;
      break;
    }
  }
  REQUIRE(found_self == true);
}
