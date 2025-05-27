#!/usr/bin/env python3
import subprocess
from pathlib import Path

def write_service_file(path, content):
    Path(path).write_text(content)
    print(f"[+] Created service file: {path}")

def run_command(command):
    try:
        print(f"[+] Running: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {e}")

def main():
    # Paths
    update_service_path = "/etc/systemd/system/update-monitor-paths.service"
    watcher_service_path = "/etc/systemd/system/watcher.service"

    # Service: One-Time Updater
    update_service = """[Unit]
Description=Update monitor_path.txt from GitHub on boot
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/bin/update_monitor_paths.py

[Install]
WantedBy=multi-user.target
"""

    # Service: Continuous Watcher
    watcher_service = """[Unit]
Description=Continuous Watcher for .desktop and .elf files
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/blocker.py
Restart=always
RestartSec=5
User=kali
Nice=10
CPUSchedulingPolicy=idle

[Install]
WantedBy=multi-user.target
"""

    # Write files
    write_service_file(update_service_path, update_service)
    write_service_file(watcher_service_path, watcher_service)

    # Reload systemd, enable and start services
    run_command(["systemctl", "daemon-reload"])
    run_command(["systemctl", "enable", "update-monitor-paths.service"])
    run_command(["systemctl", "enable", "watcher.service"])
    run_command(["systemctl", "start", "update-monitor-paths.service"])
    run_command(["systemctl", "start", "watcher.service"])

    print("[+] All services created, enabled, and started successfully.")

if __name__ == "__main__":
    main()
