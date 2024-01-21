import re
import fileinput

# Function to check if $channel_name exists in ytm.yml
def channel_exists(channel_name, ytm_content):
    return re.search(fr'\s*channel_name:\s*{channel_name}\b', ytm_content) is not None

# Read ytm.yml content
with open('.github/workflows/ytm.yml', 'r') as ytm_file:
    ytm_content = ytm_file.read()

# Search for and remove the "git add," "commit & push" steps
git_steps_pattern = re.compile(r'\s*- name: git add.*?git push', re.DOTALL)
ytm_content = git_steps_pattern.sub('', ytm_content)

# Write the modified ytm.yml content back to the file
with open('.github/workflows/ytm.yml', 'w') as ytm_file:
    ytm_file.write(ytm_content)

# Read youtube_channel_info.txt and process each line
with open('youtube_channel_info.txt', 'r') as info_file:
    new_entries_added = False  # Flag to track if new entries are added
    for line in info_file:
        # Extract information from the line
        parts = line.strip().split('New: ')
        if len(parts) == 2:
            _, channel_info = parts
            channel_name, channel_group, channel_url = channel_info.split(', ', 2)

            # Check if the channel exists in ytm.yml
            if channel_exists(channel_name, ytm_content):
                print(f"Channel '{channel_name}' already exists in ytm.yml. Skipping...")
                continue

            # Process the channel information and add entry to ytm.yml
            print(f"Processing new channel: {channel_name}, {channel_group}, {channel_url}")

            # Add entry to ytm.yml
            new_entry = f"""
 
