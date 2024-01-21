import re
import fileinput

# Function to check if $channel_name exists in ytm.yml
def channel_exists(channel_name, ytm_content):
    return re.search(fr'\s*channel_name:\s*{channel_name}\b', ytm_content) is not None

# Read ytm.yml content
with open('.github/workflows/ytm.yml', 'r') as ytm_file:
    ytm_lines = ytm_file.readlines()

# Remove the "git add," "commit & push" steps
remove_git_steps = False
filtered_ytm_lines = []

for line in ytm_lines:
    if "git add -A" in line:
        remove_git_steps = True
    elif "git commit -m \"links are updated\"" in line:
        remove_git_steps = False
    elif remove_git_steps:
        continue
    else:
        filtered_ytm_lines.append(line)

# Write the modified ytm.yml content back to the file
with open('.github/workflows/ytm.yml', 'w') as ytm_file:
    ytm_file.writelines(filtered_ytm_lines)

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
    - name: Get {channel_name}
      run: |
        touch ./{channel_group}/{channel_name}.m3u8
        sudo cat >./{channel_group}/{channel_name}.m3u8 <<EOL
        #EXTM3U
        #EXT-X-VERSION:3
        #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000
        $$(yt-dlp --print urls {channel_url})
        EOL
"""
            # Append new entry to ytm.yml
            with open('.github/workflows/ytm.yml', 'a') as ytm_file_append:
                ytm_file_append.write(new_entry)

            new_entries_added = True  # Set the flag to true

# Add git add, commit, and push steps regardless of new entries
git_steps = """
    - name: git add
      run: |
        git add -A
        ls -la
    - name: commit & push
      run: |
        git commit -m "links are updated"
        git push
"""

# Append git steps to ytm.yml
with open('.github/workflows/ytm.yml', 'a') as ytm_file_append:
    ytm_file_append.write(git_steps)

# Print a message indicating the script has finished
print("Script completed.")
