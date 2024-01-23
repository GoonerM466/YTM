import yt_dlp
from collections import defaultdict

def search_live_channels(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f'ytsearch:{query}', download=False)
        return result.get('entries', [])

def get_channel_category(channel_id):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}', download=False)
        return result.get('categories', [])[0].lower() if result.get('categories') else None

def search_live_links():
    live_links = []
    search_result = search_live_channels("is live")
    if search_result:
        for entry in search_result:
            channel_id = entry['channel_id']
            group = get_channel_category(channel_id)
            live_links.append({
                'name': entry['title'],
                'url': entry['url'],
                'group': group if group else 'other',
            })
    return live_links

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
    live_links = search_live_links()
    if live_links:
        print("Live Channels:")
        print_live_channels(live_links)
        write_to_file(live_links)
        print("Script executed successfully.")
    else:
        print("No live channels found.")
