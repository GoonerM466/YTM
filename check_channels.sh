#!/bin/bash

# Read channels from current_channels.txt and update/create the corresponding m3u8 files

while IFS=, read -r channel_name group channel_url; do
    echo "Processing ${channel_name} (${group})"
    echo "URL: ${channel_url}"

    m3u8_file="./${group,,}/${channel_name}.m3u8"
    mkdir -p "${group,,}"

    # Use yt-dlp to dump pages and grep for the live stream URL
    video_url=$(yt-dlp --dump-pages "${channel_url}" | grep -oP '(?<=ytplayer.config = ).*?(?=;</script>)' | jq -r '.args.player_response.streamingData.hlsManifestUrl')

    cat >"${m3u8_file}" <<EOL
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
${video_url}
EOL

done < current_channels.txt
