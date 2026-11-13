"""
Configuration & Path Constants for change-wallpaper
"""

from pathlib import Path

HOME = Path.home()

WALLPAPER_TARGET = HOME / ".config" / "wallpaper"
KITTY_DIR = HOME / ".config" / "kitty"
SWAY_DIR = HOME / ".config" / "sway"
WAYBAR_DIR = HOME / ".config" / "waybar"
FIREFOX_PROFILES_DIR = HOME / ".mozilla" / "firefox"
CHROMIUM_DIR = HOME / ".config" / "chromium"
CHROMIUM_THEME_DIR = HOME / ".config" / "chromium-material-theme"
CHROMIUM_FLAGS_FILE = HOME / ".config" / "chromium-flags.conf"
WOFI_DIR = HOME / ".config" / "wofi"
SWAYLOCK_DIR = HOME / ".config" / "swaylock"
SWAYNC_DIR = HOME / ".config" / "swaync"
GTK3_DIR = HOME / ".config" / "gtk-3.0"
GTK4_DIR = HOME / ".config" / "gtk-4.0"
NVIM_DIR = HOME / ".config" / "nvim"
PHYLAX_DIR = HOME / ".config" / "phylax"
BTOP_DIR = HOME / ".config" / "btop"
NCMPCPP_DIR = HOME / ".config" / "ncmpcpp"
CAVA_DIR = HOME / ".config" / "cava"
CAVA_THEMES_DIR = CAVA_DIR / "themes"
