import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import os

def clean_old_epg(input_file, max_age_hours=36):
    # Parse the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()
    # Get the current time in UTC
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Filter out and remove programs older than max_age_hours
    for program in root.findall('.//programme'):
        start_time_str = program.get('start')
        start_time = datetime.strptime(start_time_str, '%Y%m%d%H%M%S %z')
        # Calculate the age of the program in hours
        age_hours = (current_time - start_time).total_seconds() / 3600
        if age_hours > max_age_hours:
            root.remove(program)

    # Write the remaining programs back to the input file
    tree.write(input_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    input_file = 'combined_epg.xml'
    max_age_hours = 36  # Define max_age_hours here
    clean_old_epg(input_file, max_age_hours)
