import os
import yt_dlp
import time

def search_youtube_and_get_channel_url(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    try:
        with ydl:
            search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
            entry = search_results.get('entries', [{}])[0]

            # Check if the video requires membership
            if entry.get('requires_membership'):
                print(f"Video requires membership. Skipping '{search_phrase}'.")
                return None

            channel_url = entry.get('channel_url', None)
            return channel_url
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading information from YouTube: {str(e)}")
        return None

def process_input_file(input_filename):
    output_filename = input_filename

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        # ... (existing code)

    if channel_url:
        live_channel_url = f"{channel_url.rstrip('/')}/live"
        updated_lines.append(f"Channel Name: {channel_name}\n")
        updated_lines.append(f"Channel URL: {live_channel_url}\n")
        # ... (remaining code)
    else:
        print(f"Could not find a channel URL for '{channel_name}'. Skipping.")
        return  # Skip processing for this channel

    with open(output_filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated information written to {output_filename}")

def process_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_live_channels.txt"):
            input_file_path = os.path.join(directory, filename)
            print(f"Processing file: {input_file_path}")
            process_input_file(input_file_path)

if __name__ == "__main__":
    # Directory where the files are located
    directory = "found_channels"
    
    # Process all files in the directory
    process_all_files_in_directory(directory)
