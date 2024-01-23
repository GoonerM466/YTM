import yt_dlp
from collections import defaultdict

def get_live_channels(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        return result.get('entries', [])

def get_channel_category(channel_id):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}', download=False)
        return result.get('categories', [])[0].lower() if result.get('categories') else None

def search_live_links(channel_names):
    live_links = []
    for channel_name in channel_names:
        search_query = f'{channel_name} live'
        search_result = get_live_channels(search_query)
        if search_result:
            channel_id = search_result[0]['channel_id']
            group = get_channel_category(channel_id)
            live_links.append({
                'name': channel_name,
                'url': search_result[0]['url'],
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

            file.write(f'New! {channel["name"]}, {channel["group"]}, {channel["url"]}\n')

if __name__ == '__main__':
    live_channels = get_live_channels('https://youtube.com/live')
    if live_channels:
        channel_names = [entry['title'] for entry in live_channels]
        live_links = search_live_links(channel_names)
        write_to_file(live_links)
        print("Script executed successfully.")
    else:
        print("No live channels found.")
