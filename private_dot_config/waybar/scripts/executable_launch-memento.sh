#!/usr/bin/env bash
# Dedicated launcher for Memento Mori Waybar Desktop Widget
# Dynamically centers on all active monitors in multi-monitor setups

# Terminate existing daemon if running
for pid in $(pgrep -f "launch-memento.py" 2>/dev/null); do
    if [ "$pid" != "$$" ]; then
        kill "$pid" 2>/dev/null
    fi
done

# If --once is passed, run synchronously and exit
if [ "$1" = "--once" ]; then
    exec python3 "$HOME/.config/waybar/scripts/launch-memento.py" --once
fi

# Run background monitor watcher to auto-recenter on monitor connect/disconnect
exec python3 "$HOME/.config/waybar/scripts/launch-memento.py"
