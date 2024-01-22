channels_yaml=$(cat ytm.yaml)

for channel_info in "${channels_yaml[@]}"; do
  name=$(echo "$channel_info" | grep -oP 'name: \K.*')
  group=$(echo "$channel_info" | grep -oP 'group: \K.*')
  url=$(echo "$channel_info" | grep -oP 'url: \K.*')

  if live_status=$(yt-dlp --quiet --print live "$url" 2>/dev/null || echo "false"); then
    if [ "$live_status" = "true" ]; then
      echo "Live stream found for $name! Added to ./$group/$name.m3u8"
      mkdir -p ./$group  # Ensure the group directory exists
      touch ./$group/$name.m3u8
      {
        echo "#EXTM3U"
        echo "#EXT-X-VERSION:3"
        echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000"
        yt-dlp --quiet --print urls "$url/live" 2>/dev/null || echo "Error fetching live URLs for $name"
      } | sudo tee ./$group/$name.m3u8 > /dev/null
    else
      schedule_time=$(yt-dlp --quiet --print scheduledStartTime "$url" 2>/dev/null || echo "NA")
      if [ "$schedule_time" != "NA" ]; then
        echo "Channel $name is not currently live. It will be live at $schedule_time (EST timezone)"
      else
        echo "Channel $name is not currently live."
      fi
    fi
  else
    echo "Error checking live status for $name"
  fi
done
