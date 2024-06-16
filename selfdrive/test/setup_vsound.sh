#!/bin/bash

{
  #start pulseaudio daemon
  sudo pulseaudio -D --no-cpu-limit=yes

  # create a virtual null audio and set it to default device
  sudo pactl load-module module-null-sink sink_name=virtual_audio
  sudo pactl set-default-sink virtual_audio

  export PULSE_SINK=virtual_audio
} > /dev/null 2>&1
