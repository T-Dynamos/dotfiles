#!/usr/bin/env python3
"""
launch-memento.py: Dynamic multi-monitor launcher for the Memento Mori desktop widget.
Detects all active Sway outputs, calculates exact geometric vertical center for each monitor,
generates ~/.config/waybar/memento-mori.json per output, and starts Waybar.
Also monitors Sway output events (connect/disconnect/toggle) and auto-recenters.
"""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

CONFIG_DIR = Path.home() / ".config" / "waybar"
MEMENTO_JSON = CONFIG_DIR / "memento-mori.json"
MEMENTO_CSS = CONFIG_DIR / "memento-mori.css"
LIFESPAN_SCRIPT = CONFIG_DIR / "scripts" / "lifespan.py"

# Widget height is approx 54px (13px font + 32px padding + 3px border + 6px box-shadow/line-height)
WIDGET_HALF_HEIGHT = 27


def get_active_outputs():
    try:
        res = subprocess.run(
            ["swaymsg", "-t", "get_outputs"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode != 0:
            return []
        outputs = json.loads(res.stdout)
        active = []
        for o in outputs:
            if o.get("active") and o.get("rect"):
                rect = o["rect"]
                width = rect.get("width", 0)
                height = rect.get("height", 0)
                if width > 0 and height > 0:
                    active.append({
                        "name": o["name"],
                        "width": width,
                        "height": height
                    })
        return active
    except Exception as e:
        print(f"[Warning] Failed to query sway outputs: {e}", file=sys.stderr)
        return []


def build_config(active_outputs):
    if not active_outputs:
        # Fallback to standard 1080p center if sway is not ready
        return [{
            "name": "memento-default",
            "layer": "bottom",
            "position": "top",
            "margin-top": 513,
            "exclusive": False,
            "passthrough": True,
            "modules-center": ["custom/memento-mori"],
            "custom/memento-mori": {
                "exec": f"python3 {LIFESPAN_SCRIPT}",
                "return-type": "json",
                "interval": 60,
                "format": "{}",
                "tooltip": False
            }
        }]

    bars = []
    for out in active_outputs:
        name = out["name"]
        height = out["height"]
        # Exact vertical center on this monitor
        margin_top = max(0, int(height / 2 - WIDGET_HALF_HEIGHT))
        bars.append({
            "name": f"memento-{name}",
            "output": name,
            "layer": "bottom",
            "position": "top",
            "margin-top": margin_top,
            "exclusive": False,
            "passthrough": True,
            "modules-center": ["custom/memento-mori"],
            "custom/memento-mori": {
                "exec": f"python3 {LIFESPAN_SCRIPT}",
                "return-type": "json",
                "interval": 60,
                "format": "{}",
                "tooltip": False
            }
        })
    return bars


def restart_waybar_instance():
    # Kill any existing memento-mori waybar processes
    try:
        res = subprocess.run(["pgrep", "-f", "memento-mori.json"], capture_output=True, text=True)
        my_pid = os.getpid()
        for line in res.stdout.strip().splitlines():
            pid = int(line.strip())
            if pid != my_pid:
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
    except Exception:
        pass

    time.sleep(0.15)

    # Spawn new instance
    subprocess.Popen(
        ["waybar", "-c", str(MEMENTO_JSON), "-s", str(MEMENTO_CSS)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )


def update_and_launch():
    outputs = get_active_outputs()
    config = build_config(outputs)
    new_content = json.dumps(config, indent=2)

    MEMENTO_JSON.write_text(new_content, encoding="utf-8")
    restart_waybar_instance()
    print(f"Memento Mori widget launched for active outputs: {[o['name'] for o in outputs]}")


def listen_for_output_changes():
    try:
        proc = subprocess.Popen(
            ["swaymsg", "-t", "subscribe", "-m", '["output"]'],
            stdout=subprocess.PIPE,
            text=True
        )
        for _ in iter(proc.stdout.readline, ""):
            # Output event detected, debounce slightly to allow sway mode commit
            time.sleep(0.3)
            outputs = get_active_outputs()
            config = build_config(outputs)
            new_content = json.dumps(config, indent=2)
            try:
                current_content = MEMENTO_JSON.read_text(encoding="utf-8")
            except Exception:
                current_content = ""
            if new_content != current_content:
                MEMENTO_JSON.write_text(new_content, encoding="utf-8")
                restart_waybar_instance()
                print(f"[Auto-recenter] Outputs changed. Updated for: {[o['name'] for o in outputs]}")
    except Exception as e:
        print(f"[Warning] Output change listener ended: {e}", file=sys.stderr)


def main():
    update_and_launch()

    # If run with --once, exit immediately (e.g. from change-wallpaper)
    if "--once" in sys.argv:
        return

    # Otherwise keep running in background to react to monitor connect/disconnect/toggles
    listen_for_output_changes()


if __name__ == "__main__":
    main()
