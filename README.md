# T-Dynamos Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/), featuring an integrated **Material You (Material Design 3)** dynamic theming system powered by [`materialyoucolor`](https://github.com/T-Dynamos/materialyoucolor-python).

All components—**Sway**, **Waybar**, **Kitty**, **Wofi**, **Swaylock**, **SwayNC**, **Thunar (GTK)**, and **Firefox**—synchronize their color palettes dynamically from your active wallpaper.

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
- **Interactive Network Manager**: Click or right-click the Wi-Fi icon to launch `networkmanager_dmenu` for scanning and connecting to networks in a Material 3 popover.

### Terminal: Kitty
- Automatically includes `colors.conf` generated from the wallpaper.
- Deep dark `surface` background (`#180B01` / `#0A0D1B`), high-contrast `on_surface` text, primary accent cursor and active tabs, plus 16 harmonized ANSI terminal colors.
- Hot-reloads live on wallpaper change via `SIGUSR1`.

### App Launcher: Wofi
- Clean, centered Material 3 search card with rounded corners (`20px`), floating pill input, and primary selection highlights.
- Completely transparent window backdrop eliminating compositor corner clipping artifacts.
- Press **Windows key (`Super`)** or **`Mod4+d`** to toggle.

### Screen Locker: Swaylock
- Dynamic Material 3 lock screen matching the active wallpaper (`~/.config/swaylock/config`).
- Features a semi-transparent surface ring with primary accent keypress feedback, error backspace indicators, and wallpaper scaling.
- Lock instantly with **`Super + l`**.

### Notification Center: SwayNC
- Dynamic Material 3 Notification Center and OSD widget styling (`~/.config/swaync/style.css`).
- Floating notification cards, pill action buttons, and control center sliders harmonized to wallpaper palette.
- Hot-reloads live via `swaync-client -R -rs`.
- Toggle control center with **`Super + Shift + n`**.

### File Manager & GTK: Thunar
- Full Material 3 dark styling across GTK 3 & GTK 4 apps (`~/.config/gtk-3.0/` and `~/.config/gtk-4.0/`).
- Seamless Thunar custom styling: tonal sidebar pane, rounded pill search and pathbar chips, and refined popover menus.

### Browser: Firefox
- Custom `userChrome.css` and `userContent.css` matching the active Material You dark theme across navigation toolbar, pill URL bar, floating pill tabs rounded on all sides, context menus, and new tab page.
- Colors auto-regenerated in `chrome/colors.css` upon wallpaper change.

---

## Installation & Setup

### 1. Install All Dependencies (Single Command)

Run this single command on Arch Linux to install all necessary system packages, Sway environment dependencies, and Python libraries:

```bash
sudo pacman -S --needed --noconfirm chezmoi sway swaybg swaylock swaync waybar kitty wofi thunar firefox grim slurp jq wl-clipboard wf-recorder hyprpicker brightnessctl pamixer playerctl libpulse networkmanager networkmanager-dmenu bluez bluez-utils lxqt-policykit xdg-desktop-portal xdg-desktop-portal-wlr python python-pip ttf-jetbrains-mono-nerd && pip install --break-system-packages materialyoucolor pillow
```

*Optional AUR packages:*
```bash
yay -S woomer-sway   # Screen magnifier bound to Super + Shift + x
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
| `Super + l` | Lock Screen with **Swaylock** |
| `Super + c` | Close focused window |
| `Super + f` | Toggle Fullscreen |
| `Super + Space` | Toggle Floating window |
| `Super + Shift + n` | Toggle **SwayNC** Notification Center |
| `Super + Shift + p` | Pick color on screen (**Hyprpicker**) |
| `Super + 1-9` | Switch to Workspace 1-9 |
| `Super + Shift + 1-9` | Move container to Workspace 1-9 |
| `Super + Shift + s` | Screenshot menu (`screen` / `window` / `region`) |
| `Super + Shift + r` | Screen recording with audio |
| `Super + Shift + x` | Screen magnifier (**Woomer**) |
| `Super + Shift + c` | Reload Sway configuration |
| `Super + Shift + e` | Exit Sway session |

---

## Tracked Configurations

```
~/.config/
├── sway/
│   ├── config
│   ├── screenshot           # Grim + Slurp screenshot handler
│   └── theme                # Dynamic Material 3 border colors
├── swaylock/
│   └── config               # Dynamic Material 3 lockscreen
├── swaync/
│   ├── config.json
│   └── style.css            # Dynamic Notification Center theme
├── waybar/
│   ├── config
│   ├── style.py             # Material You stylesheet generator
│   ├── style.css            # Dynamic Waybar stylesheet
│   └── scripts/
│       └── powerbank.py     # 3S PowerBank telemetry monitor
├── gtk-3.0/
│   ├── gtk.css              # Dynamic Thunar & GTK3 theming
│   └── colors.css
├── gtk-4.0/
│   ├── gtk.css              # Dynamic GTK4 theming
│   └── colors.css
├── kitty/
│   ├── kitty.conf
│   └── colors.conf          # Dynamic terminal colors
├── wofi/
│   ├── config
│   └── style.css            # Dynamic launcher styling
├── pip/
│   └── pip.conf             # Global Python package settings
└── wallpaper                # Active wallpaper image

~/.local/bin/
├── change-wallpaper         # Theme sync script
└── set-wallpaper -> change-wallpaper
```

---

## License
MIT © [T-Dynamos](https://github.com/T-Dynamos)
