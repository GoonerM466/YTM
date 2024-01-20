#!/bin/bash

# Skip the first two lines
sed -i '1,2d' youtube_channel_info.txt

while IFS= read -r line; do
  # Extracting values from the line
  channel_name=$(echo "$line" | cut -d '|' -f 1 | tr -d ' ')
  group_name=$(echo "$line" | cut -d '|' -f 2 | tr -d ' ')
  logo=$(echo "$line" | cut -d '|' -f 3 | tr -d ' ')
  tvg_id=$(echo "$line" | cut -d '|' -f 4 | tr -d ' ')

  # Reading the next line for the channel URL
  read -r channel_url

  # Appending new entry to ytm.yml
  echo "- name: $channel_name
    run: |
      touch ./$group_name/$channel_name.m3u8
      sudo cat > ./$group_name/$channel_name.m3u8 <<EOL
      #EXTM3U
      #EXT-X-VERSION:3
      #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
      \$(yt-dlp --print urls $channel_url)
      EOL" >> .github/workflows/ytm.yml
done < youtube_channel_info.txt
