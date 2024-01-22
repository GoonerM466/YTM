import os

def main():
    # Check if old_epg.xml exists, if not, create it
    if not os.path.exists('old_epg.xml'):
        with open('old_epg.xml', 'w') as old_file:
            old_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="none" generator-info-url="none">\n</tv>')

    # Read existing combined_epg.xml and parse the end time of each program
    try:
        with open('combined_epg.xml', 'r') as combined_file:
            existing_content = combined_file.read()

        # Remove header, channel info, and programs older than 36 hours
        lines = existing_content.split('\n')
        header = lines[0]
        remaining_programs = [line for line in lines[1:] if 'stop="' in line]
        current_time = datetime.utcnow()

        # Filter programs with an end time within the last 36 hours
        remaining_programs = [program for program in remaining_programs if (
            current_time - datetime.strptime(re.search(r'stop="([^"]+)"', program).group(1), '%Y%m%d%H%M%S %z')).total_seconds() < 36 * 3600]

        # Write the remaining programs to old_epg.xml
        with open('old_epg.xml', 'a') as old_file:
            old_file.write('\n'.join(remaining_programs))

        # Clean the contents of combined_epg.xml before writing new information
        with open('combined_epg.xml', 'w') as combined_file:
            combined_file.write(f"{header}\n")

    except FileNotFoundError:
        # Create combined_epg.xml if it doesn't exist
        with open('combined_epg.xml', 'w') as combined_file:
            combined_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="none" generator-info-url="none">\n</tv>')

    # Process live_status.txt and add new program information to combined_epg.xml
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

    # Combine all information into the final XMLTV content
    xmltv_content = f"{channel_info}{program_info}"
    
    # Append the new program information to combined_epg.xml
    with open('combined_epg.xml', 'a') as combined_file:
        combined_file.write(xmltv_content)

if __name__ == '__main__':
    main()
