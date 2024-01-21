#!/bin/bash

channel_name=$1
output_dir=$2

mkdir -p "$output_dir"
touch "$output_dir/$channel_name.m3u8"

start_time=$(date +%s)
video_count=0
max_retries=1
retry_count=0

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

  if ! yt-dlp --print urls "https://www.youtube.com/@$channel_name/streams"; then
    error_message=$(yt-dlp "https://www.youtube.com/@$channel_name/streams" 2>&1)
    if [[ $error_message == *"HTTP Error 429: Too Many Requests"* ]]; then
      echo "Encountered 'HTTP Error 429: Too Many Requests'. Retrying ($((retry_count + 1)) of $max_retries)."
      retry_count=$((retry_count + 1))
      if [ $retry_count -gt $max_retries ]; then
        echo "Maximum retries reached. Stopping search for the channel."
        break
      fi
      sleep 20
      continue
    else
      echo "Error: $error_message"
      echo "Error while checking the channel. Moving on to the next channel."
      break
    fi
  fi

  current_time=$(date +%s)
  elapsed_time=$((current_time - start_time))
  echo "Elapsed time: $elapsed_time seconds"

  if [ $elapsed_time -ge 60 ]; then
    echo "Time limit reached. Moving on to the next channel."
    break
  fi

  video_count=$((video_count + 1))
done
