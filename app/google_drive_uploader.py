import os
import sys
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def get_list_of_local_directories():

    drive_mappings_path = 'D:/Cole/PROJECTS/Google Drive Uploader/google_drive_uploader/app/drive_mappings.json'
    list_of_directories = []

    if os.path.isfile(drive_mappings_path):
        with open(drive_mappings_path) as file:
            data = json.load(file)
            index = 0
            for value in data['drive_mappings']:
                list_of_directories.append(value["local_path"])
                if "new" in value and value["new"].lower() == "true":    # Check if this is the first time we are uploading this local directory (field "new": "True" in drive_mappings.json)

                    # get list of all files in directory and upload:
                    for file in os.listdir(value["local_path"]):
                        if os.path.isfile(os.path.join(value["local_path"], file)):
                            print("value going to google_drive_uploader: \n", value["local_path"] + "/" + file)
                            google_drive_uploader(value["local_path"] + "/" + file)

                    # now deleting the new field from this value:
                    new_value_dict = {
                        "local_path": value["local_path"],
                        "remote_id": value["remote_id"],
                        "remote_path": value["remote_path"]
                    }
                    data['drive_mappings'][index] = new_value_dict               
                index += 1
            with open(drive_mappings_path, 'w') as file:
                json.dump(data, file, indent=4)

            return True, list_of_directories
    else:
        print("drive_mappings.json not found!")
        return False, "drive_mappings.json not found!"


def get_drive_directory_id(local_path):

    drive_mappings_path = 'D:/Cole/PROJECTS/Google Drive Uploader/google_drive_uploader/app/drive_mappings.json'
    local_directory = os.path.dirname(local_path)

    if os.path.isfile(drive_mappings_path):
        with open(drive_mappings_path) as file:
            data = json.load(file)
            exists = False
            for i in data['drive_mappings']:
                # if i['local_path'] == local_directory:
                if local_directory in i['local_path']: # if the local file that was modified has a path that is inside drive_mappings.json (or part of its path, E.g. an ansestor directory matches),then fetch the remote_id for this dir
                    
                    # create some kind of double if statement here (uncomment the commented condition above as 1, have this as other) that returns a second parameter which lets method below know whether the path of file matched exactly, or if this is like a sub sub directory of the parent file. depending on that parameter in function below make an if statement that branches: 1) treat it like normal full path == full path 2) file path == a sub sub directory of the remote id directory found, then we need to do more calculations, recursive algorithm to upload all subdirectories, etc.
                    
                    remote_id = i['remote_id']
                    exists = True
                    break
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
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "D:/Cole/PROJECTS/Google Drive Uploader/google_drive_uploader/app/client_secrets.json"    # full path of your client_secrets.json file
        g_login = GoogleAuth()
        g_login.LocalWebserverAuth()    # will fire up your browser and navigate to a google login page, choose the account you want to access in your program, authorize the app, and you will be sent to a page saying that
        drive = GoogleDrive(g_login)    # creates a Google Drive object to handle creating files and uploading them to drive, we need to pass the g_login object to the constructor to check if authentication was successful.

        # Get Google Drive directory id from drive_mappings.json:
        resp = get_drive_directory_id(local_path)
        if not(resp[0]):
            return
        else:
            parent_directory_id = resp[1]
        
        with open(local_path, "r") as file:
            # Search the parent directory for an existing file with that name:
            file_list = drive.ListFile({'q': "'" + parent_directory_id + "' in parents and title = '" + 
                                            os.path.basename(local_path) + "' and trashed=false"}).GetList()
            
            if len(file_list) > 0:    # Upload the existing file we found in Google Drive here

                existing_file_id = file_list[0]['id']
                
                file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}],
                                               'id': existing_file_id, 
                                               'title': os.path.basename(local_path)})
                file_drive.SetContentString(file.read())
                file_drive.Upload()
                print("Modified file {} in Drive!".format(os.path.basename(local_path)))

            else:    # Upload the file as new

                file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}], 
                                               'title': os.path.basename(local_path)})
                file_drive.SetContentString(file.read())
                file_drive.Upload()
                print("Created file {} in Drive!".format(os.path.basename(local_path)))

    except Exception as e:
        print("Error:\n", e, sep="")
