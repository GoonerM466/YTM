#!/bin/bash

# Function to get live URLs for a channel and append them to the corresponding .m3u8 file
get_channel_urls() {
    channel_name=$1
    directory=$2
    mkdir -p "$directory"
    touch "$directory/$channel_name.m3u8"

    # Fetch live stream URL
    live_url=$(yt-dlp --print urls "https://www.youtube.com/@$channel_name/live")

    # Append the live URL to the .m3u8 file
    echo "#EXTM3U" > "$directory/$channel_name.m3u8"
    echo "#EXT-X-VERSION:3" >> "$directory/$channel_name.m3u8"
    echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000" >> "$directory/$channel_name.m3u8"
    echo "$live_url" >> "$directory/$channel_name.m3u8"
}

# Call the function for each channel listed in the workflow
get_live_urls "$1" "$2"

echo "Script execution completed"
