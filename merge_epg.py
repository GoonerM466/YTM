import xml.etree.ElementTree as ET

def merge_epg(channel_info_file, epg_old_file, output_file):
    # Parse the channel info XML file
    channel_info_tree = ET.parse(channel_info_file)
    channel_info_root = channel_info_tree.getroot()

    # Parse the old EPG XML file
    epg_old_tree = ET.parse(epg_old_file)
    epg_old_root = epg_old_tree.getroot()

    # Find the last channel entry
    last_channel = channel_info_root.findall('.//channel')[-1]

    # Insert the content from epg_old.xml after the last channel entry
    last_channel_index = channel_info_root.index(last_channel)
    for program in epg_old_root.findall('.//programme'):
        channel_info_root.insert(last_channel_index + 1, program)

    # Write the combined information to the output file
    channel_info_tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    channel_info_file = 'channel_info.xml'
    epg_old_file = 'epg_old.xml'
    output_file = 'combined_epg.xml'

    merge_epg(channel_info_file, epg_old_file, output_file)
