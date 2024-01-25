import os
import yt_dlp
import time
from datetime import datetime, timedelta

# Function to retrieve scheduled live streams from a channel URL
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

# Function to extract the time until the live event starts from the error message
def get_time_until_event(error_message):
    try:
        time_str = error_message.split("will begin in ")[1].split(".")[0].strip()
        parts = time_str.split(" ")
        duration = timedelta(
            hours=int(parts[0].split('h')[0]) if 'h' in parts[0] else 0,
            minutes=int(parts[1].split('m')[0]) if 'm' in parts[1] else 0,
            seconds=int(parts[2].split('s')[0]) if 's' in parts[2] else 0
        )
        return duration
    except (IndexError, ValueError):
        print(f"Error extracting time from error message: {error_message}")
        return None

if __name__ == "__main__":
    # File containing current channels in the format: $channel_name, $group, $channel_url/live
    current_channels_file = "current_channels.txt"
    # File to store upcoming scheduled live streams
    scheduled_streams_file = "scheduled_streams.txt"

# Function to process the current channels file and write scheduled streams to the output file
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
        for stream_info in scheduled_streams:
            parts = stream_info.split('- Live - ')
            if len(parts) == 2:
                channel_name, start_time_str = map(str.strip, parts)
                start_time = datetime.strptime(start_time_str, '%a %b %d %H:%M:%S UTC %Y')
                time_until_event = get_time_until_event(stream_info)

                if time_until_event:
                    print(f"Upcoming stream for {channel_name}: {start_time} (in {time_until_event})")
                    file.write(f"{channel_name} - Live - {start_time} (in {time_until_event})\n")

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
