import re

def parse_live_status(line):
    # Parse the information from the live_status.txt line
    match = re.match(r'^([\w_]+) - (Live|Not Live) - (.+ UTC \d{4})$', line)
    if match:
        channel_name, live_status, time_str = match.groups()
        return channel_name, live_status, time_str
    return None

def generate_channel_info(channel_name):
    # Generate the XMLTV content for channel information
    return f'''  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>
'''

def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    channel_info = ""

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, _, _ = parsed_info
            channel_info += generate_channel_info(channel_name)

    # Combine all information into the final XMLTV content
    xmltv_content = f"{header}{channel_info}"
    
    # Use the xmltv_content variable as needed (e.g., save to a file, send in an API request, etc.)
    # Example: 
    # with open('output.xml', 'w') as output_file:
    #     output_file.write(xmltv_content)

if __name__ == '__main__':
    main()
