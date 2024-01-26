import os
import yt_dlp
import time
import sys

def search_youtube_and_get_channel_info(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    try:
        search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
        entry = search_results.get('entries', [{}])[0]
        
        # Check if the video requires membership
        if entry.get('requires_membership'):
            result = f"Video requires membership. Skipping '{search_phrase}'."
            print(result)
            return None, None, result
        
        channel_url = entry.get('channel_url', None)
        video_id = entry.get('id', None)

        result = f"Found channel URL: {channel_url}\nFound video ID: {video_id}"
        print(result)

        return channel_url, video_id, result
    except yt_dlp.utils.ExtractorError as e:
        result = f"Error extracting information from YouTube: {str(e)}"
        print(result)
        return None, None, result
    except yt_dlp.utils.DownloadError as e:
        result = f"Error downloading information from YouTube: {str(e)}"
        print(result)
        return None, None, result
    except Exception as e:
        result = f"An unexpected error occurred: {str(e)}"
        print(result)
        return None, None, result

def process_input_file(input_filename):
    output_filename = "./program/alt_urls.txt"  # Change the output file path
    log_filename = "./program/workflow_log.txt"  # New log file path

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    workflow_log = []

    for line in lines:
        if line.startswith("$search_term"):
            # Assuming the input file has the format $search_term, $group, $channel_url
            search_term, group, channel_url = line.strip().split(', ')
            search_term_lower = search_term.lower()

            new_channel_url, video_id, result = search_youtube_and_get_channel_info(search_term_lower)

            workflow_log.append(result)

            if new_channel_url:
                live_channel_url = f"{new_channel_url.rstrip('/')}/live"
                if video_id:
                    video_id_url = f"https://www.youtube.com/watch?v={video_id}\n"
                    updated_lines.append(f"{search_term}, {group}, {live_channel_url}, {video_id_url}")
                    workflow_log.append(f"Updated information for '{search_term}' written to output.")
                else:
                    workflow_log.append(f"Could not find a video ID for '{search_term}'. Skipping.")

            else:
                workflow_log.append(f"Could not find a channel URL for '{search_term}'. Skipping.")

        else:
            updated_lines.append(line)

    with open(output_filename, 'w') as file:  # Change to 'w' for write mode
        file.writelines(updated_lines)

    with open(log_filename, 'w') as log_file:  # New log file
        log_file.writelines("\n".join(workflow_log))

    print(f"Updated information written to {output_filename}")
    print(f"Workflow log written to {log_filename}")

if __name__ == "__main__":
    # Specify the path for the input file
    input_file_path = "current_channels.txt"  # Change to the actual path

    # Redirect stdout to a file
    sys.stdout = open("workflow_report.txt", "w")

    # Process the specified input file
    process_input_file(input_file_path)

    # Close the file to ensure all data is written
    sys.stdout.close()
