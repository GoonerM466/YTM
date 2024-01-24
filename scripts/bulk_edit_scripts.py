import os
import re

MAX_RUNTIME_SECONDS = 210  # 3.5 minutes

def bulk_edit_scripts(directory):
    for filename in os.listdir(directory):
        if filename.startswith("find_") and filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace the existing clean_text function
            content = re.sub(r'def clean_text\(text\):.+?return cleaned_text', 'def clean_text(text):\n    return text', content, flags=re.DOTALL)

            # Replace the while True loop with a try-except block to break out of the loop
            content = re.sub(r'while True:', 'try:', content)
            content = re.sub(r'except Exception as e:.+?raise', 'except Exception as e:\n        print("No live channels found.")\n        break', content, flags=re.DOTALL)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Script '{filename}' has been modified.")

if __name__ == "__main__":
    script_directory = "./.scripts"
    bulk_edit_scripts(script_directory)
