#!/bin/bash

# Function to get live URLs for a channel and append them to the corresponding .m3u8 file
get_channel_urls() {
    channel_name=$1
    directory=$2
    mkdir -p "$directory"
    touch "$directory/$channel_name.m3u8"

    # Check if the video is live or scheduled
    channel_url="https://www.youtube.com/@$channel_name/live"
    video_info_json=$(yt-dlp --print-json "$channel_url")
    video_status=$(echo "$video_info_json" | jq -r .status)

    if [ "$video_status" = "live" ]; then
        # Fetch live stream URL
        live_url=$(yt-dlp --print urls "$channel_url")

        # Append the live URL to the .m3u8 file
        echo "#EXTM3U" > "$directory/$channel_name.m3u8"
        echo "#EXT-X-VERSION:3" >> "$directory/$channel_name.m3u8"
        echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000" >> "$directory/$channel_name.m3u8"
        echo "$live_url" >> "$directory/$channel_name.m3u8"
    else
        echo "The video is not live or scheduled for $channel_name. Skipping..."
    fi
}
