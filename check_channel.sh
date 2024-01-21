#!/bin/bash

# Function to get live stream URLs for a channel
get_channel_urls() {
  local channel_name="$1"
  local output_path="$2"

  mkdir -p "$output_path"
  touch "$output_path/$channel_name.m3u8"
  cat > "$output_path/$channel_name.m3u8" <<EOL
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
$(yt-dlp --print urls "https://www.youtube.com/@$channel_name/live")
EOL
}
