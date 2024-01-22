import re

# Function to check if $channel_name exists in current_channels.txt
def channel_exists(channel_name, current_channels_content):
    return re.search(fr'\s*{channel_name},', current_channels_content) is not None

# Read current_channels.txt content
with open('current_channels.txt', 'r') as current_channels_file:
    current_channels_content = current_channels_file.read()

# Read youtube_channel_info.txt and process each line
with open('youtube_channel_info.txt', 'r') as info_file:
    new_entries_added = False  # Flag to track if new entries are added

    for line in info_file:
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

            # Add entry to current_channels.txt
            new_entry = f"{channel_name}, {channel_group}, {channel_url}\n"
            with open('current_channels.txt', 'a') as current_channels_file_append:
                current_channels_file_append.write(new_entry)

            new_entries_added = True  # Set the flag to true

# Print a message indicating the script has finished
print("Script completed.")
