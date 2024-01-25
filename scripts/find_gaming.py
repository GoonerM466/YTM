import os
from googleapiclient.discovery import build
from google.auth.credentials import AnonymousCredentials
import yt_dlp
import time
from datetime import datetime
import re

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes

def get_channel_category(channel_id):
    # You may implement your logic to determine the category of the channel based on the channel_id
    # For now, let's return None as a placeholder
    return None

def clean_text(text):
    return text

def search_live_channels(api_key, max_results=50):
    start_time = time.time()
    youtube = build('youtube', 'v3', developerKey=api_key)

    live_links = []
    next_page_token = None

    try:
        print("Searching...")
        request = youtube.search().list(
            part="snippet",
            eventType="live",
            maxResults=max_results,
            order="viewCount",
            q="gaming",
            type="video",
            pageToken=next_page_token
        )

        response = request.execute()
        print("API Response:", response)  # Add this line to print the API response

        items = response.get('items', [])
        if not items:
            print("No live channels found.")
            return live_links  # Terminate the function if no items are found

        for item in items:
            try:
                # Check if the video is live, skip if it's a premiere scheduled for the future
                if item['snippet']['liveBroadcastContent'] != 'live':
                    continue
            except KeyError:
                pass  # Key may not be present if it's a premiere

            channel_name = clean_text(item['snippet']['channelTitle'])
            channel_id = item['snippet']['channelId']
            group = get_channel_category(channel_id)  # You may implement this function as in your previous script
            
            # Construct channel URL, removing spaces
            channel_url = f'https://youtube.com/@{channel_name.replace(" ", "")}/live'

            title = clean_text(item['snippet']['title'])
            channel_logo = item['snippet']['thumbnails']['default']['url']
            channel_description = clean_text(item['snippet']['description'])

            live_links.append({
                'name': channel_name,
                'url': channel_url,
                'title': title,
                'thumbnails': {'default': {'url': channel_logo}},
                'description': channel_description,
                'group': group if group else 'other',
            })
            print(f"Channel found: {channel_name}")

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            return live_links  # Terminate the function if there is no next page

        print(f"Waiting 10 seconds before the next page...")
        time.sleep(10)
        print("Waiting...")

        elapsed_time = time.time() - start_time
        if elapsed_time > MAX_RUNTIME_SECONDS:
            print(f"Maximum runtime ({MAX_RUNTIME_SECONDS} seconds) reached. Exiting...")
            return live_links  # Terminate the function if maximum runtime is reached

    except Exception as e:
        print("Error during search:", e)
        print("No live channels found.")

    return live_links

if __name__ == "__main__":
    api_key = "AIzaSyAtg0O4emlRm5sAWF_8DW2ktWtgF_Wxuk4"  # Replace with your API key
    live_channels = search_live_channels(api_key)

    # Write results to the all_live_channels.txt file
    with open('found_channels/gaming_live_channels.txt', 'w', encoding='utf-8') as file:
        for channel in live_channels:
            file.write(f"Channel Name: {channel['name']}\n")
            file.write(f"Channel URL: {channel['url']}\n")
            file.write(f"Title: {channel['title']}\n")
            file.write(f"Description: {channel['description']}\n")
            file.write(f"Logo URL: {channel['thumbnails']['default']['url']}\n")
            file.write(f"Add this link to the update file: New: {channel['name']}, INSERT YOUR PREFERRED GROUP, {channel['url']}\n")
            file.write("\n")
