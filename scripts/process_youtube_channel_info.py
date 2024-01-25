import re

def channel_exists(channel_name, current_channels_content):
    pattern = fr'New: {re.escape(channel_name)},'
    match = re.search(pattern, current_channels_content)
    
    if match:
        print(f"Match found for '{channel_name}': {match.group()}")
    else:
        print(f"No match found for '{channel_name}', pattern: '{pattern}'")

    return match is not None

# Read current_channels.txt content
with open('current_channels.txt', 'r') as current_channels_file:
    current_channels_content = current_channels_file.read()

# Read youtube_channel_info.txt and process each line
with open('youtube_channel_info.txt', 'r') as info_file:
    lines = info_file.readlines()

# Open current_channels.txt in append mode
with open('current_channels.txt', 'a') as current_channels_file_append:
    # Process each line in youtube_channel_info.txt
    for line in lines:
        # Extract information from the line
        parts = line.strip().split('New: ')
        if len(parts) == 2:
            _, channel_info = parts
            channel_name, channel_group, channel_url = channel_info.split(', ', 2)

            # Check if the channel exists in current_channels.txt
            if channel_exists(channel_name, current_channels_content):
                print(f"Channel '{channel_name}' already exists in current_channels.txt. Skipping...")
                continue

            # Process the channel information and add entry to current_channels.txt
            print(f"Processing new channel: {channel_name}, {channel_group}, {channel_url}")

            # Ensure that the original channel_name is used when adding the new entry
            original_channel_name_entry = f"{channel_name}, {channel_group}, {channel_url}"

            # Append the new entry to the file
            current_channels_file_append.write(original_channel_name_entry + "\n")

# Print a message indicating the script has finished
print("Script completed.")
