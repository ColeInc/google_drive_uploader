import os
import sys
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def get_drive_directory_id(local_path):

    local_directory = os.path.dirname(local_path)

    if os.path.isfile('drive_mappings.json'):
            with open('drive_mappings.json') as file:
                data = json.load(file)
                exists = False
                for i in data['drive_mappings']:
                    print("current i: ", i)
                    if i['local_path'] == local_directory:
                        remote_id = i['remote_id']
                        exists = True
                if exists:
                    return True, remote_id
                else:
                    print("No matching entry for this local path was found inside drive_mappings.json.")
                    return False, "No matching entry for this local path was found inside drive_mappings.json."
    else:
        print("drive_mappings.json not found!")
        return False, "drive_mappings.json not found!"


def google_drive_uploader(local_path):

    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()    # will fire up your browser and navigate to a google login page, choose the account you want to access in your program, authorize the app, and you will be sent to a page saying that
    drive = GoogleDrive(g_login)    # creates a Google Drive object to handle creating files and uploading them to drive, we need to pass the g_login object to the constructor to check if authentication was successful.
    
    resp = get_drive_directory_id(local_path)
    if not(resp[0]):
        print(resp[1])
        return
    else:
        parent_directory_id = resp[1]
    
    with open(local_path, "r") as file:
        file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}], 'title': os.path.basename(local_path)})
        file_drive.SetContentString(file.read())
        file_drive.Upload()
