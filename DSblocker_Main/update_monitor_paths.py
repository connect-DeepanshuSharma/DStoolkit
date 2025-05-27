#!/usr/bin/env python3
import hashlib
import subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing 'requests' module. Install with: pip3 install requests")
    exit(1)

GITHUB_PATHS_URL = "https://raw.githubusercontent.com/connect-DeepanshuSharma/DStoolkit/refs/heads/main/DSblocker/err.txt"
LOCAL_PATHS_FILE = Path("/usr/local/bin/err.txt")
WATCHER_SERVICE = "watcher.service"

def fetch_remote():
    try:
        resp = requests.get(GITHUB_PATHS_URL, timeout=5)
        if resp.status_code == 200:
            return resp.text
    except:
        pass
    return None

def sha256(text): return hashlib.sha256(text.encode()).hexdigest()

def read_file(file: Path): return file.read_text() if file.exists() else ""

def write_file(file: Path, content: str): file.write_text(content)

def restart_service(name):
    subprocess.run(["systemctl", "restart", name], check=False)

def main():
    remote = fetch_remote()
    if not remote:
        return

    local = read_file(LOCAL_PATHS_FILE)
    if sha256(remote) != sha256(local):
        write_file(LOCAL_PATHS_FILE, remote)
        restart_service(WATCHER_SERVICE)

if __name__ == "__main__":
    main()
