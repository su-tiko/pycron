from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import threading
import os
import time


class FileWatcher(threading.Thread):
    def __init__(self, filename, reload_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_abspath = os.path.abspath(filename)
        self.filename = os.path.basename(self.file_abspath)
        self.file_dir = os.path.dirname(self.file_abspath)

        self.stop_ev = threading.Event()
        self.reload_event = reload_queue

    def run(self):
        event_handler = CrontabEventHandler(self.file_abspath, self.reload_event)
        observer = Observer()
        observer.schedule(event_handler, self.file_dir, self.reload_event)
        observer.start()

        while not self.stop_ev.is_set():
            time.sleep(10)

        print("Stop_ev seems to has been set")

        observer.stop()
        observer.join()

    def stop(self):
        self.stop_ev.set()


class CrontabEventHandler(PatternMatchingEventHandler):
    patterns = []

    def __init__(self, filepath, reload_event, *args, **kwargs):
        self.patterns = [filepath]
        self.reload_event = reload_event
        super().__init__(*args, **kwargs)

        print("Watching patterns", self.patterns)

    def on_any_event(self, event):
        if event.src_path in self.patterns and not self.reload_event.is_set():
            print("File has been modified, setting reload event...")
            self.reload_event.set()
