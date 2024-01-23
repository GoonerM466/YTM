name: Generate XMLTV

on:
  workflow_dispatch:
  workflow_run:
    workflows:
      - "Get YouTube Live m3u8"
      - "Clean Old EPG"
    types:
      - completed

jobs:
  generate_xmltv:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip

    - name: Execute generate_channel_info.py
      run: python generate_channel_info.py > combined_epg.xml

    - name: Check if changes exist
      id: check_changes
      run: |
        git diff --exit-code || echo "Changes detected" && exit 0

    - name: Check repository status before staging
      run: git status

    - name: Stage changes
      if: steps.check_changes.outputs.return-code == '0'
      run: git add .

    - name: Check repository status after staging
      run: git status

    - name: Commit and push changes
      if: steps.check_changes.outputs.return-code == '0'
      run: |
        git config --local user.email "action@github.com" 2> /dev/null || true
        git config --local user.name "GitHub Action" 2> /dev/null || true
        git commit -m "Generate XMLTV" && git push
