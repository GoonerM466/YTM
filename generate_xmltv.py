import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

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
    # Read the existing XMLTV file
    try:
        tree = ET.parse('combined_epg.xml')
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        # If the file doesn't exist or is not valid XML, create a new root
        root = ET.Element('tv')
        tree = ET.ElementTree(root)

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    channel_info = ""
    program_info = ""

    # Keep track of existing channels
    existing_channels = set(channel.attrib['id'] for channel in root.findall('.//channel'))

    for line in open('live_status.txt', 'r').readlines():
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Insert channel info only if the channel doesn't already exist
            if channel_name not in existing_channels:
                channel_info += generate_channel_info(channel_name)
                existing_channels.add(channel_name)

            program_info += generate_program_info(channel_name, live_status, time_str)

    # Delete unnecessary channels
    for channel in root.findall('.//channel'):
        if channel.attrib['id'] not in existing_channels:
            root.remove(channel)

    # Remove old program entries
    current_time = datetime.utcnow()
    for program in root.findall('.//programme'):
        stop_time_str = program.attrib['stop']
        stop_time = datetime.strptime(stop_time_str, '%Y%m%d%H%M%S +0000')
        if (current_time - stop_time).total_seconds() > 36 * 3600:
            root.remove(program)

    # Append new program entries
    new_programs = ET.fromstring(program_info)
    for program in new_programs:
        root.append(program)

    # Combine all information into the final XMLTV content
    xmltv_content = f"{header}{ET.tostring(root).decode('utf-8')}</tv>"

    # Write the updated XMLTV content to the file
    with open('combined_epg.xml', 'w') as file:
        file.write(xmltv_content)

if __name__ == '__main__':
    main()
