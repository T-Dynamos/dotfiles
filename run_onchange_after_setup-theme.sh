#!/usr/bin/env bash
# Automatically applies theme across Sway, Waybar, Firefox, Kitty, etc. on new install or changes
if [ -f "$HOME/.local/bin/change-wallpaper" ]; then
    chmod +x "$HOME/.local/bin/change-wallpaper" "$HOME/.local/bin/random-wallpaper" 2>/dev/null
    "$HOME/.local/bin/change-wallpaper" || true
fi
