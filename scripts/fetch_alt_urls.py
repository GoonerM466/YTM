import os
import yt_dlp
import time

def search_youtube_and_get_channel_url(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    try:
        print(f"Searching for '{search_phrase}'...")
        search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
        entry = search_results.get('entries', [{}])[0]

        # Check if the video requires membership
        if entry.get('requires_membership'):
            print(f"Video requires membership. Skipping '{search_phrase}'.")
            return None

        channel_url = entry.get('channel_url', None)
        print(f"Found channel URL for '{search_phrase}': {channel_url}")
        return channel_url
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading information from YouTube: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in search_youtube_and_get_channel_url: {str(e)}")
        return None

def get_live_video_id(channel_url):
    ydl = yt_dlp.YoutubeDL()
    try:
        print(f"Getting live video ID for channel URL: {channel_url}...")
        channel_info = ydl.extract_info(channel_url, download=False)
        live_video_id = channel_info.get('url', '').split('=')[-1]
        print(f"Found live video ID: {live_video_id}")
        return live_video_id
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading information from YouTube: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in get_live_video_id: {str(e)}")
        return None

def process_input_file(input_filename):
    output_filename = "./program/alt_urls.txt"  # Change the output file path

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        if line.startswith("$search_term"):
            # Assuming the input file has the format $search_term, $group, $channel_url
            search_term, group, channel_url = line.strip().split(', ')
            search_term_lower = search_term.lower()
            print(f"Processing search term: {search_term}")

            new_channel_url = search_youtube_and_get_channel_url(search_term_lower)

            if new_channel_url:
                print(f"Got new channel URL: {new_channel_url}")
                live_channel_url = f"{new_channel_url.rstrip('/')}/live"
                live_video_id = get_live_video_id(live_channel_url)

                if live_video_id:
                    video_id_url = f"https://www.youtube.com/watch?v={live_video_id}\n"
                    updated_lines.append(f"{search_term}, {group}, {live_channel_url}, {video_id_url}")
                    print(f"Found live video ID for '{search_term}': {video_id_url}")
                else:
                    print(f"Could not find a live video ID for '{search_term}'. Skipping.")

            else:
                print(f"Could not find a channel URL for '{search_term}'. Skipping.")

        else:
            updated_lines.append(line)

    with open(output_filename, 'w') as file:  # Change to 'w' for write mode
        file.writelines(updated_lines)

    print(f"Updated information written to {output_filename}")

if __name__ == "__main__":
    # Specify the path for the input file
    input_file_path = "current_channels.txt"  # Change to the actual path

    # Process the specified input file
    print(f"Processing input file: {input_file_path}")
    process_input_file(input_file_path)
