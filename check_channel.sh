#!/bin/bash

channel_name=$1
output_dir=$2

mkdir -p "$output_dir"
touch "$output_dir/$channel_name.m3u8"

start_time=$(date +%s)
video_count=0
while true; do
  if yt-dlp --print urls "https://www.youtube.com/@$channel_name/streams" | grep -Eq 'This live event will begin in [0-9]+ (days|hours)'; then
    echo "Skipping scheduled live event. Moving on to the next channel."
    break
  fi

  # Check if there are any videos from the past
  if yt-dlp --print urls "https://www.youtube.com/@$channel_name/streams" | grep -Eq 'This live event has ended'; then
    echo "Found videos from the past. Moving on to the next channel."
    break
  fi

  if [ $video_count -ge 20 ]; then
    echo "Checked 20 videos, none are live. Moving on to the next channel."
    break
  fi

  if yt-dlp --print urls "https://www.youtube.com/@$channel_name/streams"; then
    break
  fi

  current_time=$(date +%s)
  elapsed_time=$((current_time - start_time))
  if [ $elapsed_time -ge 60 ]; then
    echo "Time limit reached. Moving on to the next channel."
    break
  fi

  video_count=$((video_count + 1))
done
