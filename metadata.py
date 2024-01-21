import os
import requests
from bs4 import BeautifulSoup
import yaml
import re
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from googleapiclient.discovery import build

# Try to import googleapiclient, and install it if not present
try:
    from googleapiclient.discovery import build
except ImportError:
    print("google-api-python-client not found. Installing...")
    os.system("pip install google-api-python-client")
    from googleapiclient.discovery import build

# Function to get channel logo from YouTube Data API
def get_channel_logo(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.channels().list(part='snippet', id=channel_id).execute()

    if 'items' in response and response['items']:
        return response['items'][0]['snippet']['thumbnails']['default']['url']
    else:
        return None

# Function to scrape YouTube live channel information
def scrape_youtube_live_channel(channel_url, api_key):
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

            # Extract channel ID from URL
            channel_id_match = re.search(r'https://www\.youtube\.com/channel/(\S+)', channel_url)
            channel_id = channel_id_match.group(1) if channel_id_match else None

            # Get channel logo using YouTube Data API
            channel_logo_url = get_channel_logo(api_key, channel_id) if channel_id else None

            # Dump raw metadata to file
            with open('meta_dump.txt', 'a', encoding='utf-8') as dump_file:
                dump_file.write(f"Channel: {channel_url}\n")
                dump_file.write(f"Metadata: {metadata_content}\n")
                dump_file.write(f"Event Time: {event_time_content}\n\n")

            return {"metadata": metadata_content, "event_time": event_time_content, "channel_logo": channel_logo_url}
    else:
        print(f"Failed to retrieve the page for {channel_url}. Status code: {response.status_code}")
    return None

def generate_epg_xml(youtube_data_list):
    root = Element('tv', generator_info_name="none", generator_info_url="none")

    for index, youtube_data in enumerate(youtube_data_list, start=1):
        if youtube_data:
            # Channel information
            channel_name = re.search(r'https://www\.youtube\.com/(\S+)\)', youtube_data["url"])
            channel_name = channel_name.group(1) if channel_name else f'Unknown_Channel_{index}'

            channel = SubElement(root, 'channel', id=channel_name)
            icon = SubElement(channel, 'icon', src=youtube_data["channel_logo"])
            display_name = SubElement(channel, 'display-name', lang='en')
            display_name.text = channel_name

            # Event information
            programme = SubElement(root, 'programme', start='20240101000000 +0000', stop='20240101235959 +0000', channel=channel_name)
            title = SubElement(programme, 'title', lang='en')
            title.text = f"Event_{index}"

            desc = SubElement(programme, 'desc', lang='en')
            desc.text = youtube_data["metadata"]

            category = SubElement(programme, 'category', lang='en')
            category.text = f"Group_{index}"

            hashtag_category = SubElement(programme, 'category', lang='en')
            hashtag_category.text = f"Hashtags_{index}"

            icon = SubElement(programme, 'icon', src=youtube_data["channel_logo"])

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
    api_key = "AIzaSyBztHpAhFSfGbFvIkPrcPE9HbhXjQo_tSc"  # Replace with your YouTube API key
    yaml_file_path = '.github/workflows/ytm.yml'

    youtube_urls = extract_channel_urls(yaml_file_path)

    youtube_data_list = []
    for url in youtube_urls:
        # Extracting channel name from URL for reference in the metadata (you may adjust this part)
        data = {"url": url}
        print(f"Scraping data for {url}")
        metadata = scrape_youtube_live_channel(url, api_key)
        if metadata:
            data.update(metadata)
            youtube_data_list.append(data)

    generate_epg_xml(youtube_data_list)
