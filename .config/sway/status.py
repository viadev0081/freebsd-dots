#!/usr/bin/env python3
import json
import re
import shutil
import subprocess
import time

def command(args):
    try:
        return subprocess.check_output(
            args, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

def sysctl(name):
    return command(["/sbin/sysctl", "-n", name])

def wifi_text():
    interfaces = command(["/sbin/ifconfig", "-l"]).split()

    for interface in interfaces:
        if not interface.startswith("wlan"):
            continue

        info = command(["/sbin/ifconfig", interface])
        match = re.search(
            r"^\s*ssid\s+(.+?)(?=\s+(?:channel|bssid)\b|$)",
            info,
            re.MULTILINE,
        )
        if match:
            ssid = match.group(1).strip().strip('"')
            if ssid and ssid != '""':
                return f"  {ssid}"

    return "  down"

def blocks():
    result = []

    # Значок FreeBSD из Nerd Fonts: nf-dev-freebsd
    result.append({"full_text": " ", "color": "#a74141"})

    battery = sysctl("hw.acpi.battery.life")
    if battery.isdigit():
        percentage = int(battery)
        color = "#ab4642" if percentage <= 10 else (
            "#f7ca88" if percentage <= 20 else "#a1b56c"
        )
        result.append({
            "full_text": f"BAT {percentage}%",
            "color": color,
        })

    result.append({"full_text": wifi_text(), "color": "#d8d8d8"})

    disk = shutil.disk_usage("/")
    result.append({
        "full_text": f"DISK {disk.free // (1024 ** 3)}G",
        "color": "#d8d8d8",
    })

    load = sysctl("vm.loadavg")
    if load:
        result.append({"full_text": f"LOAD {load}", "color": "#d8d8d8"})

    result.append({
        "full_text": time.strftime("%a %d %b  %H:%M"),
        "color": "#d8d8d8",
    })

    return result

print(json.dumps({"version": 1, "click_events": False}), flush=True)
print("[", flush=True)

first = True
while True:
    if not first:
        print(",", flush=True)
    print(json.dumps(blocks(), ensure_ascii=False), flush=True)
    first = False
    time.sleep(5)
