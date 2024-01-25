import os
import yt_dlp
import time
from datetime import datetime

def get_scheduled_live_streams(channel_url):
    ydl = yt_dlp.YoutubeDL()
    try:
        channel_info = ydl.extract_info(channel_url, download=False)

        # Check if the channel has upcoming live broadcasts
        if 'upcoming_live_broadcasts' in channel_info:
            upcoming_streams = channel_info['upcoming_live_broadcasts']

            # Format and return the information for up to 20 upcoming live streams
            return [
                f"{channel_info['title']} - Live - {datetime.utcfromtimestamp(stream['start_time']).strftime('%a %b %d %H:%M:%S UTC %Y')}"
                for stream in upcoming_streams[:20]
            ]
        else:
            print(f"No upcoming live streams found for {channel_info['title']}.")

            # Check if the error is about a live event starting soon
            if 'This live event will begin in a few moments.' in str(channel_info.get('title', '')):
                start_time_str = channel_info.get('title', '').split(':')[-1].strip()
                start_time = datetime.strptime(start_time_str, '%I:%M %p %Z %a %b %d, %Y')
                return [f"{channel_info['title']} - Live - {start_time.strftime('%a %b %d %H:%M:%S UTC %Y')}"]

            return None
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")
        return None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading information from YouTube: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def process_current_channels_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        channels = file.readlines()

    scheduled_streams = []

    for channel in channels:
        channel_info = channel.strip().split(',')
        if len(channel_info) == 3:
            channel_name, group, channel_url = map(str.strip, channel_info)
            live_channel_url = f"{channel_url.rstrip('/')}/live"

            streams = get_scheduled_live_streams(live_channel_url)

            if streams:
                scheduled_streams.extend(streams)
            else:
                # If no upcoming streams, try the channel's main page
                streams = get_scheduled_live_streams(channel_url)
                if streams:
                    scheduled_streams.extend(streams)
                else:
                    print(f"No scheduled streams found for {channel_name}. Moving on.")

    with open(output_filename, 'w') as file:
        file.write('\n'.join(scheduled_streams))

    print(f"Scheduled streams information written to {output_filename}")

def remove_past_entries(input_filename):
    current_time = time.time()
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Filter out past entries
    filtered_lines = [line for line in lines if int(line.split('-')[-1].strip()) > current_time]

    with open(input_filename, 'w') as file:
        file.writelines(filtered_lines)

if __name__ == "__main__":
    # File containing current channels in the format: $channel_name, $group, $channel_url/live
    current_channels_file = "current_channels.txt"
    # File to store upcoming scheduled live streams
    scheduled_streams_file = "scheduled_streams.txt"

    process_current_channels_file(current_channels_file, scheduled_streams_file)
    remove_past_entries(scheduled_streams_file)
