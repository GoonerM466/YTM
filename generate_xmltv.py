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

def generate_xmltv(channel_name, live_status, time_str):
    # Generate the XMLTV content based on the provided information
    start_time = convert_to_xmltv_time(time_str)
    stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

    xmltv_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>

  <programme start="{start_time}" stop="{stop_time}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in & enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>

</tv>
'''
    return xmltv_content

def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            xmltv_content = generate_xmltv(channel_name, live_status, time_str)
            print(xmltv_content)

if __name__ == '__main__':
    main()
