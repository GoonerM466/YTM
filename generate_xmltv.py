import re
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

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
    try:
        # Attempt to parse the existing XMLTV file
        tree = ET.parse('combined_epg.xml')
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError):
        # Handle the case where the file is not found or cannot be parsed
        root = ET.Element('tv', attrib={'generator-info-name': 'none', 'generator-info-url': 'none'})

    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    channel_info = ""
    program_info = ""

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            channel_info += generate_channel_info(channel_name)
            program_info += generate_program_info(channel_name, live_status, time_str)

    # Create a new root element and add the channel and program information
    new_root = ET.Element('tv', attrib={'generator-info-name': 'none', 'generator-info-url': 'none'})
    new_root.extend(ET.fromstring(channel_info + program_info))

    # Write the updated information to combined_epg.xml
    tree = ET.ElementTree(new_root)
    tree.write('combined_epg.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    main()
