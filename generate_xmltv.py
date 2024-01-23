import re
from datetime import datetime, timedelta
import os

def parse_live_status(line):
    try:
        # Parse the information from the live_status.txt line
        match = re.match(r'^([\w_]+) - (Live|Not Live) - (.+ UTC \d{4})$', line)
        if match:
            channel_name, live_status, time_str = match.groups()
            print(f"Parse the information from the live_status.txt line - success!")
            return channel_name, live_status, time_str
        else:
            raise ValueError("Failed to parse line: {}".format(line))
    except Exception as e:
        print(f"Error parsing line: {e}")
        return None

def convert_to_xmltv_time(time_str):
    try:
        # Convert the time string to XMLTV format
        dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Z %Y')
        print(f"Convert the time string to XMLTV format - success!")
        return dt.strftime('%Y%m%d%H%M%S +0000')
    except Exception as e:
        print(f"Error converting time string: {e}")
        return None

def generate_channel_info(channel_name):
    try:
        # Generate the XMLTV content for channel information
        result = f'''  <channel id="{channel_name}">
    <display-name lang="en">{channel_name}</display-name>
  </channel>
'''
        print(f"Generate the XMLTV content for channel information - success!")
        return result
    except Exception as e:
        print(f"Error generating channel information: {e}")
        return None

def generate_program_info(channel_name, live_status, time_str):
    try:
        # Generate the XMLTV content for program information
        start_time = convert_to_xmltv_time(time_str)
        stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

        result = f'''  <programme start="{start_time}" stop="{stop_time}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''
        print(f"Generate the XMLTV content for program information - success!")
        return result
    except Exception as e:
        print(f"Error generating program information: {e}")
        return None

def main():
    try:
        # Check if old_epg.xml exists, if not, create it
        if not os.path.exists('old_epg.xml'):
            with open('old_epg.xml', 'w') as old_file:
                old_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="none" generator-info-url="none">\n</tv>')
            print(f"Check if old_epg.xml exists, if not, create it - success!")
        return result
    except Exception as e:
        print(f"Error checking for old_epg, could not create either: {e}")
        return None

        # Read existing combined_epg.xml and parse the end time of each program
        try:
            with open('combined_epg.xml', 'r') as combined_file:
                existing_content = combined_file.read()
            print(f"Read existing combined_epg.xml and parse the end time of each program - success!")
        return result
    except Exception as e:
        print(f"Error reading exiating epg: {e}")
        return None

            # Remove header, channel info, and programs older than 36 hours
            lines = existing_content.split('\n')
            header = lines[0]
            remaining_programs = [line for line in lines[1:] if 'stop="' in line]
            current_time = datetime.utcnow()
            print(f"Remove header, channel info, and programs older than 36 hours - success!")
        return result
    except Exception as e:
        print(f"Error removing older programs: {e}")
        return None
            
            # Filter programs with an end time within the last 36 hours
            remaining_programs = [program for program in remaining_programs if (
                current_time - datetime.strptime(re.search(r'stop="([^"]+)"', program).group(1), '%Y%m%d%H%M%S %z')).total_seconds() < 36 * 3600]
            print(f"Read existing combined_epg.xml and parse the end time of each program - success!")
        return result
    except Exception as e:
        print(f"Error filtering old programs: {e}")
        return None

            # Write the remaining programs to old_epg.xml
            with open('old_epg.xml', 'a') as old_file:
                old_file.write('\n'.join(remaining_programs))
            print(f"Write the remaining programs to old_epg.xml - success!")
        return result
    except Exception as e:
        print(f"Error writing programs to old_epg: {e}")
        return None

            # Clean the contents of combined_epg.xml before writing new information
            with open('combined_epg.xml', 'w') as combined_file:
                combined_file.write(f"{header}\n")
            print(f"Clean the contents of combined_epg.xml before writing new information - success!")
        return result
    except Exception as e:
        print(f"Error cleaning combined_epg: {e}")
        return None

        except FileNotFoundError:
            # Create combined_epg.xml if it doesn't exist
            with open('combined_epg.xml', 'w') as combined_file:
                combined_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="none" generator-info-url="none">\n</tv>')
            print(f"Create combined_epg.xml - success!")
        return result
    except Exception as e:
        print(f"Error creating combined_epg: {e}")
        return None

        # Process live_status.txt and add new program information to combined_epg.xml
        with open('live_status.txt', 'r') as file:
            lines = file.readlines()
            print(f"Process live_status.txt and add new program information to combined_epg.xml - success!")
        return result
    except Exception as e:
        print(f"Error adding new programs: {e}")
        return None

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
        print(f"Combine all information into the final XMLTV content - success!")
        return result
    except Exception as e:
        print(f"Error combinbing old and new epg: {e}")
        return None

        # Append the new program information to combined_epg.xml
        with open('combined_epg.xml', 'a') as combined_file:
            combined_file.write(xmltv_content)
        print(f"Append the new program information to combined_epg.xml - success!")
        return result
    except Exception as e:
        print(f"Error appending newer programs: {e}")
        return None

    except Exception as e:
        print(f"Error in main(): {e}")

if __name__ == '__main__':
    main()
