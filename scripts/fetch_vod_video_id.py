import os
import yt_dlp

def extract_channel_info(line):
    parts = line.strip().split(', ')
    channel_name = parts[0]
    group = parts[1]
    channel_url = parts[2] + '/streams'
    return channel_name, group, channel_url

def get_recent_videos(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'playlist_items': 3,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return [entry['id'] for entry in info['entries']]

def main():
    source_file = 'current_channels.txt'
    output_file = 'VOD_to_fetch.txt'

    if not os.path.exists(source_file):
        print(f"Error: {source_file} does not exist.")
        return

    with open(source_file, 'r') as file:
        lines = file.readlines()

    if not lines:
        print(f"Error: {source_file} is empty.")
        return

    with open(output_file, 'w') as file:
        for line in lines:
            channel_name, group, channel_url = extract_channel_info(line)

            videos = get_recent_videos(channel_url)
            for video_id in videos:
                file.write(f"{video_id}, {group}, {channel_name}\n")

    print(f"Script executed successfully. Check {output_file} for results.")

if __name__ == "__main__":
    main()
