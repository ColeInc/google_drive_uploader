# Google Drive Uploader

Powershell + Python scripts that will allow me to set certain directories to be polled, and any new files or changes made to this directory from now on will be uploaded to a defined google drive directory automatically.

## Resources:

pip install pydrive
pip install watchdog (don't know if i'll use this 100% yet)

## Prerequisites:

* settings.yaml
* drive_mappings.json
* 

## How to get the Directory ID of Google Drive Folder:

Simply just click on the directory of your choice inside google drive, and the URL will look something like:
- https://drive.google.com/drive/folders/18dvQVKdR4QpgZ9TmKbnkGbEo8iNfgvsN
The Directory ID is going to be the code you can see in this URL, E.g. "18dvQVKdR4QpgZ9TmKbnkGbEo8iNfgvsN"