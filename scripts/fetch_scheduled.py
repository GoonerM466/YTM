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
            title = str(channel_info.get('title', ''))
            if 'This live event will begin' in title:
                # Try to extract the start time from the description
                start_time_str = channel_info.get('description', '').split('on ')[-1].strip()
                try:
                    start_time = datetime.strptime(start_time_str, '%b %d, %Y at %I:%M %p %Z')
                    return [f"{channel_info['title']} - Live - {start_time.strftime('%a %b %d %H:%M:%S UTC %Y')}"]
                except ValueError:
                    print(f"Error parsing start time for {channel_info['title']} - {start_time_str}")
                    return None

            return None
    except yt_dlp.utils.ExtractorError as e:
        print(f"Error extracting information from YouTube: {str(e)}")

        # If the error is about a video ID, try to look up the video URL
        video_id = str(e).split(":")[-1].strip()
        video_url = f"https://youtube.com/watch?v={video_id}"

        # Try to get live stream information for the video URL
        streams = get_scheduled_live_streams(video_url)

        if streams:
            return streams
        else:
            print(f"Unable to retrieve live stream information for {video_url}.")
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
    events_beginning_soon = []

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
                    events_beginning_soon.append(f"{channel_name} - Live event will begin in a few moments.")

    # Check if there are any events beginning soon before writing to the output file
    if events_beginning_soon:
        print("\nEvents beginning soon:")
        for event in events_beginning_soon:
            print(event)
    else:
        print("No events beginning soon.")

    with open(output_filename, 'w') as file:
        file.write('\n'.join(scheduled_streams))

    print(f"Scheduled streams information written to {output_filename}")

# Function to remove past entries from the scheduled streams file
def remove_past_entries(input_filename):
    current_time = time.time()
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Filter out past entries
    filtered_lines = [line for line in lines if int(line.split('-')[-1].strip()) > current_time]

    with open(input_filename, 'w') as file:
        file.writelines(filtered_lines)

# Uncomment the following line if you want to remove past entries
remove_past_entries(scheduled_streams_file)

if __name__ == "__main__":
    # File containing current channels in the format: $channel_name, $group, $channel_url/live
    current_channels_file = "current_channels.txt"
    # File to store upcoming scheduled live streams
    scheduled_streams_file = "scheduled_streams.txt"

    process_current_channels_file(current_channels_file, scheduled_streams_file)
    # Uncomment the following line if you want to remove past entries
    # remove_past_entries(scheduled_streams_file)
