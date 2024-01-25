try:
    print("Searching...")
    request = youtube.search().list(
        part="snippet",
        eventType="live",
        maxResults=max_results,
        order="viewCount",
        q="sport",
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
        break

    print(f"Waiting 10 seconds before the next page...")
    time.sleep(10)
    print("Waiting...")

    elapsed_time = time.time() - start_time
    if elapsed_time > MAX_RUNTIME_SECONDS:
        print(f"Maximum runtime ({MAX_RUNTIME_SECONDS} seconds) reached. Exiting...")
        break

except Exception as e:
    print("An error occurred:", e)
    print("No live channels found.")
    break
