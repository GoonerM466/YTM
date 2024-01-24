import os
import datetime
import yt_dlp

def fetch_m3u8(channel_name, group, channel_url):
    print(f"Fetching m3u8 for {channel_name}...")

    output_folder = "./current_channels/{}/".format(group)
    output_file = "{}{}.m3u8".format(output_folder, channel_name)

    os.makedirs(output_folder, exist_ok=True)

    # Remove extra "/" from the channel URL
    channel_url = channel_url.rstrip('/')

    ydl_opts = {
        'quiet': False,  # Set to True if you want less console output from yt-dlp
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info("{}/live".format(channel_url), download=False)
            video_id = info_dict.get('video_id', None)

            if video_id:
                m3u8_url = "https://www.youtube.com/watch?v={}&ab_channel={}".format(video_id, channel_name)
            else:
                m3u8_url = None

            with open(output_file, 'w') as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:3\n")
                f.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n")
                if m3u8_url:
                    f.write("{}\n".format(m3u8_url))

        print(f"m3u8 for {channel_name} fetched successfully.")
        return m3u8_url

    except yt_dlp.utils.ExtractorError as e:
        print(f"Error fetching m3u8 for {channel_name}: {e}")
        return None

def update_live_status(channels):
    print("Updating live status...")

    live_status_file = "live_status.txt"
    with open(live_status_file, 'w') as f:
        pass

    current_datetime = datetime.datetime.utcnow().strftime('%a %b %d %H:%M:%S UTC %Y')
    with open(live_status_file, 'a') as f:
        for channel_name, live_status in channels.items():
            f.write("{} - {} - {}\n".format(channel_name, live_status, current_datetime))

    print("Live status updated successfully.")

def main():
    print("Fetching m3u8 for all channels...")

    channels_file = "channels.txt"
    channels = {}

    with open(channels_file, 'r') as f:
        for line in f:
            channel_name, group, channel_url = line.strip().split(', ')
            try:
                m3u8_url = fetch_m3u8(channel_name, group, channel_url)
                channels[channel_name] = "Live" if m3u8_url else "Not Live"
            except Exception as e:
                print(f"Error processing {channel_name}: {e}")
                channels[channel_name] = "Not Live"

    update_live_status(channels)

    print("Script execution completed.")

if __name__ == "__main__":
    main()
