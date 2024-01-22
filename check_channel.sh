channels_yaml=$(cat ytm.yaml)

for channel_info in "${channels_yaml[@]}"; do
  name=$(echo "$channel_info" | cut -d':' -f1)
  group=$(echo "$channel_info" | grep -oP 'group: \K.*')
  url=$(echo "$channel_info" | grep -oP 'url: \K.*')

  live_status=$(yt-dlp --quiet --print live "$url" || echo "false")
  
  if [ "$live_status" = "true" ]; then
    echo "Live stream found! Added to $name.m3u8"
    touch ./$name/$name.m3u8
    {
      echo "#EXTM3U"
      echo "#EXT-X-VERSION:3"
      echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000"
      yt-dlp --quiet --print urls "$url/live" || echo "Error fetching live URLs"
    } | sudo tee ./$name/$name.m3u8 > /dev/null
  elif [ "$live_status" = "false" ]; then
    echo "This channel is not currently live."
  else
    schedule_time=$(yt-dlp --quiet --print scheduledStartTime "$url" || echo "NA")
    if [ "$schedule_time" != "NA" ]; then
      echo "This channel is not currently live. It will be live at $schedule_time (EST timezone)"
    else
      echo "Error checking live status for $name"
    fi
  fi
done
