# T-Dynamos Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/), featuring an integrated **Material You (Material Design 3)** dynamic theming system powered by [`materialyoucolor`](https://github.com/T-Dynamos/materialyoucolor-python).

All components—**Sway**, **Waybar**, **Kitty**, **Wofi**, and **Firefox**—synchronize their color palettes dynamically from your active wallpaper.

---

## Architecture & Features

### Material You Dynamic Theming Engine
- Powered by [`materialyoucolor`](https://github.com/T-Dynamos/materialyoucolor-python) (Material Design 3 Python implementation using C++ Celebi quantization).
- Extracts dominant colors from `~/.config/wallpaper` and generates a complete Material 3 Dark scheme.
- Harmonizes semantic colors (emerald green for charging, coral red for alerts, warm peach, yellow, cyan, and violet) using `Blend.harmonize`.
- Single command `change-wallpaper` updates and hot-reloads all apps simultaneously.

### Window Manager: Sway
- Minimal, fast Wayland tiling compositor.
- Dynamic window border colors (`client.focused`, `client.unfocused`, `client.urgent`) matching the wallpaper palette.
- App launcher bound to the **Windows key (`Super`)**.

### Status Bar: Waybar
- **Authentic Material 3 aesthetic**: Calm tonal surfaces (`surface_container`) with subtle borders (`outline_variant`), free from rainbow clutter.
- **Connected Pill Capsules**:
  - **Left Cluster**: `cpu` → `temperature` → `memory` → `custom-spacing-left` connected seamlessly into one capsule with smooth rounded ends.
  - **Right Cluster**: `custom-spacing-right` → `mpris` → `network` → `pulseaudio` → `brightness` → `fan` → `powerbank` → `battery` connected into one capsule.
  - **Center**: Independent active workspace pills (`primary` highlight) and elevated clock pill.
- **Dynamic Background Transparency**: When the active workspace has no windows, the Waybar background is completely `transparent` so your wallpaper shines through. When a window is focused, it smoothly transitions to a solid `surface` background for maximum readability.
- **3S PowerBank & Battery Telemetry**: Custom Bluetooth module reporting power draw (W) and energy used (Wh) with state-aware charging accents.

### Terminal: Kitty
- Automatically includes `colors.conf` generated from the wallpaper.
- Deep dark `surface` background (`#180B01` / `#0A0D1B`), high-contrast `on_surface` text, primary accent cursor and active tabs, plus 16 harmonized ANSI terminal colors.
- Hot-reloads live on wallpaper change via `SIGUSR1`.

### App Launcher: Wofi
- Clean, centered Material 3 search card with rounded corners (`20px`), pill search input, and primary selection highlights.
- Press **Windows key (`Super`)** or **`Mod4+d`** to toggle.

### Browser: Firefox
- Custom `userChrome.css` and `userContent.css` matching the active Material You dark theme across navigation toolbar, pill URL bar, tabs, context menus, and new tab page.
- Colors auto-regenerated in `chrome/colors.css` upon wallpaper change.

---

## Installation & Setup

### 1. Prerequisites (Arch Linux)
```bash
sudo pacman -S --needed chezmoi sway waybar kitty wofi swaybg brightnessctl pamixer
pip install materialyoucolor pillow
```

### 2. Apply with Chezmoi
```bash
chezmoi init --apply T-Dynamos
```

---

## Wallpaper & Theme Manager (`change-wallpaper`)

The included utility `change-wallpaper` (also available as `set-wallpaper`) handles full system synchronization.

### Usage

```bash
# 1. Change wallpaper and re-theme Sway, Waybar, Kitty, Wofi, and Firefox:
change-wallpaper ~/Pictures/wallpaper.png

# 2. Re-apply / refresh theme using current wallpaper (~/.config/wallpaper):
change-wallpaper

# 3. Use an alternate Material 3 scheme variant (tonal-spot, vibrant, fruit-salad, rainbow):
change-wallpaper --scheme tonal-spot

# 4. Background watcher mode (automatically re-themes when ~/.config/wallpaper is updated):
change-wallpaper --watch
```

---

## Keybindings (Sway)

| Keybinding | Action |
|---|---|
| `Super` (tap) / `Super + d` | Toggle **Wofi** App Launcher |
| `Super + Return` | Open **Kitty** Terminal |
| `Super + Backspace` | Open **Firefox** Browser |
| `Super + Escape` | Open **Thunar** File Manager |
| `Super + c` | Close focused window |
| `Super + f` | Toggle Fullscreen |
| `Super + Space` | Toggle Floating window |
| `Super + 1-9` | Switch to Workspace 1-9 |
| `Super + Shift + 1-9` | Move container to Workspace 1-9 |
| `Super + Shift + s` | Screenshot menu (`screen` / `window` / `region`) |
| `Super + Shift + r` | Screen recording with audio |
| `Super + Shift + c` | Reload Sway configuration |
| `Super + Shift + e` | Exit Sway session |

---

## Tracked Configurations

```
~/.config/
├── sway/
│   ├── config
│   └── theme                # Dynamic Material 3 border colors
├── waybar/
│   ├── config
│   ├── style.py             # Material You stylesheet generator
│   ├── style.css            # Dynamic Waybar stylesheet
│   └── scripts/
│       └── powerbank.py     # 3S PowerBank telemetry monitor
├── kitty/
│   ├── kitty.conf
│   └── colors.conf          # Dynamic terminal colors
├── wofi/
│   ├── config
│   └── style.css            # Dynamic launcher styling
└── wallpaper                # Active wallpaper image

~/.local/bin/
├── change-wallpaper         # Theme sync script
└── set-wallpaper -> change-wallpaper
```

---

## License
MIT © [T-Dynamos](https://github.com/T-Dynamos)
