#!/usr/bin/env python3
"""
power-profile.py: Combined Power Profile & Battery Charge/Discharge Time for Waybar.
Formats as `{time} {icon}` (or `{icon}` when idle/full) with click-to-cycle power profiles.
"""
import json
from pathlib import Path
import subprocess
import sys

ORDER = ["power-saver", "balanced", "performance"]
ICONS = {
    "power-saver": "",
    "balanced": "",
    "performance": "",
}


def get_profile():
    state_file = Path("/var/lib/power-profiles-daemon/state.ini")
    if state_file.exists():
        try:
            for line in state_file.read_text().splitlines():
                if line.startswith("Profile="):
                    val = line.split("=", 1)[1].strip()
                    if val in ORDER:
                        return val
        except Exception:
            pass

    try:
        res = subprocess.run(
            [
                "gdbus", "call", "--system", "--dest", "net.hadess.PowerProfiles",
                "--object-path", "/net/hadess/PowerProfiles",
                "--method", "org.freedesktop.DBus.Properties.Get",
                "net.hadess.PowerProfiles", "ActiveProfile"
            ],
            capture_output=True, text=True, timeout=1
        )
        val = res.stdout.strip().strip("(),<>'\" ")
        if val in ORDER:
            return val
    except Exception:
        pass

    return "balanced"


def cycle_profile():
    curr = get_profile()
    try:
        idx = ORDER.index(curr)
        nxt = ORDER[(idx + 1) % len(ORDER)]
    except ValueError:
        nxt = "balanced"
    subprocess.run(["powerprofilesctl", "set", nxt], check=False)


def get_battery_time():
    psy = Path("/sys/class/power_supply")
    if not psy.exists():
        return "", ""

    for bat in sorted(psy.glob("BAT*")):
        status_file = bat / "status"
        status = status_file.read_text().strip() if status_file.exists() else ""
        capacity_file = bat / "capacity"
        capacity = int(capacity_file.read_text().strip()) if capacity_file.exists() else 0

        if status in ("Full", "Not charging", "") or (status == "Charging" and capacity >= 100):
            return "", "idle"

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
            return "", "idle"

        if status == "Discharging":
            hours_float = now / rate
            if hours_float > 50:
                return "", "discharging"
            hrs = int(hours_float)
            mins = int((hours_float - hrs) * 60)
            if hrs == 0 and mins == 0:
                text = "<1m"
            elif hrs == 0:
                text = f"{mins}m"
            else:
                text = f"{hrs}h {mins:02d}m"
            return text, "discharging"
        elif status == "Charging":
            if full <= now:
                return "", "idle"
            hours_float = (full - now) / rate
            if hours_float > 50:
                return "", "charging"
            hrs = int(hours_float)
            mins = int((hours_float - hrs) * 60)
            if hrs == 0 and mins == 0:
                return "", "idle"
            text = f"{mins}m" if hrs == 0 else f"{hrs}h {mins:02d}m"
            return text, "charging"

    return "", ""


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("cycle", "next"):
        cycle_profile()
        return

    prof = get_profile()
    time_str, bat_st = get_battery_time()
    icon = ICONS.get(prof, "")

    if time_str:
        display_text = f"{time_str} {icon}"
    else:
        display_text = icon

    tooltip_lines = [f"Power Profile: {prof}"]
    if bat_st == "charging" and time_str:
        tooltip_lines.append(f"Time to full charge: {time_str}")
    elif bat_st == "discharging" and time_str:
        tooltip_lines.append(f"Time to discharge: {time_str}")
    elif bat_st == "idle":
        tooltip_lines.append("Fully charged / AC connected")
    tooltip_lines.append("Click: Switch profile")

    classes = [prof]
    if bat_st:
        classes.append(bat_st)

    out = {
        "text": display_text,
        "tooltip": "\n".join(tooltip_lines),
        "class": " ".join(classes),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
