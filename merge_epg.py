import xml.etree.ElementTree as ET

def merge_epg(old_epg_file, channel_info_file, output_file):
    # Parse the old EPG XML file
    old_epg_tree = ET.parse(old_epg_file)
    old_epg_root = old_epg_tree.getroot()

    # Check if there are any programs in old_epg.xml
    old_programs = old_epg_root.findall('.//programme')
    if not old_programs:
        print("No programs found in old_epg.xml. Exiting.")
        return

    # Parse the channel info XML file
    channel_info_tree = ET.parse(channel_info_file)
    channel_info_root = channel_info_tree.getroot()

    # Append old programs to channel info
    for old_program in old_programs:
        channel_info_root.append(old_program)

    # Write the combined information to the output file
    channel_info_tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    old_epg_file = 'old_epg.xml'
    channel_info_file = 'channel_info.xml'
    output_file = 'combined_epg.xml'
    merge_epg(old_epg_file, channel_info_file, output_file)
