# Google Drive Uploader

A Python script that will allow me to set certain directories to be polled, and any new files or changes made to this directory from now on will be uploaded to a corresponding Google Drive directory automatically.

Uses a python library called Watchdog to poll for directory changes (designed for Windows), and uses the Google Drive API to upload the files.

## Resources:

* pip install pydrive
* pip install watchdog

## Prerequisites:

* credentials.json
* settings.yaml (to make authentication to Google Drive API automatic each time)
* drive_mappings.json (local to cloud directory mapping file)
* 

## How to get the Directory ID of Google Drive Folder:

Simply just click on the directory of your choice inside google drive, and the URL will look something like:

https://drive.google.com/drive/folders/18dvQVKdR4QpgZ9TmKbnkGbEo8iNfgvsN

The Directory ID is going to be the code you can see in this URL, E.g. "18dvQVKdR4QpgZ9TmKbnkGbEo8iNfgvsN"

## Changing which Google Drive Account you upload to:

Just need to delete the credentials.json file inside the app directory and run it again, it should ask for authentication in browser and will create a new credentials.json for you automatically! You will need to move the credentials.json file back into the app directory tho, bc it gets regenerated in the directory above.


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)