#!/bin/bash

channel_name=$1
output_dir=$2

mkdir -p "$output_dir"
touch "$output_dir/$channel_name.m3u8"

start_time=$(date +%s)
max_search_time=25
max_retries=1
retry_count=0

# Function to handle timeout
timeout_handler() {
  echo "Maximum search time reached. Stopping search for the channel."
  exit 1
}

# Set a trap to call the timeout handler
trap timeout_handler SIGALRM

# Use timeout to limit the execution time
timeout "$max_search_time"s bash -c "
while true; do
  # Reset the alarm on each iteration
  trap timeout_handler SIGALRM

  urls=$(yt-dlp --print urls 'https://www.youtube.com/@$channel_name/streams' 2>&1)
  
  if [ $? -ne 0 ]; then
    error_message=$(echo "$urls" | tail -n 1)
    
    if [[ $error_message == *"HTTP Error 429: Too Many Requests"* ]]; then
      echo 'Encountered HTTP Error 429: Too Many Requests. Retrying.'
      retry_count=$((retry_count + 1))
      
      if [ $retry_count -gt $max_retries ]; then
        echo 'Maximum retries reached. Stopping search for the channel.'
        break
      fi
      continue
    else
      echo "Error: $error_message"
      echo 'Error while checking the channel. Moving on to the next channel.'
      break
    fi
  fi
  
  if echo "$urls" | grep -Eq 'This live event will begin in [0-9]+ (days|hours)'; then
    echo 'Skipping scheduled live event. Moving on to the next channel.'
    break
  fi

  if echo "$urls" | grep -Eq 'This live event has ended'; then
    echo 'Found videos from the past. Moving on to the next channel.'
    break
  fi

  echo "$urls" > "$output_dir/$channel_name.m3u8"
  break
done
"
