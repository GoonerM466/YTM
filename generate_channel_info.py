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

def generate_program_info(channel_name, live_status, time_str, existing_programs):
    # Convert time_str to XMLTV format
    start_time = convert_to_xmltv_time(time_str)
    stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

    # Search for existing program with the same channel name
    existing_program = next((program for program in existing_programs if program['channel'] == channel_name), None)

    if existing_program:
        # If titles match, extend end time by 2 hours
        if existing_program['title'] == live_status:
            existing_program['stop'] = (datetime.strptime(existing_program['stop'], '%Y%m%d%H%M%S +0000') + timedelta(hours=2)).strftime('%Y%m%d%H%M%S +0000')
        else:
            # If titles don't match, delete existing program and add the new one
            existing_programs.remove(existing_program)
            existing_programs.append({'channel': channel_name, 'title': live_status, 'start': start_time, 'stop': stop_time})
    else:
        # Add the new program
        existing_programs.append({'channel': channel_name, 'title': live_status, 'start': start_time, 'stop': stop_time})

    return f'''  <programme start="{start_time}" stop="{stop_time}" channel="{channel_name}">
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
    existing_channels = []
    existing_programs = []

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            channel_info_entry = generate_channel_info(channel_name, existing_channels)
            if channel_info_entry:
                channel_info += channel_info_entry
            program_info += generate_program_info(channel_name, live_status, time_str, existing_programs)

    # Combine all information into the final XMLTV content
    xmltv_content = f"{header}{channel_info}{program_info}</tv>"
    # Write the combined content to combined_epg.xml
    with open('combined_epg.xml', 'w') as combined_epg_file:
        combined_epg_file.write(xmltv_content)
    # Clear the content of epg_old.xml
    with open('epg_old.xml', 'w'):
        pass

if __name__ == '__main__':
    main()
