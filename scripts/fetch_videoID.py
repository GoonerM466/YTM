import os
import yt_dlp
import time

def search_youtube_and_get_video_url(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    try:
        search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
        entry = search_results.get('entries', [{}])[0]

        # Check if the video requires membership
        if entry.get('requires_membership'):
            print(f"Video requires membership. Skipping '{search_phrase}'.")
            return None

        video_id = entry.get('id', None)
        return f"https://www.youtube.com/watch?v={video_id}"
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading information from YouTube: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
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
            new_video_url = search_youtube_and_get_video_url(search_term_lower)

            if new_video_url:
                updated_lines.append(f"{search_term}, {group}, {channel_url}, {new_video_url}\n")
                # Add a 2-second delay between each search
                time.sleep(2)
            else:
                print(f"Could not find a video URL for '{search_term}'. Skipping.")
        else:
            updated_lines.append(line)

    with open(output_filename, 'w') as file:  # Change to 'w' for write mode
        file.writelines(updated_lines)

    print(f"Updated information written to {output_filename}")

if __name__ == "__main__":
    # Specify the path for the input file
    input_file_path = "./program/alt_urls.txt"  # Change to the actual path

    # Process the specified input file
    process_input_file(input_file_path)
