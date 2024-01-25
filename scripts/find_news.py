import os
from googleapiclient.discovery import build
from google.auth.credentials import AnonymousCredentials
import yt_dlp
import time
from datetime import datetime
import re

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 20

def get_channel_category(channel_id):
    # You may implement your logic to determine the category of the channel based on the channel_id
    # For now, let's return None as a placeholder
    return None

def clean_text(text):
    return text

def make_api_request(api_key, max_results=50):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print("Searching...")
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.search().list(
                part="snippet",
                eventType="live",
                maxResults=max_results,
                order="viewCount",
                q="news",
                type="video"
            )
            response = request.execute()
            print("API Response:", response)  # Add this line to print the API response

            items = response.get('items', [])
            if not items:
                print(f"Maximum retries ({MAX_RETRIES}) reached. Exiting...")
                break
                return []  # Terminate the function if no items are found

            live_links = []
            for item in items:
                try:
                    retries = 0
                    while retries < MAX_RETRIES:
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

            print(f"Waiting 10 seconds before the next page...")
            time.sleep(10)
            print("Waiting...")

            elapsed_time = time.time() - start_time
            if elapsed_time > MAX_RUNTIME_SECONDS:
                print(f"Maximum runtime ({MAX_RUNTIME_SECONDS} seconds) reached. Exiting...")
                break

            retries = 0  # Reset retries if successful
            return live_links

        except Exception as e:
            print("Error during API request:", e)
            print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)
            retries += 1

    print(f"Maximum retries ({MAX_RETRIES}) reached. Exiting...")
    return []  # Handle the case where maximum retries are reached

def search_live_channels(api_key, max_results=50):
    start_time = time.time()

    live_links = make_api_request(api_key, max_results)

    # Write results to the *_live_channels.txt file
    with open('found_channels/news_live_channels.txt', 'w', encoding='utf-8') as file:
        for channel in live_links:
            file.write(f"Channel Name: {channel['name']}\n")
            file.write(f"Channel URL: {channel['url']}\n")
            file.write(f"Title: {channel['title']}\n")
            file.write(f"Description: {channel['description']}\n")
            file.write(f"Logo URL: {channel['thumbnails']['default']['url']}\n")
            file.write(f"Add this link to the update file: New: {channel['name']}, INSERT YOUR PREFERRED GROUP, {channel['url']}\n")
            file.write("\n")

if __name__ == "__main__":
    api_key = "AIzaSyAtg0O4emlRm5sAWF_8DW2ktWtgF_Wxuk4"  # Replace with your API key
    search_live_channels(api_key)
