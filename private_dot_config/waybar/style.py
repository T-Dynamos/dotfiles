from pathlib import Path
from catppuccin import PALETTE

# -------------------------
# Pick flavour
# -------------------------
c = PALETTE.frappe.colors
c = PALETTE.mocha.colors
# c = PALETTE.macchiato.colors
# -------------------------
# Color mapping (important)
# -------------------------
COL = {
    "bg_main": c.base.hex,
    "bg_alt": c.mantle.hex,
    "bg_dark": c.crust.hex,
    "text": c.text.hex,
    "text_dark": c.crust.hex,
    "text_muted": c.overlay1.hex,
    "lavender": c.lavender.hex,
    "rosewater": c.rosewater.hex,
    "peach": c.peach.hex,
    "yellow": c.yellow.hex,
    "teal": c.teal.hex,
    "red": c.red.hex,
    "green": c.green.hex,
    "mauve": c.mauve.hex,
}

# -------------------------
# Full CSS
# -------------------------
css = f"""
* {{
  border: none;
  border-radius: 0;
  min-height: 0;
  font-family: Material Design Icons, JetBrainsMono Nerd Font;
  font-size: 13px;
}}

window#waybar {{
  background-color: {COL["bg_main"]};
  transition-property: background-color;
  transition-duration: 0.5s;
}}

window#waybar.hidden {{
  opacity: 0.5;
}}

#workspaces {{
  background-color: transparent;
}}

#workspaces button {{
  all: initial;
  min-width: 0;
  padding: 6px 18px;
  margin: 10px 2px;
  border-radius: 21px;
  background-color: {COL["bg_alt"]};
  color: {COL["text"]};
}}

#workspaces button.visible {{
  color: {COL["text_dark"]};
  background-color: {COL["lavender"]};
}}

#workspaces button:hover {{
  color: {COL["text_dark"]};
  background-color: {COL["rosewater"]};
}}

#workspaces button.urgent {{
  background-color: {COL["red"]};
}}

#custom-spacing-left {{
  margin: 12px 12px 12px 0;
  font-size: 20px;
  background-color: {COL["peach"]};
  border-radius: 0 21px 21px 0;
}}

#custom-spacing-right {{
  margin: 12px 0px 12px 12px;
  font-size: 20px;
  background-color: {COL["peach"]};
  border-radius: 21px 0 0 21px;
}}

#cpu,
#temperature,
#network,
#mpris,
#backlight,
#custom-brightness,
#custom-power,
#pulseaudio,
#battery,
#mode,
#custom-fan,
#memory {{
  margin: 12px 0;
  padding: 0 10px;
  color: {COL["bg_main"]};
}}

#memory {{
  background-color: {COL["peach"]};
}}

#temperature {{
  background-color: {COL["lavender"]};
}}

#cpu {{
  background-color: {COL["rosewater"]};
}}

#network {{
  padding: 0 13px 0px 10px;
  background-color: {COL["yellow"]};
}}

#custom-fan {{
  background-color: {COL["lavender"]};
}}

#mode {{
  border-radius: 21px;
}}

#clock {{
  margin: 12px;
  padding: 0 10px;
  color: {COL["bg_main"]};
  border-radius: 21px;
  background-color: {COL["mauve"]};
}}

#backlight {{
  background-color: {COL["rosewater"]};
}}


#custom-brightness {{
  background-color: {COL["rosewater"]};
}}


#pulseaudio {{
  background-color: {COL["teal"]};
}}

#mpris {{
  background-color: {COL["peach"]};
}}

#mode {{
  color: {COL["text_muted"]};
  background-color: {COL["bg_alt"]};
}}

#battery {{
  background-color: {COL["red"]};
}}

@keyframes blink {{
  to {{
    background-color: {COL["red"]};
    color: {COL["bg_dark"]};
  }}
}}

#battery.warning,
#battery.critical,
#battery.urgent {{
  background-color: {COL["red"]};
  color: {COL["bg_dark"]};
  animation-name: blink;
  animation-duration: 0.5s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  animation-direction: alternate;
}}

#battery.charging {{
  background-color: {COL["green"]};
}}

tooltip {{
  border-radius: 8px;
  padding: 15px;
  background-color: {COL["bg_alt"]};
}}

tooltip label {{
  padding: 5px;
  background-color: {COL["bg_alt"]};
}}
"""

# -------------------------
# Write file
# -------------------------
Path("style.css").write_text(css)
