def process_channel_info(input_file, output_file, current_channels_file):
    with open(input_file, 'r') as input_file:
        input_lines = input_file.readlines()

    if not input_lines:
        print("Input file is empty. Script finished.")
        return

    with open(current_channels_file, 'r') as current_channels_file:
        current_channels = current_channels_file.readlines()

    with open(output_file, 'a') as output_file:
        for line in input_lines:
            if line.startswith("New"):
                channel_name = line.split("New: ")[1].split(" ,")[0]
                if not any(channel_name in channel for channel in current_channels):
                    output_file.write(line)
            else:
                output_file.write(line)

    print("Script finished processing.")

# Replace these file names with the actual file paths
input_file_path = "youtube_channel_info.txt"
output_file_path = "current_channels.txt"
current_channels_file_path = "current_channels.txt"

process_channel_info(input_file_path, output_file_path, current_channels_file_path)
