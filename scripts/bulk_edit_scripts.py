import os
import re
import time

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 20

def bulk_edit_scripts(directory):
    for filename in os.listdir(directory):
        if filename.startswith("find_") and filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Add the retry mechanism
            content = re.sub(r'try:', 'try:\n    retries = 0\n    while retries < MAX_RETRIES:', content)
            content = re.sub(r'except Exception as e:.+?raise', 'except Exception as e:\n            print("Error during search:", e)\n            print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")\n            time.sleep(RETRY_DELAY_SECONDS)\n            retries += 1', content, flags=re.DOTALL)
            content = re.sub(r'print\("No live channels found."\)', 'print(f"Maximum retries ({MAX_RETRIES}) reached. Exiting...")\n            break', content)

            # Replace the existing clean_text function
            content = re.sub(r'def clean_text\(text\):.+?return cleaned_text', 'def clean_text(text):\n    return text', content, flags=re.DOTALL)

            # Replace the while True loop with a try-except block to break out of the loop
            content = re.sub(r'while True:', 'try:', content)
            content = re.sub(r'except Exception as e:.+?raise', 'except Exception as e:\n        print("No live channels found.")\n        break', content, flags=re.DOTALL)

            # Change the location of the *_live_channels.txt file
            content = re.sub(r"with open\('(\w+_live_channels.txt)', 'w', encoding='utf-8'\) as file:", "with open('found_channels/\\1', 'w', encoding='utf-8') as file:", content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Script '{filename}' has been modified.")

if __name__ == "__main__":
    script_directory = "./scripts"
    bulk_edit_scripts(script_directory)
