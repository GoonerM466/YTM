import re
from datetime import datetime, timedelta

def parse_live_status(line):
    # Parse the information from the live_status.txt line
    match = re.match(r'^([\w_]+) - (Live|Not Live) - (.+ UTC \d{4})$', line)
    if match:
        channel_name, live_status, time_str = match.groups()
        return channel_name, live_status, time_str
    return None

def convert_to_xmltv_time(time_str):
    # Convert the time string to XMLTV format
    dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Z %Y')
    return dt.strftime('%Y%m%d%H%M%S +0000')

def round_up_to_hour(dt):
    # Round up the given datetime object to the nearest hour
    return (dt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def generate_channel_info(channel_name, existing_channels):
    # Extract the first part of the channel name before the first space
    channel_name_first_part = channel_name.split()[0]

    # Check for duplicate channels based on the first part of the channel name
    for existing_channel in existing_channels:
        existing_channel_first_part = existing_channel['name'].split()[0]
        if existing_channel_first_part == channel_name_first_part:
            return None

    # No matching channel found, add the new channel
    return f'''  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>
'''

def generate_program_info(channel_name, live_status, time_str, existing_programs):
    # Convert time_str to XMLTV format
    new_program_start = datetime.strptime(convert_to_xmltv_time(time_str), '%Y%m%d%H%M%S +0000')

    # Round up the start time to the nearest hour
    new_program_start_rounded = round_up_to_hour(new_program_start)
    new_program_stop_rounded = (new_program_start_rounded + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')

    # Check for existing programs with the same details
    for existing_program in existing_programs:
        if existing_program['channel'] == channel_name and existing_program['start'] == new_program_start_rounded.strftime('%Y%m%d%H%M%S +0000') and existing_program['stop'] == new_program_stop_rounded:
            # Program with the same details already exists, skip adding it
            return ""

    # Create the new program
    new_program_stop = (new_program_start + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    new_program_info = f'''  <programme start="{new_program_start_rounded.strftime('%Y%m%d%H%M%S +0000')}" stop="{new_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    # Create the following program with the same details
    following_program_start = new_program_start_rounded
    following_program_stop = (following_program_start + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    following_program_info = f'''  <programme start="{following_program_start.strftime('%Y%m%d%H%M%S +0000')}" stop="{following_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    return new_program_info + following_program_info

def generate_placeholder_programs(channel_name, current_time_rounded):
    # Generate 24 hours worth of "To be Announced" programs for the given channel
    programs = ""
    for _ in range(24):
        program_start = current_time_rounded.strftime('%Y%m%d%H%M%S +0000')
        program_stop = (current_time_rounded + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
        program_info = f'''  <programme start="{program_start}" stop="{program_stop}" channel="{channel_name}">
    <title lang="en">To be Announced</title>
    <desc lang="en">The status of this channel for this time slot is unknown. Please check back later or check online for more information.</desc>
  </programme>
'''
        programs += program_info
        current_time_rounded += timedelta(hours=1)

    return programs

def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    channel_info = ""
    program_info = ""

    existing_channels = []  # Remove old EPG channel extraction
    existing_programs = []  # Remove old EPG program extraction

    # Get the current time rounded up to the next hour
    current_time = datetime.now()
    current_time_rounded = round_up_to_hour(current_time)

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            channel_info_entry = generate_channel_info(channel_name, existing_channels)
            if channel_info_entry:
                channel_info += channel_info_entry

            # Add 24 hours worth of "To be Announced" programs for the channel
            program_info += generate_placeholder_programs(channel_name, current_time_rounded)

            program_info += generate_program_info(channel_name, live_status, time_str, existing_programs)

    # Combine all information into the final XMLTV content
    xmltv_content = f"{header}{channel_info}{program_info}</tv>"

    # Sort the programs by channel name and then in chronological order
    sorted_xmltv_content = sort_xmltv_content(xmltv_content)

    # Write the combined and sorted content to combined_epg.xml
    with open('combined_epg.xml', 'w') as combined_epg_file:
        combined_epg_file.write(sorted_xmltv_content)

    # Clear the content of epg_old.xml
    with open('epg_old.xml', 'w'):
        pass

def sort_xmltv_content(xmltv_content):
    # Helper function to sort XMLTV content by channel name and then in chronological order
    lines = xmltv_content.splitlines()
    
    # Find the last instance of "</channel>"
    last_channel_index = max(loc for loc, line in enumerate(lines) if "</channel>" in line)
    
    # Find the start and end indexes for program entries
    start_index = last_channel_index
    end_index = lines.index('</tv>')

    # Extract program entries for sorting
    programs = lines[start_index:end_index]

    # Identify and sort each program entry individually
    sorted_programs = sorted(programs, key=lambda x: (extract_channel_name(x), extract_start_time(x)))

    # Replace the original program entries with the sorted ones
    lines[start_index:end_index] = sorted_programs

    return '\n'.join(lines)


def extract_channel_name(program_line):
    match = re.search(r'channel="(.+)"', program_line)
    return match.group(1) if match else ""

def extract_start_time(program_line):
    match = re.search(r'start="(.+)"', program_line)
    return match.group(1) if match else ""

if __name__ == '__main__':
    main()
