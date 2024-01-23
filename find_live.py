import os
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import yt_dlp

def search_live_channels(api_key, max_results=250):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        eventType="live",
        maxResults=max_results,
        order="viewCount",
        type="video"
    )

    response = request.execute()

    live_links = []
    for item in response.get('items', []):
        channel_name = item['snippet']['title']
        channel_id = item['snippet']['channelId']
        group = get_channel_category(channel_id)  # You may implement this function as in your previous script
        live_links.append({
            'name': channel_name,
            'url': f'https://www.youtube.com/channel/{channel_id}',
            'group': group if group else 'other',
        })

    return live_links

def get_channel_category(channel_id):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}', download=False)
        return result.get('categories', [])[0].lower() if result.get('categories') else None

def write_to_file(live_channels):
    live_channels.sort(key=lambda x: (x['group'], x['name']))

    with open('all_live_channels.txt', 'w') as file:
        current_group = None

        for channel in live_channels:
            if channel['group'] != current_group:
                file.write(f'\n#####_{channel["group"]}_#####\n')
                current_group = channel['group']

        # Truncate the file before writing new entries
        file.truncate(0)

        for channel in live_channels:
            file.write(f'New! {channel["name"]}, {channel["group"]}, {channel["url"]}\n')

def print_live_channels(live_channels):
    for channel in live_channels:
        print(f'New! {channel["name"]}, {channel["group"]}, {channel["url"]}')

if __name__ == '__main__':
    youtube_api_key = "AIzaSyBztHpAhFSfGbFvIkPrcPE9HbhXjQo_tSc"
    live_links = search_live_channels(youtube_api_key)
    
    if live_links:
        print("Live Channels:")
        print_live_channels(live_links)
        write_to_file(live_links)
        print("Script executed successfully.")
    else:
        print("No live channels found.")
