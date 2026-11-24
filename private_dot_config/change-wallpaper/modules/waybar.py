"""
Waybar Status Bar Theme Updater
"""

import datetime
import subprocess
import time
from config import WAYBAR_DIR


def update_waybar(pal):
    style_css = WAYBAR_DIR / "style.css"
    content = f"""* {{
  border: none;
  border-radius: 0;
  min-height: 0;
  font-family: Material Design Icons, JetBrainsMono Nerd Font;
  font-size: 13px;
}}

window#waybar {{
  background-color: {pal["surface"]};
  transition-property: background-color;
  transition-duration: 0.25s;
}}

/* Completely transparent when no window is on the workspace */
window#waybar.empty {{
  background-color: transparent;
}}

window#waybar.hidden {{
  opacity: 0.5;
}}

#window {{
  background: transparent;
  padding: 0;
  margin: 0;
  border: none;
}}

/* ==========================================================
   LEFT MODULE CLUSTER (Clean Material 3 Container)
   group/hardware: cpu -> temperature -> memory
   ========================================================== */
#hardware {{
  background-color: {pal["surface_container"]};
  border: 1px solid {pal["outline_variant"]};
  border-radius: 18px;
  margin: 10px 4px 10px 10px;
  padding: 4px 8px;
}}

#hardware * {{
  background: transparent;
  border: none;
  margin: 0;
  padding: 0;
  color: {pal["on_surface"]};
  font-weight: 500;
}}

#hardware #cpu {{
  padding-left: 8px;
  padding-right: 9px;
}}

#hardware #temperature {{
  padding-left: 8px;
  padding-right: 6px;
}}

#hardware #memory {{
  padding-left: 9px;
  padding-right: 8px;
}}

/* ==========================================================
   WORKSPACES (Clean Material 3 Pill Buttons)
   ========================================================== */
#workspaces {{
  background-color: transparent;
  margin: 6px 2px;
}}

#workspaces button {{
  all: initial;
  min-width: 0;
  padding: 4px 17px;
  margin: 2px 3px;
  border-radius: 16px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface_variant"]};
  border: 1px solid {pal["outline_variant"]};
  transition: all 0.2s ease;
}}

#workspaces button:hover {{
  color: {pal["primary"]};
  background-color: {pal["surface_container_high"]};
  border-color: {pal["primary"]};
}}

#workspaces button.focused,
#workspaces button.visible {{
  color: {pal["surface"]};
  background-color: {pal["primary"]};
  border-color: {pal["primary"]};
  font-weight: bold;
}}

#workspaces button.focused:hover,
#workspaces button.visible:hover {{
  color: {pal["surface"]};
  background-color: {pal["primary"]};
  border-color: {pal["primary"]};
  opacity: 0.9;
}}

#workspaces button.urgent {{
  color: {pal["on_error"]};
  background-color: {pal["error"]};
  border-color: {pal["error"]};
}}

/* ==========================================================
   CENTER (Clock, Mode & MPRIS Capsule)
   ========================================================== */
#clock {{
  margin: 10px 4px;
  padding: 4px 17px;
  color: {pal["on_surface"]};
  border-radius: 18px;
  background-color: {pal["surface_container_high"]};
  border: 1px solid {pal["outline_variant"]};
  font-weight: 600;
}}

#custom-player-prev,
#custom-player-next,
#mpris {{
  background: transparent;
  padding: 0;
  margin: 0;
  border: none;
}}

#custom-player-prev.active {{
  margin: 10px 0 10px 4px;
  padding: 4px 8px 4px 12px;
  border-radius: 18px 0 0 18px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border: 1px solid {pal["outline_variant"]};
  border-right: none;
  font-weight: 500;
  transition: all 0.2s ease;
}}

#custom-player-prev.active:hover {{
  background-color: {pal["surface_container_high"]};
  color: {pal["primary"]};
}}

#mpris.playing,
#mpris.paused {{
  margin: 10px 0;
  padding: 4px 10px;
  border-radius: 0;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
  transition: all 0.2s ease;
}}

#mpris.playing {{
  color: {pal["on_surface"]};
  background-color: {pal["surface_container_high"]};
}}

#mpris.paused {{
  color: {pal["on_surface_variant"]};
}}

#custom-player-next.active {{
  margin: 10px 4px 10px 0;
  padding: 4px 12px 4px 8px;
  border-radius: 0 18px 18px 0;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border: 1px solid {pal["outline_variant"]};
  border-left: none;
  font-weight: 500;
  transition: all 0.2s ease;
}}

#custom-player-next.active:hover {{
  background-color: {pal["surface_container_high"]};
  color: {pal["primary"]};
}}

#mode {{
  border-radius: 16px;
  margin: 10px 4px;
  padding: 4px 10px;
  color: {pal["on_surface"]};
  background-color: {pal["surface_container"]};
  border: 1px solid {pal["outline_variant"]};
}}

/* ==========================================================
   RIGHT MODULE CLUSTER (Clean Material 3 Container)
   group/quicklinks: network#name -> network -> pulseaudio
   -> custom-brightness -> backlight -> custom-battery-time
   -> power-profiles-daemon -> battery
   ========================================================== */
#quicklinks {{
  background-color: {pal["surface_container"]};
  border: 1px solid {pal["outline_variant"]};
  border-radius: 18px;
  margin: 10px 10px 10px 4px;
  padding: 4px 8px;
}}

#quicklinks * {{
  background: transparent;
  border: none;
  margin: 0;
  padding: 0;
  color: {pal["on_surface"]};
  font-weight: 500;
}}

#quicklinks #network.name {{
  padding-left: 8px;
  padding-right: 5px;
}}

#quicklinks #network:not(.name) {{
  padding-left: 6px;
  padding-right: 9px;
}}

#quicklinks #network.disconnected,
#quicklinks #network.ethernet {{
  padding-left: 8px;
  padding-right: 9px;
}}

#quicklinks #pulseaudio {{
  padding-left: 9px;
  padding-right: 9px;
}}

#quicklinks #custom-brightness {{
  padding: 0 7px;
}}

#quicklinks #custom-brightness.empty {{
  padding: 0;
  margin: 0;
}}

#quicklinks #backlight {{
  padding-left: 7px;
  padding-right: 7px;
}}

#quicklinks #custom-power-profile {{
  padding-left: 9px;
  padding-right: 9px;
  font-weight: 500;
}}

#quicklinks #battery {{
  padding-left: 9px;
  padding-right: 8px;
}}

#quicklinks #custom-power-profile.performance {{
  color: {pal["peach"]};
}}

#quicklinks #custom-power-profile.balanced {{
  color: {pal["teal"]};
}}

#quicklinks #custom-power-profile.power-saver {{
  color: {pal["green"]};
}}

#quicklinks #battery.charging,
#quicklinks #battery.plugged {{
  color: {pal["green"]};
}}

#tray {{
  margin: 10px 10px 10px 4px;
  padding: 2px 10px;
  border-radius: 16px;
  background-color: {pal["surface_container"]};
  border: 1px solid {pal["outline_variant"]};
}}

/* Status States for Connected Modules */
#custom-battery-time.charging,
#custom-powerbank.charging {{
  color: {pal["green"]};
}}

#custom-powerbank.idle {{
  color: {pal["on_surface_variant"]};
}}

/* Power Profiles Daemon */
#power-profiles-daemon.performance {{
  color: {pal["peach"]};
}}

#power-profiles-daemon.balanced {{
  color: {pal["teal"]};
}}

#power-profiles-daemon.power-saver {{
  color: {pal["green"]};
}}

/* Tooltips */
tooltip {{
  border-radius: 12px;
  padding: 6px 10px;
  background-color: {pal["surface_container_high"]};
  border: 1px solid {pal["outline_variant"]};
}}

tooltip decoration {{
  border-radius: 12px;
}}

tooltip label {{
  padding: 2px 4px;
  background-color: transparent;
  color: {pal["on_surface"]};
}}
"""
    style_css.write_text(content)


def restart_waybars():
    # Safely terminate all existing waybar instances
    subprocess.run(["pkill", "-x", "waybar"], stderr=subprocess.DEVNULL)
    time.sleep(0.3)

    # Launch main waybar
    subprocess.Popen(["waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(0.2)

    # Launch memento-mori desktop widget
    launch_script = WAYBAR_DIR / "scripts" / "launch-memento.sh"
    if launch_script.is_file():
        subprocess.Popen([str(launch_script), "--once"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    else:
        subprocess.Popen(
            ["waybar", "-c", str(WAYBAR_DIR / "memento-mori.json"), "-s", str(WAYBAR_DIR / "memento-mori.css")],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )


def update_memento_mori(pal):
    memento_css = WAYBAR_DIR / "memento-mori.css"

    content = f"""* {{
  border: none;
  border-radius: 0;
  min-height: 0;
  font-family: "JetBrainsMono Nerd Font", monospace;
}}

window#waybar {{
  background-color: transparent;
  border: none;
  box-shadow: none;
}}

#custom-memento-mori {{
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border: 1px solid {pal["outline_variant"]};
  border-radius: 28px;
  padding: 14px 32px;
  box-shadow: none;
  font-size: 13px;
  letter-spacing: 0.5px;
}}
"""
    memento_css.write_text(content)
