
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def clean_old_epg(input_file, output_file, max_age_hours=36):
    # Parse the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Get the current time
    current_time = datetime.utcnow()

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
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    # Check if the combined_epg.xml file is empty
    if len(root.findall('.//programme')) == 0:
        # If there are no remaining programs, create an empty combined_epg.xml file
        with open(input_file, 'w'):
            pass

if __name__ == "__main__":
    input_file = 'combined_epg.xml'
    output_file = 'epg_old.xml'
    clean_old_epg(input_file, output_file)

    # Create old_epg.xml even if there are no remaining programs
    with open('old_epg.xml', 'w'):
        pass
