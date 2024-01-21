#!/bin/bash

# Function to get live stream URLs for a channel
get_channel_urls() {
  local channel_name="$1"
  local output_path="$2"

  mkdir -p "$output_path"
  touch "$output_path/$channel_name.m3u8"

  echo "Checking live status for $channel_name"
  video_status=$(yt-dlp --print-json "https://www.youtube.com/@$channel_name/live" | jq -r '.status')

  if [ "$video_status" == "live" ]; then
    echo "Fetching live stream URLs for $channel_name"
    urls=$(yt-dlp --print urls "https://www.youtube.com/@$channel_name/live" 2>&1)
    echo "yt-dlp output:"
    echo "$urls"

    cat > "$output_path/$channel_name.m3u8" <<EOL
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
$urls
EOL

  else
    echo "$channel_name is not currently live."
  fi
}

echo "Script execution completed"
