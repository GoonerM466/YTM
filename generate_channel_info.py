name: Get YouTube Live m3u8

on:
  schedule:
    - cron: '45 0/2 * * *'
  workflow_dispatch:
  workflow_run:
    workflows:
      - "New Channel Scrape Workflow"
      - "Delete M3U8 Files"
    types:
      - completed

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: config
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
    - name: Install yt-dlp
      run: |
        curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
        chmod a+rx /usr/local/bin/yt-dlp
    - name: Delay for 10 seconds
      run: sleep 10

    - name: Pull latest changes
      run: git pull origin main

    - name: Rebase changes
      run: git pull --rebase origin main

    - name: Create current_channels directory
      run: mkdir -p ./current_channels

    - name: Read channel information from current_channels.txt
      run: |
        # Clear the contents of live_status.txt
        echo "" > live_status.txt

        while IFS=, read -r channel_name group channel_url; do
          # Modify channel_name: remove spaces and trim to 3 words
          channel_name=$(echo "$channel_name" | sed -E 's/[^a-zA-Z0-9]+/-/g' | awk '{print $1; for(i=2;i<=3;i++) {if($i!="") {printf "-%s", $i}}}')
          mkdir -p "./current_channels/$group"
          touch "./current_channels/$group/$channel_name.m3u8"
          {
            echo "#EXTM3U"
            echo "#EXT-X-VERSION:3"
            echo "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000"
            yt-dlp --print urls "$channel_url"
          } | sudo tee "./current_channels/$group/$channel_name.m3u8" >/dev/null
          
          # Check if the channel is live
          live_status="Not Live"
          if yt-dlp --print is_live "$channel_url" | grep -q "True"; then
            live_status="Live"
            echo "$channel_name is live! Updating $channel_name.m3u8 with current live stream!"
          fi
          
          # Append live status information to live_status.txt
          echo "$channel_name - $live_status - $(date)" >> live_status.txt
        done < current_channels.txt

    - name: git add
      run: |
        git add -A
        ls -la
    - name: commit & push
      run: |
        git diff --cached --quiet || git commit -m Updated
        git push origin main
