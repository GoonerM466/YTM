import re
from datetime import datetime, timedelta
import os

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

def generate_channel_info(channel_name):
    # Generate the XMLTV content for channel information
    return f'''  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>
'''

def generate_program_info(channel_name, live_status, time_str):
    # Generate the XMLTV content for program information
    start_time = convert_to_xmltv_time(time_str)
    stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

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

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            channel_info += generate_channel_info(channel_name)
            program_info += generate_program_info(channel_name, live_status, time_str)

    # Read program information from old_epg.xml and insert it at the top
    with open('old_epg.xml', 'r') as old_epg_file:
        old_epg_content = old_epg_file.read()

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
