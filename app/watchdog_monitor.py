import os
import sys
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google_drive_uploader import google_drive_uploader

old = 0

class Watcher:
    
    def __init__(self):
        self.observer = Observer()
        if len(sys.argv) > 1:
            self.DIRECTORY_TO_MONITOR = sys.argv[1]
        else:
            # Make sure this is a full path, not relative.
            self.DIRECTORY_TO_MONITOR = "D:/Cole/PROJECTS/Google Drive Uploader/TEST_DIRECTORY"
            
        print("-----------------------------------------------------------")
        print("Starting google_drive_uploader at directory:\n{}".format(self.DIRECTORY_TO_MONITOR))
        print("-----------------------------------------------------------")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_MONITOR, recursive=True)    # set recursive to false if you don't want to monitor subdirectories as well.
        self.observer.start()
        try:
            while True:
                time.sleep(20)    # maybe change this to like 60 or 300 for production
        except Exception as e:
            self.observer.stop()
            print("Closing watchdog monitor.")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod    # the python way of defining a static method
    def on_any_event(event):

        global old
        date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            google_drive_uploader(event.src_path)
            print("{} - Create event: {}".format(date_time, event.src_path))

        elif event.event_type == 'modified':
            statbuf = os.stat(event.src_path)
            new = statbuf.st_mtime
            if (new - old) > 0.5:
                google_drive_uploader(event.src_path)
                print("{} - Modify event: {}".format(date_time, event.src_path))
            old = new

if __name__ == '__main__':
    w = Watcher()
    w.run()
