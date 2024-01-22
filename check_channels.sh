#!/bin/bash

# Replace YOUR_API_KEY with your actual YouTube API key
API_KEY="AIzaSyBztHpAhFSfGbFvIkPrcPE9HbhXjQo_tSc"

# Read channels from current_channels.txt and update/create the corresponding m3u8 files

while IFS=, read -r channel_name group channel_url; do
    echo "Processing ${channel_name} (${group})"
    echo "URL: ${channel_url}"

    m3u8_file="./${group,,}/${channel_name}.m3u8"
    mkdir -p "${group,,}"

    # Extract channel ID from the channel URL
    channel_id=$(echo "${channel_url}" | sed -n 's/.*\/\([^\/]*\)\/live.*/\1/p')

    # Use YouTube API to get live stream information
    video_url=$(curl -s "https://www.googleapis.com/youtube/v3/search?part=id&channelId=${channel_id}&eventType=live&type=video&key=${API_KEY}" | jq -r '.items[0].id.videoId')

    cat >"${m3u8_file}" <<EOL
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
https://www.youtube.com/watch?v=${video_url}
EOL

done < current_channels.txt

