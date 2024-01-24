def generate_program_info(channel_name, live_status, time_str, existing_programs):
    # Convert time_str to XMLTV format
    new_program_start = datetime.strptime(convert_to_xmltv_time(time_str), '%Y%m%d%H%M%S +0000')

    # Round up the start time to the nearest hour
    new_program_start_rounded = round_up_to_hour(new_program_start)
    new_program_stop_rounded = (new_program_start_rounded + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')

    # Check for existing programs with the same details
    for existing_program in existing_programs:
        if existing_program['channel'] == channel_name and existing_program['start'] == new_program_start_rounded.strftime('%Y%m%d%H%M%S +0000') and existing_program['stop'] == new_program_stop_rounded:
            # Program with the same details already exists, skip adding it
            return ""

    # Create the new program
    new_program_stop = (new_program_start + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    new_program_info = f'''  <programme start="{new_program_start_rounded.strftime('%Y%m%d%H%M%S +0000')}" stop="{new_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    # Create the following program with the same details
    following_program_start = new_program_start_rounded
    following_program_stop = (following_program_start + timedelta(hours=1)).strftime('%Y%m%d%H%M%S +0000')
    following_program_info = f'''  <programme start="{following_program_start.strftime('%Y%m%d%H%M%S +0000')}" stop="{following_program_stop}" channel="{channel_name}">
    <title lang="en">{live_status}</title>
    <desc lang="en">{"{} is currently streaming live! Tune in and enjoy!".format(channel_name) if live_status == "Live" else "{} is not currently live. Check the schedule online or try again later!".format(channel_name)}</desc>
  </programme>
'''

    return new_program_info + following_program_info
