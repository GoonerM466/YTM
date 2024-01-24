def main():
    with open('live_status.txt', 'r') as file:
        lines = file.readlines()

    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="none" generator-info-url="none">
'''

    xmltv_content = header

    # Get the current time rounded up to the next hour
    current_time = datetime.now()
    current_time_rounded = round_up_to_hour(current_time)

    for line in lines:
        parsed_info = parse_live_status(line)
        if parsed_info:
            channel_name, live_status, time_str = parsed_info

            # Add channel information
            channel_info_entry = generate_channel_info(channel_name)
            if channel_info_entry:
                xmltv_content += channel_info_entry

            # Clear existing program information for the current channel
            existing_programs = []  # Reset the list for each channel

            # Add current program information
            xmltv_content += generate_program_info(channel_name, live_status, time_str, existing_programs)

            # Calculate the end time of the last live program
            last_program_end = current_time_rounded + timedelta(hours=2)

            # Add 12 hours of placeholder programs
            xmltv_content += generate_placeholder_programs(channel_name, last_program_end)

    xmltv_content += '</tv>'

    # Write the combined content to combined_epg.xml
    with open('combined_epg.xml', 'w') as combined_epg_file:
        combined_epg_file.write(xmltv_content)

if __name__ == '__main__':
    main()
