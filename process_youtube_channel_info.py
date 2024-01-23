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

            # Find the first empty line in 'current_channels.txt'
            empty_line_position = current_channels_content.find('\n\n')

            # If an empty line is found, insert the new entry after the empty line
            if empty_line_position != -1:
                with open('current_channels.txt', 'w') as current_channels_file_write:
                    current_channels_file_write.write(current_channels_content[:empty_line_position + 1] + f"{channel_name}, {channel_group}, {channel_url}\n" + current_channels_content[empty_line_position + 1:])
            else:
                # If no empty line is found, simply append the new entry
                with open('current_channels.txt', 'a') as current_channels_file_append:
                    current_channels_file_append.write(f"{channel_name}, {channel_group}, {channel_url}\n")

            new_entries_added = True  # Set the flag to true

# Print a message indicating the script has finished
print("Script completed.")
