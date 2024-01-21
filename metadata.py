import os
import requests
from bs4 import BeautifulSoup
import yaml
import re
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def scrape_youtube_live_channel(channel_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(channel_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        metadata = soup.find('meta', {'name': 'description'})
        event_time = soup.find('span', {'class': 'event-time'})

        if metadata and event_time:
            metadata_content = metadata.get('content')
            event_time_content = event_time.text.strip()
            return {"metadata": metadata_content, "event_time": event_time_content}
    else:
        print(f"Failed to retrieve the page for {channel_url}. Status code: {response.status_code}")
    return None

def generate_epg_xml(youtube_data_list):
    root = Element('tv')

    for index, youtube_data in enumerate(youtube_data_list, start=1):
        if youtube_data:
            channel = SubElement(root, 'channel', id=str(index))
            display_name = SubElement(channel, 'display-name', lang='en')
            display_name.text = f"Channel {index}"

            programme = SubElement(root, 'programme', start='20240101000000 +0000', stop='20240101235959 +0000', channel=str(index))
            title = SubElement(programme, 'title', lang='en')
            title.text = f"Program {index}"

            description = SubElement(programme, 'desc', lang='en')
            description.text = youtube_data["metadata"]

    tree = ElementTree(root)
    tree.write('combined_epg.xml', encoding='utf-8', xml_declaration=True)

# Read YAML file and extract channel URLs
def extract_channel_urls(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        content = file.read()

    # Use regular expression to find URLs in the specified format
    url_pattern = r'https://www\.youtube\.com/\S+\)'
    channel_urls = re.findall(url_pattern, content)

    return channel_urls

# Example usage
if __name__ == "__main__":
    yaml_file_path = '.github/workflows/ytm.yml'

    youtube_urls = extract_channel_urls(yaml_file_path)

    youtube_data_list = []
    for url in youtube_urls:
        # Extracting channel name from URL for reference in the metadata (you may adjust this part)
        channel_name = re.search(r'https://www\.youtube\.com/(\S+)\)', url)
        channel_name = channel_name.group(1) if channel_name else 'Unknown Channel'

        print(f"Scraping data for {channel_name} ({url})")
        data = scrape_youtube_live_channel(url)
        if data:
            youtube_data_list.append(data)

    generate_epg_xml(youtube_data_list)
