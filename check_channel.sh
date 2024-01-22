#!/usr/bin/bash -e

channels_yaml=$(cat ytm.yaml)

for channel_info in "${channels_yaml[@]}"; do
  name=$(echo "$channel_info" | grep -oP 'name: \K.*')
  group=$(echo "$channel_info" | grep -oP 'group: \K.*')
  url=$(echo "$channel_info" | grep -oP 'url: \K.*')

  live_status=$(yt-dlp --print live "$url" 2>/dev/null || true)

  if [[ $live_status == *"This live event will begin"* ]]; then
    schedule_time=$(yt-dlp --print scheduledStartTime "$url" 2>/dev/null || echo "NA")
    echo "This channel is not currently live. It will be live at $schedule_time (EST timezone)"
  elif [ "$live_status" = "true" ]; then
    echo "Live stream found! Added to $group/$name.m3u8"
    mkdir -p ./$group/$name
    touch ./$group/$name/$name.m3u8
    {
      echo "#EXTM3U"
      echo "#EXT-X-VERSION:3"
      echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000"
      yt-dlp --print urls "$url/live"
    } | sudo tee ./$group/$name/$name.m3u8 > /dev/null
  else
    echo "This channel is not currently live."
  fi
done
