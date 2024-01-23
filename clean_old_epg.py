import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import os

def clean_old_epg(input_file, output_file, max_age_hours=36):
    # Check if the input XML file exists
    if not os.path.exists(input_file):
        # If the file doesn't exist, create an empty combined_epg.xml file
        with open(input_file, 'w'):
            pass
        # Also create old_epg.xml regardless of remaining programs
        os.system('touch old_epg.xml')
        return

    # Read the content of the input XML file
    with open(input_file, 'r') as input_file_handle:
        content = input_file_handle.read()

    # Check if the content is empty or only contains whitespace
    if not content.strip():
        # If the content is empty, finish without further processing
        # Also create old_epg.xml regardless of remaining programs
        os.system('touch old_epg.xml')
        return

    # Parse the input XML file
    tree = ET.fromstring(content)
    root = ET.ElementTree(tree).getroot()

    # Get the current time with timezone information
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Remove header and all channels
    for channel in root.findall('.//channel'):
        root.remove(channel)

    # Filter out and remove programs older than max_age_hours
    for program in root.findall('.//programme'):
        start_time_str = program.get('start')
        start_time = datetime.strptime(start_time_str, '%Y%m%d%H%M%S %z')

        # Calculate the age of the program in hours
        age_hours = (current_time - start_time).total_seconds() / 3600

        if age_hours > max_age_hours:
            root.remove(program)

    # Write the remaining programs to the output file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    # Check if the combined_epg.xml file is empty after removing programs
    if len(root.findall('.//programme')) == 0:
        # If there are no remaining programs, create an empty combined_epg.xml file
        with open(input_file, 'w'):
            pass

    # Always create old_epg.xml regardless of remaining programs
    os.system('touch old_epg.xml')

if __name__ == "__main__":
    input_file = 'combined_epg.xml'
    output_file = 'epg_old.xml'
    clean_old_epg(input_file, output_file)
