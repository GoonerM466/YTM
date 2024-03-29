import os
import datetime
import yt_dlp

def fetch_ts_segments(channel_name, group, channel_url):
    print(f"Fetching TS segments for {channel_name}...")

    output_folder = "./current_channels/{}/".format(group)
    output_file = "{}{}.m3u8".format(output_folder, channel_name)

    os.makedirs(output_folder, exist_ok=True)

    # Touch the file to create it if it doesn't exist
    open(output_file, 'a').close()

    # Remove extra "/" from the channel URL
    channel_url = channel_url.rstrip('/')

    ydl_opts = {
        'quiet': False,  # Set to True if you want less console output from yt-dlp
        'format': 'best',  # Selects the best available quality
        'outtmpl': output_file,  # Output file template
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info("{}/live".format(channel_url), download=False)
            m3u8_url = next((format['url'] for format in info_dict.get('formats', []) if format.get('url') and format.get('protocol') == 'm3u8'), None)

            if m3u8_url:
                with open(output_file, 'w') as f:
                    f.write("#EXTM3U\n")
                    f.write("#EXT-X-VERSION:3\n")
                    f.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n")
                    f.write("{}\n".format(m3u8_url))
                print(f"TS segments for {channel_name} fetched successfully.")
                return output_file
            else:
                print(f"No live stream found for {channel_name}")
                return None

    except yt_dlp.utils.ExtractorError as e:
        print(f"Error fetching TS segments for {channel_name}: {e}")
        return None

def is_channel_live(channel_url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(channel_url, download=False)
            return info_dict.get('is_live', False)
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error checking if the channel is live: {e}")
        return False

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
    print("Fetching TS segments for all channels...")

    channels_file = "channels.txt"
    channels = {}

    with open(channels_file, 'r') as f:
        for line in f:
            channel_name, group, channel_url = line.strip().split(', ')
            try:
                m3u8_file = fetch_ts_segments(channel_name, group, channel_url)
                channels[channel_name] = "Live" if m3u8_file else "Not Live"
            except Exception as e:
                print(f"Error processing {channel_name}: {e}")
                channels[channel_name] = "Error"

    update_live_status(channels)

    print("Script execution completed.")

if __name__ == "__main__":
    main()
