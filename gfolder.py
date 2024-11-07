#!/usr/bin/env python3
# coding=utf-8
import os, re, sys, time
import requests
import gdown
import lxml.html
# Solve the limit of 50 on the maximum number of files downloaded in single folder on Google Drive. You can use this script to recursively download a folder, including all the files and subfolders on Google Drive.
# based on https://gist.github.com/DaniDipp/744b52adb341e41fdf871346a59e442c. thanks to @DaniDipp
# fixed the utf-8 folder name problem, by fish4terrisa-MSDSM
# really a dirty hack :)
def recursive_gdown(folder_id, current_path=''): 
    url = f"https://drive.google.com/embeddedfolderview?id={folder_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.content}")
        return
    
    data = str(response.content)
    html_element = lxml.html.document_fromstring(response.text)
    folder_title = html_element.xpath('//title')[0].text_content()

    # Pattern to find files and folders
    file_pattern = r"https://drive\.google\.com/file/d/([-\w]{25,})/view\?usp=drive_web"
    folder_pattern = r"https://drive\.google\.com/drive/folders/([-\w]{25,})"
    files = re.findall(file_pattern, data)
    folders = re.findall(folder_pattern, data)
    print(f"Found {len(files)} files and {len(folders)} folders")
    # Create directory for current folder if it doesn't exist
    print(folder_title)
    path = os.path.join(current_path, folder_title)
    os.makedirs(path, exist_ok=True)
    print(f"Processing directory: {path}")

    # Download files
    for i, file_id in enumerate(files):
        file_directory = f"{path}/"
        print(f"Downloading File {i + 1}/{len(files)}: {file_id}")
        while True:
            try:
                gdown.download(f"https://drive.google.com/uc?id={file_id}", file_directory, quiet=False, resume=True)
                break
            except gdown.exceptions.FileURLRetrievalError:
                print("Failed to download file. Retrying in 10 mins...")
                time.sleep(10 * 60)

    # Recursively process each sub-folder
    for folder_id in folders:
        recursive_gdown(folder_id, path)
        
if __name__ == "__main__": 
    if(len(sys.argv) < 2):
        print(f"Usage: {sys.argv[0]} <gdrive-folder-id>")
        exit(1)
    folder_id = sys.argv[1]
    if(not bool(re.match(r"^[-\w]{25,}$", folder_id))):
        print(f"Invalid id: {folder_id}")
        exit(1)
    recursive_gdown(folder_id, ".")

