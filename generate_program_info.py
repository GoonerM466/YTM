import re
import xml.etree.ElementTree as ET

def parse_live_status(line):
    # Parse the information from the live_status.txt line
    match = re.match(r'^([\w_]+) - (Live|Not Live) - (.+ UTC \d{4})$', line)
    if match:
        channel_name, live_status, time_str = match.groups()
        return channel_name, live_status, time_str
    return None

def generate_program_info(channel_name, live_status, time_str):
    # Generate the XMLTV content for program information
    start_time = convert_to_xmltv_time(time_str)
    stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

    return f'''  <programme start="{start_time}" stop="{stop_time}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

def convert_to_xmltv_time(time_str):
    # Convert the time string to XMLTV format
    dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Z %Y')
    return dt.strftime('%Y%m%d%H%M%S +0000')

def add_programs_to_combined_epg(programs):
    # Parse the existing combined_epg.xml file
    combined_epg_tree = ET.parse('combined_epg.xml')
    combined_epg_root = combined_epg_tree.getroot()

    # Find the last entry in the existing file
    last_entry = combined_epg_root[-1] if len(combined_epg_root) > 0 else None

    # Add the new programs after the last entry
    for program in programs:
        if last_entry is not None:
            last_entry.addnext(program)
        else:
            combined_epg_root.append(program)

    # Write the combined information back to the combined_epg.xml file
    combined_epg_tree.write('combined_epg.xml', encoding='utf-8', xml_declaration=True)

def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    programs = []

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info
            program_info = generate_program_info(channel_name, live_status, time_str)
            programs.append(ET.fromstring(program_info))  # Convert to ElementTree Element

    add_programs_to_combined_epg(programs)

if __name__ == '__main__':
    main()
