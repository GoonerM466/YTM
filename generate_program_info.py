from datetime import datetime, timedelta
from merge_epg import merge_epg

def convert_to_xmltv_time(time_str):
    # Convert the time string to XMLTV format
    dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Z %Y')
    return dt.strftime('%Y%m%d%H%M%S +0000')

def generate_program_info(channel_name, live_status, time_str):
    # Generate the XMLTV content for program information
    start_time = convert_to_xmltv_time(time_str)
    stop_time = (datetime.strptime(start_time, '%Y%m%d%H%M%S +0000') + timedelta(hours=3)).strftime('%Y%m%d%H%M%S +0000')

    return f'''  <programme start="{start_time}" stop="{stop_time}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

def main():
    with open('combined_epg.xml', 'r') as file:
        epg_content = file.read()

    program_info = ""

    # Parse the combined EPG XML content
    epg_lines = epg_content.splitlines()

    for line in epg_lines:
        # Assuming each line is a program entry
        program_info += line

    # Generate new program entries
    # Modify this part based on your logic for obtaining new programs
    new_channel_name = "New Channel"
    new_live_status = "Live"
    new_time_str = "Mon Jan 01 12:00:00 UTC 2023"

    program_info += generate_program_info(new_channel_name, new_live_status, new_time_str)

    # Write the updated program information to combined_epg.xml
    with open('combined_epg.xml', 'w') as file:
        file.write(program_info)

if __name__ == '__main__':
    main()
