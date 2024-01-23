import os
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import yt_dlp
import time

def search_live_channels(api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)

    live_links = []
    next_page_token = None

    while True:
        try:
            request = youtube.search().list(
                part="snippet",
                eventType="live",
                maxResults=max_results,
                order="viewCount",
                type="video",
                pageToken=next_page_token
            )

            response = request.execute()

            for item in response.get('items', []):
                channel_name = item['snippet']['title']
                channel_id = item['snippet']['channelId']
                group = get_channel_category(channel_id)  # You may implement this function as in your previous script
                live_links.append({
                    'name': channel_name,
                    'url': f'https://www.youtube.com/channel/{channel_id}',
                    'group': group if group else 'other',
                })

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

            print(f"Waiting 10 seconds before the next page...")
            time.sleep(10)

        except Exception as e:
            if 'quota' in str(e).lower():
                print(f"API Quota exceeded warning. Waiting 20 seconds...")
                time.sleep(20)
            else:
                raise

    return live_links
