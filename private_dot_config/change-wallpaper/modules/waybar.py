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
   LEFT MODULE CLUSTER (Connected Material 3 Pill)
   cpu -> temperature -> memory -> custom-spacing-left
   ========================================================== */
#cpu {{
  margin: 10px 0 10px 10px;
  padding: 4px 10px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-radius: 20px 0 0 20px;
  border: 1px solid {pal["outline_variant"]};
  border-right: none;
  font-weight: 500;
}}

#temperature {{
  margin: 10px 0;
  padding: 4px 10px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#memory {{
  margin: 10px 0;
  padding: 4px 10px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#custom-spacing-left {{
  margin: 10px 10px 10px 0;
  padding: 4px 6px;
  background-color: {pal["surface_container"]};
  color: {pal["outline"]};
  border-radius: 0 20px 20px 0;
  border: 1px solid {pal["outline_variant"]};
  border-left: none;
  font-size: 14px;
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
  padding: 4px 14px;
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
  padding: 4px 14px;
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
   RIGHT MODULE CLUSTER (Connected Material 3 Ribbon)
   custom-spacing-right -> network -> pulseaudio
   -> custom-brightness -> backlight -> custom-fan
   -> custom-powerbank -> battery
   ========================================================== */
#custom-spacing-right {{
  margin: 10px 0 10px 10px;
  padding: 4px 6px;
  background-color: {pal["surface_container"]};
  color: {pal["outline"]};
  border-radius: 20px 0 0 20px;
  border: 1px solid {pal["outline_variant"]};
  border-right: none;
  font-size: 14px;
}}

#network {{
  margin: 10px 0;
  padding: 4px 7px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#pulseaudio {{
  margin: 10px 0;
  padding: 4px 7px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#custom-brightness,
#backlight {{
  margin: 10px 0;
  padding: 4px 7px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#custom-fan {{
  margin: 10px 0;
  padding: 4px 7px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

#custom-powerbank {{
  margin: 10px 0;
  padding: 4px 7px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-top: 1px solid {pal["outline_variant"]};
  border-bottom: 1px solid {pal["outline_variant"]};
  border-left: none;
  border-right: none;
  font-weight: 500;
}}

/* Only battery changes color to green when charging, otherwise default on_surface color */
#battery {{
  margin: 10px 10px 10px 0;
  padding: 4px 12px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border-radius: 0 20px 20px 0;
  border: 1px solid {pal["outline_variant"]};
  border-left: none;
  font-weight: 500;
}}

#battery.good,
#battery.warning,
#battery.critical,
#battery.critical:not(.charging),
#battery.urgent {{
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  animation: none;
}}

#battery.charging,
#battery.plugged,
#custom-powerbank.charging {{
  background-color: {pal["surface_container"]};
  color: {pal["green"]};
  animation: none;
}}

#tray {{
  margin: 10px 10px 10px 4px;
  padding: 2px 10px;
  border-radius: 16px;
  background-color: {pal["surface_container"]};
  border: 1px solid {pal["outline_variant"]};
}}

/* Status States for Connected Modules */
#custom-powerbank.charging {{
  color: {pal["green"]};
}}

#custom-powerbank.idle {{
  color: {pal["on_surface_variant"]};
}}

/* Tooltips */
tooltip {{
  border-radius: 12px;
  padding: 12px;
  background-color: {pal["surface_container_high"]};
  border: 1px solid {pal["outline_variant"]};
}}

tooltip label {{
  padding: 4px;
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
    birth = datetime.datetime(2007, 4, 21, 4, 0, 0)
    target = datetime.datetime(2087, 4, 21, 4, 0, 0)
    now = datetime.datetime.now()
    total_span = (target - birth).total_seconds()
    lived_span = max(0, (now - birth).total_seconds())
    pct = round(min(100.0, max(0.0, (lived_span / total_span) * 100)), 1)

    r_pri = int(pal["primary"][1:3], 16)
    g_pri = int(pal["primary"][3:5], 16)
    b_pri = int(pal["primary"][5:7], 16)

    r_bg = int(pal["surface_container"][1:3], 16)
    g_bg = int(pal["surface_container"][3:5], 16)
    b_bg = int(pal["surface_container"][5:7], 16)

    # 100% opaque blend so bright/white wallpapers cannot bleed through
    r_blend = int(0.68 * r_bg + 0.32 * r_pri)
    g_blend = int(0.68 * g_bg + 0.32 * g_pri)
    b_blend = int(0.68 * b_bg + 0.32 * b_pri)
    blend_hex = f"#{r_blend:02x}{g_blend:02x}{b_blend:02x}"

    start_blur = max(0.0, pct - 6.0)
    end_blur = min(100.0, pct + 8.0)

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
  background: linear-gradient(to left, 
    {blend_hex} 0%, 
    {blend_hex} {start_blur}%, 
    {pal["surface_container"]} {end_blur}%, 
    {pal["surface_container"]} 100%
  );
  color: {pal["on_surface"]};
  border: 1.5px solid {pal["outline"]};
  border-radius: 28px;
  padding: 16px 32px;
  box-shadow: none;
  font-size: 13px;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.95);
}}
"""
    memento_css.write_text(content)
