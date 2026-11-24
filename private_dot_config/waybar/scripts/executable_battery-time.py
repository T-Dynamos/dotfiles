#!/usr/bin/env python3
"""
battery-time.py: Outputs real-time remaining charge/discharge time for Waybar.
"""
import json
from pathlib import Path
import sys


def get_info():
    psy = Path("/sys/class/power_supply")
    if not psy.exists():
        return None

    for bat in sorted(psy.glob("BAT*")):
        status_file = bat / "status"
        status = status_file.read_text().strip() if status_file.exists() else ""
        if status in ("Full", "Not charging", ""):
            return None

        energy_file = bat / "energy_now"
        energy_full_file = bat / "energy_full"
        power_file = bat / "power_now"

        charge_file = bat / "charge_now"
        charge_full_file = bat / "charge_full"
        current_file = bat / "current_now"

        now, full, rate = 0, 0, 0

        if energy_file.exists() and power_file.exists():
            try:
                now = int(energy_file.read_text().strip())
                full = int(energy_full_file.read_text().strip()) if energy_full_file.exists() else now
                rate = int(power_file.read_text().strip())
            except Exception:
                pass
        elif charge_file.exists() and current_file.exists():
            try:
                now = int(charge_file.read_text().strip())
                full = int(charge_full_file.read_text().strip()) if charge_full_file.exists() else now
                rate = int(current_file.read_text().strip())
            except Exception:
                pass

        if rate < 100000:
            return None

        if status == "Discharging":
            hours_float = now / rate
            if hours_float > 50:
                return None
            hrs = int(hours_float)
            mins = int((hours_float - hrs) * 60)
            text = f"{mins}m" if hrs == 0 else f"{hrs}h {mins:02d}m"
            return {"text": text, "class": "discharging"}
        elif status == "Charging":
            if full <= now:
                return None
            hours_float = (full - now) / rate
            if hours_float > 50:
                return None
            hrs = int(hours_float)
            mins = int((hours_float - hrs) * 60)
            text = f"{mins}m" if hrs == 0 else f"{hrs}h {mins:02d}m"
            return {"text": text, "class": "charging"}

    return None


def main():
    info = get_info()
    if info:
        print(json.dumps(info))
    else:
        print(json.dumps({"text": "", "class": "idle"}))


if __name__ == "__main__":
    main()
