import os
import requests
from bs4 import BeautifulSoup
import yaml
import re
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def scrape_youtube_live_channel(channel_url):
    # ... (unchanged)

def extract_channel_urls(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        content = file.read()

    # Use regular expression to find URLs in the specified format
    url_pattern = r'https://www\.youtube\.com/\S+\)'
    channel_urls = re.findall(url_pattern, content)

    return channel_urls

# ... (unchanged)

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
