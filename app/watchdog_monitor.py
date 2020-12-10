import os
import sys
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google_drive_uploader import *

old = 0

class Watcher:
    
    def __init__(self):
        self.observer = Observer()

        print("---------------------------------------------")
        print("Starting google_drive_uploader!")
        print("---------------------------------------------")

    def run(self):

        event_handler = Handler()
        resp = get_list_of_local_directories()
        if resp[0] == False:
            print(resp[1])
            return
        else:
            directories_to_poll = resp[1]

        for directory in directories_to_poll:
            print("Creating observer at - {}".format(directory))
            self.observer.schedule(event_handler, directory, recursive=True)    # set recursive to false if you don't want to monitor subdirectories as well.
        self.observer.start()
        try:
            while True:
                time.sleep(2)    # maybe change this to like 60 or 300 for production
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
