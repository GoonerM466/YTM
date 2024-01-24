import os
import yt_dlp
import time

def search_youtube_and_get_channel_url(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    try:
        search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
        channel_url = search_results.get('entries', [{}])[0].get('channel_url', None)
        return channel_url
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None

def process_input_file(input_filename):
    output_filename = input_filename

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        if line.startswith("Channel Name:"):
            channel_name = line.replace("Channel Name:", "").strip()
            search_term = channel_name.lower()
            channel_url = search_youtube_and_get_channel_url(search_term)

            if channel_url:
                live_channel_url = f"{channel_url.rstrip('/')}/live"
                updated_lines.append(f"Channel Name: {channel_name}\n")
                updated_lines.append(f"Channel URL: {live_channel_url}\n")
            else:
                print(f"Could not find a channel URL for '{channel_name}'. Skipping.")

            # Add a 2-second delay between each search
            time.sleep(2)
        elif line.startswith(("Title:", "Description:", "Logo URL:")):
            updated_lines.append(line)
        elif line.startswith("Add this link to the update file:"):
            # Replace the existing "Add this link to the update file" line
            channel_url_line = f"Add this link to the update file: New: {channel_name}, INSERT YOUR PREFERRED GROUP, {live_channel_url}\n"
            updated_lines.append(channel_url_line)

    with open(output_filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated information written to {output_filename}")

def process_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_live_channels.txt"):
            input_file_path = os.path.join(directory, filename)
            process_input_file(input_file_path)

if __name__ == "__main__":
    # Directory where the files are located
    directory = "found_channels"
    
    # Process all files in the directory
    process_all_files_in_directory(directory)
