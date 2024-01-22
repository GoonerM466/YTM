This script pulls live streams from youtube, outputs the pulled streams into a m3u and logs new channels added & when.

The scripts will keep the channels up to date with new streaming links and run every 1-3 hours.

New channels can be added to the "youtube_channel_info.txt" file in the follwoing format:

New: test_channel_1, catagory_name, https://www.youtube.com/@test_channel_1/live

Each new entry should be on a new line. 

*** no other files should be edited to avoid breaking the workflow. The only file that should be manually updated is the "youtube_channel_info.txt" to add new YT chanels to track ***

The script will notice new channels have been requested and pull the new channels into the current_channels.txt file which will be used by the YTM workflow to generate the streaming links & channel m3u8 files. While doing this the script will grab the live status of the channel and export to a seperate file (live_status.txt).
Once the scraper completes its task, the combined m3u will be built. A seperate workflow will then trigger generate_xmltv.xml to write a very basic EPG based on the live status to provide a easier to determine what channels are live.

Finally, the new channels file will be cleaned, the new entries will be added to the log (recently_added_channels.txt), the date & time the streams were added will be noted, and the streams will be sorted by catagory/name.

Once a day, a script will look for any m3u8 files in the github directory and delete them to keep the directory clean from any uninteded duplication of channels or streams. This will in turn trigger the main YTM workflow to grab the latest available streams.

This is my first go at scripting, so Im sure its not very effecient, but it works - and took me hours!!

Planned updates:
- add an epg from the channels metadata and/or expected time the chanel will be live - PARTIALLY DONE
- add more channels that focus on popular subjects
- clean up & make the process more efficient - IN PROCESS
- write a script that removes channels from the line up if they havent been online for a long time, or if the channel creator deletes their channel.


