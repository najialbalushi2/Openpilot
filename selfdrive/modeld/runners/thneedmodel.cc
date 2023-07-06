#include "selfdrive/modeld/runners/thneedmodel.h"

#include <cassert>
#include <cstring>

#include "common/swaglog.h"

ThneedModel::ThneedModel(const std::string path, float *_output, size_t _output_size, int runtime, bool luse_tf8, cl_context context) {
  thneed = new Thneed(true, context);
  thneed->load(path.c_str());
  thneed->clexec();

  recorded = false;
  output = _output;
}

void ThneedModel::addInput(const std::string name, float *buffer, int size) {
  inputs.push_back(ModelInput(name, buffer, size));
}

void ThneedModel::setInputBuffer(const std::string name, float *buffer, int size) {
  for (auto &input : inputs) {
    if (name == input.name) {
      assert(input.size == size || input.size == 0);
      input.buffer = buffer;
      input.size = size;
      return;
    }
  }
  LOGE("Tried to update input `%s` but no input with this name exists", name.c_str());
}

void* ThneedModel::getCLBuffer(const std::string name) {
  int index = -1;
  for (int i = 0; i < inputs.size(); i++) {
    if (name == inputs[i].name) {
      index = i;
      break;
    }
  }

  if (index == -1) {
    LOGE("Tried to get CL buffer for input `%s` but no input with this name exists", name.c_str());
    return nullptr;
  }

  if (thneed->input_clmem.size() >= inputs.size()) {
    return &thneed->input_clmem[inputs.size() - index - 1];
  } else {
    return nullptr;
  }
}

void ThneedModel::execute() {
  if (!recorded) {
    thneed->record = true;
    float *input_buffers[inputs.size()];
    for (int i = 0; i < inputs.size(); i++) {
      input_buffers[inputs.size() - i - 1] = inputs[i].buffer;
    }

    thneed->copy_inputs(input_buffers);
    thneed->clexec();
    thneed->copy_output(output);
    thneed->stop();

    recorded = true;
  } else {
    float *input_buffers[inputs.size()];
    for (int i = 0; i < inputs.size(); i++) {
      input_buffers[inputs.size() - i - 1] = inputs[i].buffer;
    }
    thneed->execute(input_buffers, output);
  }
}
