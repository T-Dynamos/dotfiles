"""
Modules package for change-wallpaper app updaters
"""

from .kitty import update_kitty
from .sway import update_sway
from .waybar import update_waybar, update_memento_mori, restart_waybars
from .firefox import update_firefox, reload_firefox_live
from .chromium import update_chromium
from .wofi import update_wofi
from .swaylock import update_swaylock
from .swaync import update_swaync
from .gtk import update_gtk
from .neovim import update_neovim
from .phylax import update_phylax
from .btop import update_btop
from .ncmpcpp import update_ncmpcpp
from .cava import update_cava

__all__ = [
    "update_kitty",
    "update_sway",
    "update_waybar",
    "update_memento_mori",
    "restart_waybars",
    "update_firefox",
    "reload_firefox_live",
    "update_chromium",
    "update_wofi",
    "update_swaylock",
    "update_swaync",
    "update_gtk",
    "update_neovim",
    "update_phylax",
    "update_btop",
    "update_ncmpcpp",
    "update_cava",
]
