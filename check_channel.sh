#!/bin/bash

# Function to get live stream URLs for a channel
get_live_urls() {
  local channel_name="$1"
  local output_path="$2"

  mkdir -p "$output_path"
  touch "$output_path/$channel_name.m3u8"

  echo "Fetching live stream URLs for $channel_name"

  # Check if the video is live or scheduled
  channel_url="https://www.youtube.com/@$channel_name/live"
  video_info_json=$(yt-dlp --print-json "$channel_url")
  video_status=$(echo "$video_info_json" | jq -r '.status')

  if [ "$video_status" == "live" ]; then
    urls=$(yt-dlp --print urls "$channel_url" 2>&1)
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

# Call the function for each channel listed in the workflow
get_live_urls "$1" "$2"

echo "Script execution completed"
