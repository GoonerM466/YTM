This script pulls live streams from youtube, outputs the pulled streams into a m3u and logs new channels added & when.

New channels can be added to the "youtube_channel_info.txt" file in the follwoing format:

New: test_channel_1, catagory_name, https://www.youtube.com/@test_channel_1/live

Each new entry should be on a new line. 

The script will notice new channels have been requested and pull the new channels into the scraper.
Once the scraper completes its task, the combined m3u will be built.
Finally, the new channels file will be cleaned, the new entries will be added to the log (recently_added_channels.txt), the date & time the streams were added will be noted, and the streams will be sorted by catagory/name.

This is my first go at scripting, so Im sure its not very effecient, but it works - and took me hours!!

Planned updates:
- add an epg from the channels metadata and/or expected time the chanel will be live
- add more channels that focus on popular subjects
- clean up & make the process more efficient


