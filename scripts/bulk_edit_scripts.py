import os
import time

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 20

def make_api_request(api_key, max_results=50):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Your original API request code goes here
            response = make_actual_request(api_key, max_results)
            # Process the response as needed

            return response  # Exit the loop if successful

        except Exception as e:
            print("Error during API request:", e)
            print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)
            retries += 1

    print(f"Maximum retries ({MAX_RETRIES}) reached. Exiting...")
    return None  # Handle the case where maximum retries are reached

def make_actual_request(api_key, max_results=50):
    # Replace this with your actual API request code
    # It could be an HTTP request, database query, etc.
    # Here's a placeholder implementation
    print(f"Making API request with API key: {api_key}, max_results: {max_results}")
    # Return a placeholder response
    return {"data": "your_response_data"}

def bulk_edit_scripts(directory, api_key):
    for filename in os.listdir(directory):
        if filename.endswith("_live_channels.py"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            print(f"Processing script '{filename}'...")

            # Modify the script content
            modified_content = content.replace(
                'response = request.execute()',
                'response = make_api_request(api_key)'
            )

            if content != modified_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)

                print(f"Script '{filename}' has been modified.")
            else:
                print(f"Script '{filename}' is up to date.")

if __name__ == "__main__":
    script_directory = "./scripts"
    api_key = "AIzaSyAtg0O4emlRm5sAWF_8DW2ktWtgF_Wxuk4"  # Replace with your API key
    bulk_edit_scripts(script_directory, api_key)
