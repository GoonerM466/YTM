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

def generate_channel_info(channel_name, existing_channels):
    # Check for duplicate channels and do not add if already exists
    for existing_channel in existing_channels:
        if existing_channel['name'] == channel_name:
            return None
    
    # No matching channel found, add the new channel
    return f'''  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>
'''

def adjust_program_times(existing_program, new_program_start):
    # If existing program started less than 5 minutes ago, adjust its start time backward by 25 minutes
    start_time = datetime.strptime(existing_program['start'], '%Y%m%d%H%M%S +0000')
    if start_time > new_program_start - timedelta(minutes=5):
        existing_program['start'] = (new_program_start - timedelta(minutes=25)).strftime('%Y%m%d%H%M%S +0000')

def generate_program_info(channel_name, live_status, time_str, existing_programs):
    # Convert time_str to XMLTV format
    new_program_start = datetime.strptime(convert_to_xmltv_time(time_str), '%Y%m%d%H%M%S +0000')
    new_program_stop = (new_program_start + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

    # Check for existing programs with the same details
    for existing_program in existing_programs:
        if existing_program['channel'] == channel_name and existing_program['start'] < new_program_stop and existing_program['stop'] > new_program_start:
            # Adjust times to avoid overlap
            adjust_program_times(existing_program, new_program_start)
            return ""  # Do not add the new program as it already exists
    else:
        # No matching program found, add the new program
        return f'''  <programme start="{new_program_start.strftime('%Y%m%d%H%M%S +0000')}" stop="{new_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    channel_info = ""
    program_info = ""

    # Read program information from old_epg.xml and parse it
    with open('old_epg.xml', 'r') as old_epg_file:
        old_epg_content = old_epg_file.read()

    # Extract existing channel and program details from old_epg_content
    existing_channels = []
    existing_programs = []
    channel_match = re.finditer(r'<channel id="(.+)">\s*<display-name lang="en">(.+)</display-name>\s*</channel>', old_epg_content)
    for match in channel_match:
        existing_channels.append({'name': match.group(2)})
    program_match = re.finditer(r'<programme start="(.+)" stop="(.+)" channel="(.+)">', old_epg_content)
    for match in program_match:
        existing_programs.append({'channel': match.group(3), 'start': match.group(1), 'stop': match.group(2)})

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            channel_info_entry = generate_channel_info(channel_name, existing_channels)
            if channel_info_entry:
                channel_info += channel_info_entry
            program_info += generate_program_info(channel_name, live_status, time_str, existing_programs)

    # Combine all information into the final XMLTV content
    xmltv_content = f"{header}{channel_info}{old_epg_content}{program_info}</tv>"

    # Write the combined content to combined_epg.xml
    with open('combined_epg.xml', 'w') as combined_epg_file:
        combined_epg_file.write(xmltv_content)

    # Clear the content of epg_old.xml
    with open('epg_old.xml', 'w'):
        pass

if __name__ == '__main__':
    main()
