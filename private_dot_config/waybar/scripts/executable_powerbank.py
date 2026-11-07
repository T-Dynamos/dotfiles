#!/usr/bin/env python3
"""
3S PowerBank Waybar Integration Script
Streams Waybar JSON format over stdout.
Auto-detects Bluetooth state and HC-05 connection:
- If Bluetooth is OFF or device is disconnected: outputs {"text": ""} to hide module.
- If device connects: outputs compact status chip: "󰂯 96% 40W" with rich hover tooltip.
"""

import sys
import os
import re
import time
import json
import socket
import subprocess

CONFIG_PATH = "/home/tdynamos/Projects/PowerBank/powerbank_bt.json"
DEFAULT_NAMES = ["hc-05", "hc05", "powerbank", "hc-06", "hc06", "bt05", "spp-ca"]

TELEMETRY_REGEX = re.compile(
    r"V:\s*([-\d\.]+)V\s*\|\s*I:\s*([-\d\.]+)A\s*\|\s*P:\s*([-\d\.]+)W\s*\|\s*E:\s*([-\d\.]+)Wh\s*\|\s*Charge:\s*([-\d\.]+)%"
)


def emit_empty():
    """Emit empty JSON so Waybar hides the chip completely."""
    print(json.dumps({"text": "", "tooltip": "", "class": "disconnected"}), flush=True)


def is_bluetooth_powered() -> bool:
    """Check if local Bluetooth controller is powered on."""
    try:
        res = subprocess.run(
            ["bluetoothctl", "show"],
            capture_output=True,
            text=True,
            timeout=3
        )
        return "Powered: yes" in res.stdout
    except Exception:
        return False


def get_saved_mac():
    """Retrieve saved MAC from powerbank_bt.json if available."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return cfg.get("mac")
        except Exception:
            pass
    return None


def save_mac(mac, name="HC-05"):
    """Save discovered MAC to powerbank_bt.json."""
    try:
        data = {"mac": mac.upper(), "name": name, "updated_at": time.time()}
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def find_target_mac():
    """Find target MAC from saved config, paired devices, or quick scan."""
    # 1. Saved config
    saved = get_saved_mac()
    if saved:
        return saved

    # 2. Check paired devices
    try:
        res = subprocess.run(["bluetoothctl", "devices", "Paired"], capture_output=True, text=True, timeout=3)
        for line in res.stdout.splitlines():
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 3 and parts[0] == "Device":
                mac, name = parts[1].upper(), parts[2].lower()
                if any(kw in name for kw in DEFAULT_NAMES):
                    save_mac(mac, parts[2])
                    return mac
    except Exception:
        pass

    # 3. Check known devices
    try:
        res = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True, timeout=3)
        for line in res.stdout.splitlines():
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 3 and parts[0] == "Device":
                mac, name = parts[1].upper(), parts[2].lower()
                if any(kw in name for kw in DEFAULT_NAMES):
                    save_mac(mac, parts[2])
                    return mac
    except Exception:
        pass

    # 4. Quick 3-second scan
    try:
        subprocess.run(["bluetoothctl", "--timeout", "3", "scan", "on"], capture_output=True, text=True, timeout=5)
        res = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True, timeout=3)
        for line in res.stdout.splitlines():
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 3 and parts[0] == "Device":
                mac, name = parts[1].upper(), parts[2].lower()
                if any(kw in name for kw in DEFAULT_NAMES):
                    save_mac(mac, parts[2])
                    return mac
    except Exception:
        pass

    return None


def run_session(mac: str):
    """Connect to HC-05 and stream JSON lines to Waybar."""
    sock = None
    try:
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        sock.settimeout(3.0)
        sock.connect((mac, 1))

        # Once connected, set reasonable timeout for streaming lines
        sock.settimeout(2.5)
        rx_buffer = ""

        while True:
            chunk = sock.recv(256)
            if not chunk:
                break
            rx_buffer += chunk.decode("utf-8", errors="ignore")

            while "\n" in rx_buffer:
                line, rx_buffer = rx_buffer.split("\n", 1)
                line = line.strip()

                m = TELEMETRY_REGEX.search(line)
                if m:
                    v, i, p, e, charge = map(float, m.groups())

                    # Compact power string: e.g. "40W", "5.2W", "+18W", "0W"
                    if p > 0.05:
                        p_str = f" {p:.1f}W" if p < 10 else f" {p:.0f}W"
                        cls = "discharging"
                        status_str = f"Discharging ({p:.2f} W)"
                    elif p < -0.05:
                        p_str = f" +{abs(p):.1f}W" if abs(p) < 10 else f" +{abs(p):.0f}W"
                        cls = "charging"
                        status_str = f"Charging (+{abs(p):.2f} W)"
                    else:
                        p_str = " 0W"
                        cls = "idle"
                        status_str = "Idle / Standby (0.00 W)"

                    # Compact energy string: e.g. "1.25Wh", "15.3Wh"
                    if abs(e) < 10:
                        e_str = f" {e:.2f}Wh"
                    else:
                        e_str = f" {e:.1f}Wh"

                    compact_text = f"󰂯{p_str}{e_str}".strip()

                    tooltip = (
                        f"3S PowerBank & Battery Monitor\n"
                        f"───────────────────────────────\n"
                        f"Status:      {status_str}\n"
                        f"Battery:     {charge:.1f}%\n"
                        f"Power Draw:  {p:.2f} W\n"
                        f"Voltage:     {v:.2f} V\n"
                        f"Current:     {i:+.3f} A\n"
                        f"Energy:      {e:.2f} Wh (Net used)\n\n"
                        f"Left-click:  Open Terminal Monitor\n"
                        f"Right-click: Reset Wh to 0.00"
                    )

                    waybar_json = {
                        "text": compact_text,
                        "tooltip": tooltip,
                        "class": cls,
                        "percentage": int(round(max(0.0, min(100.0, charge))))
                    }
                    print(json.dumps(waybar_json), flush=True)

    except (socket.error, ConnectionError, OSError):
        pass
    finally:
        if sock:
            try:
                sock.close()
            except Exception:
                pass
        emit_empty()


def send_reset_command():
    """Connect briefly and send '0' command to reset energy counter."""
    mac = find_target_mac()
    if not mac:
        return
    try:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.settimeout(3.0)
        s.connect((mac, 1))
        s.send(b"0\n")
        time.sleep(0.1)
        s.close()
    except Exception:
        pass


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("reset", "zero"):
        send_reset_command()
        sys.exit(0)

    # Hide chip on initial startup
    emit_empty()

    while True:
        try:
            # 1. Check if Bluetooth adapter is powered on
            if not is_bluetooth_powered():
                emit_empty()
                time.sleep(3)
                continue

            # 2. Look for HC-05 device
            mac = find_target_mac()
            if not mac:
                emit_empty()
                time.sleep(5)
                continue

            # 3. Connect and stream
            run_session(mac)

            # Wait briefly after disconnect before retrying
            time.sleep(3)

        except KeyboardInterrupt:
            emit_empty()
            break
        except Exception:
            emit_empty()
            time.sleep(4)


if __name__ == "__main__":
    main()
