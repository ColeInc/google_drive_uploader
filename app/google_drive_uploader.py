import os
import sys
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def get_list_of_local_directories():
    list_of_directories = []

    if os.path.isfile('drive_mappings.json'):
        with open('drive_mappings.json') as file:
            data = json.load(file)
            for i in data['drive_mappings']:
                list_of_directories.append(i["local_path"])
            return True, list_of_directories
    else:
        print("drive_mappings.json not found!")
        return False, "drive_mappings.json not found!"


def get_drive_directory_id(local_path):

    local_directory = os.path.dirname(local_path)

    if os.path.isfile('drive_mappings.json'):
            with open('drive_mappings.json') as file:
                data = json.load(file)
                exists = False
                for i in data['drive_mappings']:
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

    try:
        g_login = GoogleAuth()
        g_login.LocalWebserverAuth()    # will fire up your browser and navigate to a google login page, choose the account you want to access in your program, authorize the app, and you will be sent to a page saying that
        drive = GoogleDrive(g_login)    # creates a Google Drive object to handle creating files and uploading them to drive, we need to pass the g_login object to the constructor to check if authentication was successful.
        
        # get google drive directory id from drive_mappings.json
        resp = get_drive_directory_id(local_path)
        if not(resp[0]):
            print(resp[1])
            return
        else:
            parent_directory_id = resp[1]
        
        with open(local_path, "r") as file:
            # search the parent directory for an existing file with that name:
            file_list = drive.ListFile({'q': "'" + parent_directory_id + "' in parents and title = '" + 
                                            os.path.basename(local_path) + "' and trashed=false"}).GetList()
            
            if len(file_list) > 0:    #upload the existing file we found here

                print(file_list[0]['modifiedDate'], file_list[0]['title'], file_list[0]['id'])
                existing_file_id = file_list[0]['id']
                
                file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}],
                                               'id': existing_file_id, 
                                               'title': os.path.basename(local_path)})
                file_drive.SetContentString(file.read())
                file_drive.Upload()
                print("Modified file {} in Drive!".format(os.path.basename(local_path)))

            else:    # upload the file as new

                file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}], 
                                               'title': os.path.basename(local_path)})
                file_drive.SetContentString(file.read())
                file_drive.Upload()
                print("Created file {} in Drive!".format(os.path.basename(local_path)))

    except Exception as e:
        print("Error:\n", e)
