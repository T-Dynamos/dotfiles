#!/usr/bin/env bash
# Dedicated launcher for Memento Mori Waybar Desktop Widget
# Safely terminates any existing instance and starts fresh

for pid in $(pgrep -x waybar 2>/dev/null); do
    if [ "$pid" != "$$" ] && grep -qa "memento-mori.json" /proc/"$pid"/cmdline 2>/dev/null; then
        kill "$pid" 2>/dev/null
    fi
done

# Short pause to allow surface release
sleep 0.1

exec waybar -c "$HOME/.config/waybar/memento-mori.json" -s "$HOME/.config/waybar/memento-mori.css"
