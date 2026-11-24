#!/bin/bash

# --- CONFIGURATION ---
DISPLAY_NUM=1
STEP=5
STATE_FILE="/tmp/waybar_brightness.tmp"
# ---------------------

# Function to send the actual DDC/CI command in the background
set_brightness_in_background() {
    pkill -f "ddcutil.*setvcp 10"
    (ddcutil --display $DISPLAY_NUM setvcp 10 $1) &
}

get_brightness() {
    local b
    b=$(ddcutil --display $DISPLAY_NUM getvcp 10 -t 2>/dev/null | awk '{print $4}')
    if [[ "$b" =~ ^[0-9]+$ ]]; then
        echo "$b" > "$STATE_FILE"
        echo "$b"
    else
        rm -f "$STATE_FILE"
        echo ""
    fi
}

case "$1" in
    "get")
        if [ -f "$STATE_FILE" ]; then
            current=$(cat "$STATE_FILE" 2>/dev/null)
            if [[ "$current" =~ ^[0-9]+$ ]]; then
                echo "$current"
            else
                get_brightness
            fi
        else
            get_brightness
        fi
        ;;
    "up")
        current=$(cat "$STATE_FILE" 2>/dev/null)
        if [[ "$current" =~ ^[0-9]+$ ]]; then
            new_brightness=$((current + STEP > 100 ? 100 : current + STEP))
            if [ "$current" -ne "$new_brightness" ]; then
                echo "$new_brightness" > "$STATE_FILE"
                set_brightness_in_background "$new_brightness"
            fi
            pkill -RTMIN+9 waybar
        fi
        ;;
    "down")
        current=$(cat "$STATE_FILE" 2>/dev/null)
        if [[ "$current" =~ ^[0-9]+$ ]]; then
            new_brightness=$((current - STEP < 0 ? 0 : current - STEP))
            if [ "$current" -ne "$new_brightness" ]; then
                echo "$new_brightness" > "$STATE_FILE"
                set_brightness_in_background "$new_brightness"
            fi
            pkill -RTMIN+9 waybar
        fi
        ;;
    "right_click")
        current=$(cat "$STATE_FILE" 2>/dev/null)
        if [[ "$current" =~ ^[0-9]+$ ]]; then
            echo "0" > "$STATE_FILE"
            set_brightness_in_background 0
            pkill -RTMIN+9 waybar
        fi
        ;;
    "left_click")
        current=$(cat "$STATE_FILE" 2>/dev/null)
        if [[ "$current" =~ ^[0-9]+$ ]]; then
            echo "100" > "$STATE_FILE"
            set_brightness_in_background 100
            pkill -RTMIN+9 waybar
        fi
        ;;
esac
