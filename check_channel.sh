#!/bin/bash

function update_channel() {
  IFS=',' read -r channel_name channel_group channel_url <<< "$1"

  live_status=$(yt-dlp --print live "$channel_url")

  if [ "$live_status" = "true" ]; then
    echo "Live stream found for $channel_name! Added to $channel_name.m3u8 in $channel_group"
    mkdir -p ./$channel_group
    touch ./$channel_group/$channel_name.m3u8
    cat > ./$channel_group/$channel_name.m3u8 <<EOL
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
$(yt-dlp --print urls "$channel_url/live")
EOL
  else
    schedule_time=$(yt-dlp --print scheduledStartTime "$channel_url")
    echo "This channel is not currently live. It will be live at $schedule_time (EST timezone)"
  fi
}

# Example usage:
update_channel "beinsportshaber,spor,https://www.youtube.com/@beinsportsturkiye"
update_channel "AFCAsianCup,spor,https://www.youtube.com/@AFCAsianCup"
update_channel "talkSPORT,spor,https://www.youtube.com/@talkSPORT"
# Add more channels as needed
