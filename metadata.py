import os
import requests
from bs4 import BeautifulSoup
import yaml
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
    root = Element('epg')

    for youtube_data in youtube_data_list:
        if youtube_data:
            channel = SubElement(root, 'channel')
            metadata = SubElement(channel, 'metadata')
            metadata.text = youtube_data["metadata"]
            event_time = SubElement(channel, 'event_time')
            event_time.text = youtube_data["event_time"]

    tree = ElementTree(root)
    tree.write('combined_epg.xml')

# Read YAML file and extract channel URLs
def extract_channel_urls(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    channel_urls = []
    for entry in data:
        if 'channel_url' in entry:
            channel_urls.append(entry['channel_url'])

    return channel_urls

# Example usage
if __name__ == "__main__":
    # Specify the YAML file containing channel information
    yaml_file_path = '.github/workflows/ytm.yml'

    # Extract YouTube channel URLs from the YAML file
    youtube_urls = extract_channel_urls(yaml_file_path)

    # Scrape data for each YouTube URL
    youtube_data_list = []
    for url in youtube_urls:
        data = scrape_youtube_live_channel(url)
        if data:
            youtube_data_list.append(data)

    # Generate and export epg.xml
    generate_epg_xml(youtube_data_list)
