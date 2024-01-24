import yt_dlp

def search_youtube_and_get_channel_url(search_phrase, max_results=1):
    ydl = yt_dlp.YoutubeDL()
    search_results = ydl.extract_info(f"ytsearch{max_results}:{search_phrase}", download=False)
    channel_url = search_results.get('entries', [{}])[0].get('channel_url', None)
    return channel_url

def process_input_file(input_filename):
    output_filename = input_filename

    with open(input_filename, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        if line.startswith("Channel Name:"):
            channel_name = line.replace("Channel Name:", "").strip()
            search_term = channel_name.lower()  # using the channel name as the search term
            channel_url = search_youtube_and_get_channel_url(search_term)

            if channel_url:
                live_channel_url = f"{channel_url.rstrip('/')}/live"
                updated_lines.append(f"Channel Name: {channel_name}\n")
                updated_lines.append(f"Channel URL: {live_channel_url}\n")
            else:
                print(f"Could not find a channel URL for '{channel_name}'. Skipping.")
        elif line.startswith(("Title:", "Description:", "Logo URL:")):
            # Preserve lines starting with "Title:", "Description:", and "Logo URL:"
            updated_lines.append(line)
        elif line.startswith("Add this link to the update file:"):
            # Preserve the original "Add this link to the update file:" line
            updated_lines.append(line)

    with open(output_filename, 'w') as file:
        file.writelines(updated_lines)

    print(f"Updated information written to {output_filename}")

if __name__ == "__main__":
    input_file = "music_live_channels.txt"
    process_input_file(input_file)
