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

def round_down_to_hour(dt):
    # Round down the given datetime object to the nearest hour
    return dt.replace(minute=0, second=0, microsecond=0)

def generate_program_info(channel_name, live_status, time_str, existing_programs):
    # Convert time_str to XMLTV format
    program_start = datetime.strptime(convert_to_xmltv_time(time_str), '%Y%m%d%H%M%S +0000')

    # Round down the start time to the nearest hour
    program_start_rounded = round_down_to_hour(program_start)

    # Check for existing programs with the same details
    for existing_program in existing_programs:
        if existing_program['channel'] == channel_name and existing_program['start'] == program_start_rounded.strftime('%Y%m%d%H%M%S +0000') and existing_program['stop'] == (program_start_rounded + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000'):
            # Program with the same details already exists, skip adding it
            return ""

    # Create the new program
    program_stop = (program_start_rounded + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    new_program_info = f'''  <programme start="{program_start_rounded.strftime('%Y%m%d%H%M%S +0000')}" stop="{program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    # Create the following program with the same details
    following_program_start = program_start_rounded + timedelta(hours=1)
    following_program_stop = (following_program_start + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    following_program_info = f'''  <programme start="{following_program_start.strftime('%Y%m%d%H%M%S +0000')}" stop="{following_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    return new_program_info + following_program_info

def generate_placeholder_programs(channel_name, current_time_rounded):
    # Generate 12 hours worth of "To be Announced" programs for the given channel
    programs = ""
    for _ in range(12):
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

    xmltv_content = header
    existing_channels = []  # Keep track of existing channels
    existing_programs = []  # Keep track of existing programs

    # Get the current time rounded up to the next hour
    current_time = datetime.now()
    current_time_rounded = round_up_to_hour(current_time)

    # Accumulate channel information
    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Add channel information
            channel_info_entry = generate_channel_info(channel_name, existing_channels)
            if channel_info_entry:
                xmltv_content += channel_info_entry

    # Accumulate program information
    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Clear existing program information for the current channel
            existing_programs = []  # Reset the list for each channel

            # Add current program information
            xmltv_content += generate_program_info(channel_name, live_status, time_str, existing_programs)

            # Calculate the end time of the last live program
            last_program_end = current_time_rounded + timedelta(hours=2)

            # Add 12 hours of placeholder programs
            xmltv_content += generate_placeholder_programs(channel_name, last_program_end)

    xmltv_content += '</tv>'

    # Write the combined content to combined_epg.xml
    with open('combined_epg.xml', 'w') as combined_epg_file:
        combined_epg_file.write(xmltv_content)

if __name__ == '__main__':
    main()
