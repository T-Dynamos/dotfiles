#!/usr/bin/env python3
"""
Waybar Power Consumption / Charging Rate Monitor
Reads instantaneous power in watts from /sys/class/power_supply/BAT*.
Outputs formatted JSON for Waybar, or empty string when inactive/full.
"""

import json
from pathlib import Path
import sys


def get_power():
    psy = Path("/sys/class/power_supply")
    if not psy.exists():
        return None

    for bat in sorted(psy.glob("BAT*")):
        status_file = bat / "status"
        status = status_file.read_text().strip() if status_file.exists() else ""
        if status.lower() == "full":
            return None

        power_file = bat / "power_now"
        if power_file.exists():
            try:
                uw = int(power_file.read_text().strip())
                w = uw / 1_000_000.0
                if w > 0.1:
                    return w, status
            except Exception:
                pass

        curr_file = bat / "current_now"
        volt_file = bat / "voltage_now"
        if curr_file.exists() and volt_file.exists():
            try:
                c = int(curr_file.read_text().strip())
                v = int(volt_file.read_text().strip())
                w = (c * v) / 1_000_000_000_000.0
                if w > 0.1:
                    return w, status
            except Exception:
                pass

    return None


def main():
    res = get_power()
    if res:
        w, status = res
        tooltip = f"Battery Power: {w:.1f} W ({status})" if status else f"Battery Power: {w:.1f} W"
        data = {
            "text": f"{w:.1f} W",
            "tooltip": tooltip,
            "class": status.lower() if status else "power"
        }
        print(json.dumps(data))
    else:
        print("")


if __name__ == "__main__":
    main()
