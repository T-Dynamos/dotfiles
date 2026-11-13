"""
Chromium Browser Material You Dynamic Theme Updater
"""

import json
from PIL import Image
from config import CHROMIUM_DIR, CHROMIUM_THEME_DIR, CHROMIUM_FLAGS_FILE, WALLPAPER_TARGET
from palette import hex_to_rgb


def update_chromium(pal):
    CHROMIUM_THEME_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Prepare ntp background image from current wallpaper
    try:
        if WALLPAPER_TARGET.is_file():
            with Image.open(WALLPAPER_TARGET) as img:
                img_resized = img.resize((1366, 768), Image.Resampling.LANCZOS)
                img_resized.save(CHROMIUM_THEME_DIR / "ntp_background.png", "PNG")
    except Exception as e:
        print(f"  [Note] Chromium background resize: {e}")

    # 2. Build Material You theme manifest.json
    def c_rgb(name):
        return list(hex_to_rgb(pal[name]))

    manifest = {
        "manifest_version": 3,
        "name": "Material You Dynamic Theme",
        "version": "1.0",
        "description": "Dynamic Material Design 3 theme matching active wallpaper",
        "theme": {
            "images": {
                "theme_ntp_background": "ntp_background.png"
            },
            "colors": {
                "frame": c_rgb("surface"),
                "frame_inactive": c_rgb("surface"),
                "frame_incognito": c_rgb("surface"),
                "frame_incognito_inactive": c_rgb("surface"),
                "toolbar": c_rgb("surface_container"),
                "toolbar_text": c_rgb("on_surface"),
                "tab_text": c_rgb("primary"),
                "tab_background_text": c_rgb("on_surface_variant"),
                "bookmark_text": c_rgb("on_surface"),
                "ntp_background": c_rgb("surface"),
                "ntp_text": c_rgb("on_surface"),
                "ntp_link": c_rgb("primary"),
                "button_background": c_rgb("surface_container"),
                "omnibox_background": c_rgb("surface_container_high"),
                "omnibox_text": c_rgb("on_surface")
            },
            "properties": {
                "ntp_background_alignment": "center",
                "ntp_background_repeat": "no-repeat"
            }
        }
    }

    (CHROMIUM_THEME_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # 3. Ensure chromium-flags.conf exists with Wayland & theme loading
    flags_content = f"""# Chromium Flags for Wayland & Material You Theme
--ozone-platform-hint=auto
--enable-features=TouchpadOverscrollHistoryNavigation,WaylandWindowDecorations
--enable-webrtc-pipewire-capturer
--force-dark-mode
--password-store=basic
--load-extension={CHROMIUM_THEME_DIR}
"""
    CHROMIUM_FLAGS_FILE.write_text(flags_content, encoding="utf-8")

    # 4. Update Chromium profile Preferences if profile exists
    prefs_file = CHROMIUM_DIR / "Default" / "Preferences"
    if prefs_file.is_file():
        try:
            r, g, b = hex_to_rgb(pal["primary"])
            argb = (0xFF << 24) | (r << 16) | (g << 8) | b
            user_color_int = argb - 0x100000000 if argb >= 0x80000000 else argb

            data = json.loads(prefs_file.read_text(encoding="utf-8"))
            browser = data.setdefault("browser", {})
            theme = browser.setdefault("theme", {})
            theme["color_scheme"] = 2
            theme["color_scheme2"] = 2
            theme["user_color"] = user_color_int
            theme["user_color2"] = user_color_int
            theme["color_variant2"] = 1

            prefs_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"  [Note] Chromium Preferences update: {e}")
