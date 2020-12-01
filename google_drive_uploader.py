import os
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def main():
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()    # will fire up your browser and navigate to a google login page, choose the account you want to access in your program, authorize the app, and you will be sent to a page saying that
    drive = GoogleDrive(g_login)    # creates a Google Drive object to handle creating files and uploading them to drive, we need to pass the g_login object to the constructor to check if authentication was successful.

    file_path = "D:/Cole/PROJECTS/Google Drive Uploader/google_drive_uploader/test_upload.txt"
    parent_directory_id = "1vk4n3GZpVRiXvTM2mqSg90kSaCcp-s0D"
    
    # make a separate json file with key pairs for local directory + corresponding google drive directory id to upload to.

    print("The filename you provided is: {}".format(sys.argv[1]))

    with open(file_path, "r") as file:
        file_drive = drive.CreateFile({'parents': [{'id': parent_directory_id}], 'title': os.path.basename(file_path)})
        file_drive.SetContentString(file.read())
        file_drive.Upload()

main()