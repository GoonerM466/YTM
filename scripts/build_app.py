import tkinter as tk
from tkinter import filedialog
import requests
import os
import time

def run_workflows(repo_name, file_path):
    # Assuming you have GitHub Actions workflows defined in your repository
    workflows = [
        "00___new_channels__00.yml",
        "00_verify_urls.yml",
        "1_fetch_live_m3u8.yml",
        "1a_fetch_logos.yml",
        "1c_generate_m3u.yml",
        "1d_generate_xmltv.yml",
        "1e_fetch_scheduled.yml",
        "1f_channel_logger.yml"
    ]

    for workflow in workflows:
        trigger_workflow(repo_name, workflow, file_path)

def trigger_workflow(repo_name, workflow_name, file_path):
    api_url = f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow_name}/dispatches"
    headers = {"Authorization": f"token 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"}

    payload = {
        "ref": "main",  # Replace with your branch name
        "inputs": {"file_path": file_path}
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 204:
        print(f"Workflow '{workflow_name}' triggered successfully.")
    else:
        print(f"Error triggering workflow '{workflow_name}'. Status code: {response.status_code}")

def process_output_files(output_dir):
    # Implement your logic to process the output files here
    # Replace this placeholder with your actual processing logic
    print(f"Processing output files in {output_dir}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def run_application():
    file_path = entry_file_path.get()
    repo_name = "GoonerM466/YTM"  # Replace with your GitHub username and repo name

    run_workflows(repo_name, file_path)
    time.sleep(5)  # Simulate waiting for workflows to complete (adjust as needed)
    process_output_files("output")  # Replace with the actual output directory

# GUI setup
root = tk.Tk()
root.title("GitHub Workflow App")

label_file_path = tk.Label(root, text="Select Input File:")
label_file_path.pack()

entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack()

btn_browse = tk.Button(root, text="Browse", command=browse_file)
btn_browse.pack()

btn_run = tk.Button(root, text="Run Workflows", command=run_application)
btn_run.pack()

root.mainloop()
