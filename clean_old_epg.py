import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

def clean_old_epg(input_file, output_file, max_age_hours):
    # Parse input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Get current time with timezone information
    current_time = datetime.now(timezone.utc)

    # Remove header and all channels
    for element in root.findall('.//channel') + root.findall('.//programme'):
        root.remove(element)

    # Filter out and remove programs older than max_age_hours
    for program in root.findall('.//programme'):
        start_time_str = program.get('start')
        start_time = datetime.strptime(start_time_str, "%Y%m%d%H%M%S %z")

        end_time_str = program.get('stop')
        end_time = datetime.strptime(end_time_str, "%Y%m%d%H%M%S %z")

        age = current_time - end_time
        if age.total_seconds() > max_age_hours * 3600:
            root.remove(program)

    # Write the remaining programs to the output file
    with open("old_" + output_file, 'wb') as output:
        tree.write(output)

    # Check if the input file is empty after removing programs
    if root.findall('.//programme'):
        # Input file is not empty, clear its contents
        for element in root.findall('.//programme'):
            root.remove(element)
        with open(input_file, 'wb') as input:
            tree.write(input)

if __name__ == "__main__":
    # Set your parameters
    input_file = "combined_epg.xml"
    output_file = "epg_old.xml"  # Corrected output file name
    max_age_hours = 36

    # Execute the script
    clean_old_epg(input_file, output_file, max_age_hours)
