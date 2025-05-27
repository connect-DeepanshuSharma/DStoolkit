#!/usr/bin/env python3
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path


LOG_TAG = "DesktopFileWatcher"
PATHS_FILE = "/usr/local/bin/err.txt"
TARGET_EXT = (".desktop", ".elf")

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(TARGET_EXT):
            try:
                os.remove(event.src_path)
                log_syslog(f"Deleted suspicious file: {event.src_path}")
            except Exception as e:
                log_syslog(f"Failed to delete {event.src_path}: {e}")

def log_syslog(message):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(LOG_TAG).info(message)

def get_watch_paths():
    if not Path(PATHS_FILE).exists():
        log_syslog(f"Paths file does not exist: {PATHS_FILE}")
        return []
    
    paths = []
    for line in Path(PATHS_FILE).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        expanded = os.path.expandvars(os.path.expanduser(line))
        if Path(expanded).is_dir():
            paths.append(expanded)
        else:
            log_syslog(f"Invalid watch path in file: {line} (resolved to: {expanded})")
    return paths
def main():
    observer = Observer()
    handler = FileHandler()
    watch_dirs = get_watch_paths()
    print(watch_dirs)
    if not watch_dirs:
        log_syslog("No valid directories to watch. Exiting.")
        return

    for path in watch_dirs:
    	
    	observer.schedule(handler, path=path, recursive=True)
    
    observer.start()
    log_syslog(f"Watching: {', '.join(watch_dirs)}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
