#!/usr/bin/env python3
"""
Waybar Material You dynamic theme generator.
Extracts Material 3 colors from active wallpaper using materialyoucolor.
Follows clean Material Design 3 tonal hierarchy with connected pill clusters.
"""

from pathlib import Path
import os
import subprocess

from materialyoucolor.quantize import ImageQuantizeCelebi
from materialyoucolor.score.score import Score
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.blend.blend import Blend
from materialyoucolor.utils.color_utils import hex_from_argb

WALLPAPER_PATH = Path.home() / ".config" / "wallpaper"
STYLE_CSS_PATH = Path.home() / ".config" / "waybar" / "style.css"


def generate_palette(image_path=WALLPAPER_PATH, is_dark=True):
    seed = None
    if Path(image_path).exists():
        try:
            colors = ImageQuantizeCelebi(str(image_path), 5, 128)
            ranked = Score.score(colors)
            if ranked:
                seed = ranked[0]
        except Exception as e:
            print(f"Warning: Failed to extract colors from {image_path}: {e}")

    # Fallback to default Material seed color if extraction fails or file missing
    if seed is None:
        seed = 0xFF6750A4

    scheme = SchemeExpressive(Hct.from_int(seed), is_dark, 0.0)
    mdc = MaterialDynamicColors()

    def get_c(name):
        return getattr(mdc, name).get_hex(scheme)[:7]

    def harm_tone(color_int, tone):
        h = Hct.from_int(Blend.harmonize(color_int, seed))
        h.tone = tone
        return hex_from_argb(h.to_int())[:7]

    return {
        "surface": get_c("surface"),
        "surface_container": get_c("surfaceContainer"),
        "surface_container_high": get_c("surfaceContainerHigh"),
        "surface_container_lowest": get_c("surfaceContainerLowest"),
        "on_surface": get_c("onSurface"),
        "on_surface_variant": get_c("onSurfaceVariant"),
        "outline": get_c("outline"),
        "outline_variant": get_c("outlineVariant"),
        "primary": get_c("primary"),
        "on_primary": get_c("onPrimary"),
        "primary_container": get_c("primaryContainer"),
        "on_primary_container": get_c("onPrimaryContainer"),
        "secondary": get_c("secondary"),
        "on_secondary": get_c("onSecondary"),
        "secondary_container": get_c("secondaryContainer"),
        "on_secondary_container": get_c("onSecondaryContainer"),
        "tertiary": get_c("tertiary"),
        "on_tertiary": get_c("onTertiary"),
        "tertiary_container": get_c("tertiaryContainer"),
        "on_tertiary_container": get_c("onTertiaryContainer"),
        "error": get_c("error"),
        "on_error": get_c("onError"),
        "error_container": get_c("errorContainer"),
        "on_error_container": get_c("onErrorContainer"),
        "green": harm_tone(0xFF4CAF50, 80),
        "green_dark": harm_tone(0xFF4CAF50, 20),
        "yellow": harm_tone(0xFFFFEB3B, 80),
        "yellow_dark": harm_tone(0xFFFFEB3B, 20),
        "teal": harm_tone(0xFF00BCD4, 80),
        "teal_dark": harm_tone(0xFF00BCD4, 20),
        "purple": harm_tone(0xFFAB47BC, 80),
        "purple_dark": harm_tone(0xFFAB47BC, 20),
        "peach": harm_tone(0xFFFF8A65, 80),
        "peach_dark": harm_tone(0xFFFF8A65, 20),
    }


def generate_waybar_css(pal):
    return f"""* {{
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

#workspaces button.visible {{
  color: {pal["surface"]};
  background-color: {pal["primary"]};
  border-color: {pal["primary"]};
  font-weight: bold;
}}

#workspaces button:hover {{
  color: {pal["on_surface"]};
  background-color: {pal["surface_container_high"]};
}}

#workspaces button.urgent {{
  color: {pal["on_error"]};
  background-color: {pal["error"]};
  border-color: {pal["error"]};
}}

/* ==========================================================
   CENTER (Clock, Mode & MPRIS)
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

#mpris {{
  margin: 10px 4px;
  padding: 4px 12px;
  border-radius: 18px;
  background-color: {pal["surface_container"]};
  color: {pal["on_surface"]};
  border: 1px solid {pal["outline_variant"]};
  font-weight: 500;
  transition: all 0.2s ease;
}}

#mpris.playing {{
  color: {pal["primary"]};
  border-color: {pal["primary"]};
  background-color: {pal["surface_container_high"]};
}}

#mpris.paused {{
  color: {pal["on_surface_variant"]};
  border-color: {pal["outline_variant"]};
}}

#mode {{
  border-radius: 16px;
  margin: 10px 4px;
  padding: 4px 10px;
  color: {pal["on_surface_variant"]};
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
  border-radius: 20px 0 0 20px;
  border: 1px solid {pal["outline_variant"]};
  border-right: none;
  font-size: 14px;
}}

#network,
#pulseaudio,
#custom-brightness,
#backlight,
#custom-fan,
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

#battery.charging {{
  color: {pal["green"]};
}}

@keyframes blink {{
  to {{
    background-color: {pal["error"]};
    color: {pal["on_error"]};
  }}
}}

#battery.warning,
#battery.critical,
#battery.urgent {{
  background-color: {pal["error"]};
  color: {pal["on_error"]};
  animation-name: blink;
  animation-duration: 0.5s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  animation-direction: alternate;
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


def main():
    pal = generate_palette(WALLPAPER_PATH, is_dark=True)
    css = generate_waybar_css(pal)
    STYLE_CSS_PATH.write_text(css)
    print(f"Waybar CSS written to {STYLE_CSS_PATH}")
    subprocess.run(["pkill", "-SIGUSR2", "waybar"], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
