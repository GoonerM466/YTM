import yt_dlp

def is_video_live(video_url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get('is_live', False)

def main():
    source_file = "VOD_to_fetch.txt"
    lines_to_remove = []

    with open(source_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            # Assuming the format is: $channel_name, $group, $video_url, $image_url
            video_url = line.split(',')[2].strip()
            if is_video_live(video_url):
                lines_to_remove.append(line)

    # Remove live video entries from the source file
    with open(source_file, 'w') as file:
        file.writelines(line for line in lines if line not in lines_to_remove)

if __name__ == "__main__":
    main()
