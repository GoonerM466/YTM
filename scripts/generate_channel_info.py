import re
from datetime import datetime, timedelta

# ... (rest of the script remains unchanged)

def main():
    try:
        with open('live_status.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: File 'live_status.txt' not found.")
        return

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    xmltv_content = header
    existing_channels = []  # Keep track of existing channels
    existing_programs = []  # Keep track of existing programs

    # Get the current time rounded up to the next hour
    current_time = datetime.now()
    current_time_rounded = round_up_to_hour(current_time)

    # Accumulate channel information
    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Add channel information
            channel_info_entry = generate_channel_info(channel_name, existing_channels)
            if channel_info_entry:
                xmltv_content += channel_info_entry

    # Accumulate program information
    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Clear existing program information for the current channel
            existing_programs = []  # Reset the list for each channel

            # Add current program information
            xmltv_content += generate_program_info(channel_name, live_status, time_str, existing_programs)

            # Calculate the end time of the last live program
            last_program_end = current_time_rounded + timedelta(hours=2)

            # Add 12 hours of placeholder programs
            xmltv_content += generate_placeholder_programs(channel_name, last_program_end)

    xmltv_content += '</tv>'

    try:
        # Write the combined content to combined_epg.xml
        with open('combined_epg.xml', 'r') as existing_file:
            existing_content = existing_file.read()

        if existing_content != xmltv_content:
            with open('combined_epg.xml', 'w') as combined_epg_file:
                combined_epg_file.write(xmltv_content)
            print("Combined EPG has been updated.")
        else:
            print("Everything is up to date.")

    except Exception as e:
        print("Error:", str(e))
        print("Everything is up to date.")

if __name__ == '__main__':
    main()
