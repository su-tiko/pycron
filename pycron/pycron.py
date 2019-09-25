from .scheduler import Scheduler
from .file_watcher import FileWatcher

import threading
import argparse

file_watcher = None
scheduler = None

reload_event = threading.Event()


def launch_file_watcher(filename):
    global file_watcher

    file_watcher = FileWatcher(filename, reload_event)
    file_watcher.start()


def launch_scheduler(filename):
    global scheduler

    scheduler = Scheduler(filename, reload_event)
    scheduler.start()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('filename', help='file to read', type=str, default=".crontab")

    args = arg_parser.parse_args()

    filename = args.filename

    launch_file_watcher(filename)
    launch_scheduler(filename)


if __name__ == '__main__':
    main()
