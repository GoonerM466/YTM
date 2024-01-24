import os
import datetime
import yt_dlp

def fetch_m3u8(channel_name, group, channel_url):
    output_folder = "./current_channels/{}/".format(group)
    output_file = "{}{}.m3u8".format(output_folder, channel_name)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize yt-dlp options
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Look for m3u8 at channel_url/live
        info_dict = ydl.extract_info("{}/live".format(channel_url), download=False)
        video_id = info_dict.get('video_id', None)

        if video_id:
            # Construct URL using video_id
            m3u8_url = "https://www.youtube.com/watch?v={}&ab_channel={}".format(video_id, channel_name)
        else:
            m3u8_url = None

        # Write or update m3u8 file
        with open(output_file, 'w') as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-VERSION:3\n")
            f.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n")
            if m3u8_url:
                f.write("{}\n".format(m3u8_url))

    return m3u8_url

def update_live_status(channels):
    live_status_file = "live_status.txt"

    # Wipe the contents of live_status.txt
    with open(live_status_file, 'w') as f:
        pass

    # Write live status to live_status.txt
    current_datetime = datetime.datetime.utcnow().strftime('%a %b %d %H:%M:%S UTC %Y')
    with open(live_status_file, 'a') as f:
        for channel_name, live_status in channels.items():
            f.write("{} - {} - {}\n".format(channel_name, live_status, current_datetime))

def main():
    channels_file = "channels.txt"
    channels = {}

    # Read channels from channels.txt
    with open(channels_file, 'r') as f:
        for line in f:
            channel_name, group, channel_url = line.strip().split(', ')
            m3u8_url = fetch_m3u8(channel_name, group, channel_url)
            channels[channel_name] = "Live" if m3u8_url else "Not Live"

    # Update live status in live_status.txt
    update_live_status(channels)

if __name__ == "__main__":
    main()

