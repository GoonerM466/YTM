import os
from googleapiclient.discovery import build
from google.auth.credentials import AnonymousCredentials
import yt_dlp
import time
from datetime import datetime, timezone

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes

def get_channel_category(channel_id):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}', download=False)
        return result.get('categories', [])[0].lower() if result.get('categories') else None

def search_live_channels(api_key, max_results=50):
    start_time = time.time()
    youtube = build('youtube', 'v3', developerKey=api_key)

    live_links = []
    next_page_token = None

    # Set the publishedBefore parameter to the current time in RFC 3339 format
    published_before = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"

    while True:
        try:
            print("Searching...")
            request = youtube.search().list(
                part="snippet",
                eventType="live",
                maxResults=max_results,
                order="viewCount",
                publishedBefore=published_before,
                regionCode="CA",
                relevanceLanguage="en",
                type="video",
                pageToken=next_page_token
            )

            response = request.execute()
            print("API Response:", response)  # Add this line to print the API response

            items = response.get('items', [])
            if not items:
                print("No live channels found.")
                break

            for item in items:
                try:
                    # Check if the video is live, skip if it's a premiere scheduled for the future
                    if item['snippet']['liveBroadcastContent'] != 'live':
                        continue
                except KeyError:
                    pass  # Key may not be present if it's a premiere

                channel_name = item['snippet']['title']
                channel_id = item['snippet']['channelId']
                group = get_channel_category(channel_id)
                live_links.append({
                    'name': channel_name,
                    'url': f'https://www.youtube.com/channel/{channel_id}',
                    'group': group if group else 'other',
                })
                print(f"Channel found: {channel_name}")

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

            print(f"Waiting 10 seconds before the next page...")
            time.sleep(10)
            print("Waiting...")

            elapsed_time = time.time() - start_time
            if elapsed_time > MAX_RUNTIME_SECONDS:
                print(f"Maximum runtime ({MAX_RUNTIME_SECONDS} seconds) reached. Exiting...")
                break

        except Exception as e:
            if 'quota' in str(e).lower():
                print(f"API Quota exceeded warning. Waiting 20 seconds...")
                time.sleep(20)
                print("Waiting...")
            else:
                raise

    return live_links

if __name__ == "__main__":
    api_key = "AIzaSyBztHpAhFSfGbFvIkPrcPE9HbhXjQo_tSc"  # Replace with your API key
    search_live_channels(api_key)
