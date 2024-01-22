for channel_info in "${all_channels[@]}"; do
  IFS=',' read -r channel_name channel_group channel_url <<< "$channel_info"
  live_status=$(yt-dlp --print live "$channel_url")
  
  if [ "$live_status" = "true" ]; then
    echo "Live stream found! Added to $channel_name.m3u8"
    touch ./$channel_name/$channel_name.m3u8
    {
      echo "#EXTM3U"
      echo "#EXT-X-VERSION:3"
      echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000"
      yt-dlp --print urls "$channel_url/live"
    } | sudo tee ./$channel_name/$channel_name.m3u8 > /dev/null
  else
    schedule_time=$(yt-dlp --print scheduledStartTime "$channel_url")
    if [ "$schedule_time" != "NA" ]; then
      echo "This channel is not currently live. It will be live at $schedule_time (EST timezone)"
    else
      echo "This channel is not currently live."
    fi
  fi
done
