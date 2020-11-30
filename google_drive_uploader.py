import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

g_login = GoogleAuth()
g_login.LocalWebserverAuth()    # will fire up your browser and navigate to a google login page, choose the account you want to access in your program, authorize the app, and you will be sent to a page saying that
drive = GoogleDrive(g_login)    # creates a Google Drive object to handle creating files and uploading them to drive, we need to pass the g_login object to the constructor to check if authentication was successful.

file_path = "D:\Cole\PROJECTS\Google Drive Uploader\google_drive_uploader\test_upload.txt"

with open(file_path, "r") as file:
    file_drive = drive.CreateFile({'title': os.path.basename(file.name) })  
    file_drive.SetContentString(file.read()) 
    file_drive.Upload()
