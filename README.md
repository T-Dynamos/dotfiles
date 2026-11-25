# T-Dynamos Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/), featuring an integrated **Material You (Material Design 3)** dynamic theming system powered by [`materialyoucolor`](https://github.com/T-Dynamos/materialyoucolor-python).

All components—**Sway**, **Waybar**, **Kitty**, **Wofi**, **Swaylock**, **SwayNC**, **Thunar (GTK)**, **Firefox**, **Chromium**, **btop**, **ncmpcpp**, and **CAVA**—synchronize their color palettes dynamically from your active wallpaper.

---

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/0102785b-2c19-455e-b36b-35ba9653e34b" />


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

### Status Bar: Waybar & Desktop Widgets
- **Authentic Material 3 aesthetic**: Calm tonal surfaces (`surface_container`) with subtle borders (`outline_variant`) and harmonized secondary color roles (`peach` for CPU, `yellow` for temp/brightness, `purple` for RAM, `teal` for network, `secondary` for audio, `green` for power).
- **Interactive MPRIS Media Capsule**: Center-positioned media controller with dedicated clickable Previous (`󰒮`), Play/Pause (`󰐊`/`󰏤`), and Next (`󰒭`) buttons seamlessly connected into a single pill, auto-hidden when stopped.
- **Desktop Memento Mori Countdown Widget**: Centered ambient desktop widget (`layer: "bottom"`, `exclusive: false`) displaying remaining lifespan in weeks, days, and hours based on birth date (21 April 2007, 04:00 AM) and an 80-year horizon.
- **Connected Pill Capsules**:
  - **Left Cluster**: `cpu` → `temperature` → `memory` → `custom-spacing-left` connected seamlessly into one capsule with smooth rounded ends.
  - **Right Cluster**: `custom-spacing-right` → `network` → `pulseaudio` → `brightness` → `fan` → `powerbank` → `battery` connected into one capsule.
  - **Center**: MPRIS player capsule and elevated clock pill.
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

### Browsers: Firefox & Chromium
- **Firefox**: Custom `userChrome.css` and `userContent.css` matching the active Material You dark theme across navigation toolbar, pill URL bar, context menus, and custom home page (`about:home` / `about:newtab`).
- **Chromium**: Native Wayland execution via `chromium-flags.conf` with PipeWire WebRTC screen sharing, touch gesture navigation, and dynamic Material 3 theme extension (`~/.config/chromium-material-theme/`) with matching wallpaper NTP background.
- Colors auto-regenerated upon wallpaper change.

### System Monitor: btop
- Dedicated dynamic theme file (`~/.config/btop/themes/material-you.theme`) generated from active wallpaper.
- Harmonized graph gradients (CPU, temperature, memory free/cached/used, network up/down) and tonal box outlines matching the system palette.

### Music Player: ncmpcpp
- Complete Material You color synchronization across main playlist, visualizer, catalog, and album art views (`config`, `config-art`, `catalog.conf`, `visualizer.conf`).
- Dynamic visualizer gradient spectrum mapped to vibrant tonal accents with full-screen mode and Material 3 slider styling.

### Audio Visualizer: CAVA
- Dynamic 8-stop vertical gradient (`~/.config/cava/themes/material-you` and `~/.config/cava/config`) generated from active wallpaper palette.
- High-performance 60 FPS PipeWire audio capture with Monstercat wave smoothing.
- Real-time theme reloading (`live-config = 1`).

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

Applying with Chezmoi automatically runs `run_onchange_before_install-packages.sh` to install any missing Arch packages (including `sway`, `waybar`, `kitty`, `fish`, `ollama-vulkan`, `go`, etc.), `materialyoucolor`, and `charmbracelet/crush`.

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
| `Super + Shift + Backspace` | Open **Chromium** Browser |
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

## Local AI Coding Stack (`Ollama` + `Crush`)

Local LLM coding setup powered by **`ollama-vulkan`** (AMD Radeon 780M RADV Vulkan) and [**Charmbracelet Crush**](https://github.com/charmbracelet/crush).

### Configured Files
* **Crush Config:** `~/.config/crush/crushrc` (`private_dot_config/crush/crushrc`)
  * Connects to `http://localhost:11434/v1/` with `--discover-models true`.
  * Currently configures `ollama/qwen3.6:35b` (`131072` / `128K` context, `--thinking toggleable`, `--supports-images true`, `--think` enabled on `model large`).
  * Grants full built-in tool auto-approval (`permissions allow ...`) and unblocks default bash restrictions (`permissions unblock ...`).
* **Ollama Environment:** `~/.config/fish/conf.d/ollama.fish` & `~/.config/environment.d/20-ollama.conf`
  * `OLLAMA_IGPU_ENABLE=1` — prevents Ollama from dropping integrated GPUs (`Radeon 780M`).
  * `OLLAMA_FLASH_ATTENTION=1` & `OLLAMA_KV_CACHE_TYPE=q8_0` — halves KV-cache RAM usage.
  * `OLLAMA_CONTEXT_LENGTH=131072` — sets server context length to `128K` (must stay aligned with `crushrc`).

### Changing Models
1. Pull or remove models in Ollama:
   ```bash
   ollama pull qwen3.5:9b      # example: fast 100%-GPU model
   ollama rm qwen3.6:35b       # remove unused model files
   ollama list
   ```
2. Update `model add`, `model large`, and `model small` in `~/.local/share/chezmoi/private_dot_config/crush/crushrc`:
   ```bash
   model add ollama/<model-tag> \
     --name "Display Name" \
     --context-window 131072 \
     --default-max-tokens 16384 \
     --thinking toggleable \
     --supports-images true

   model large ollama/<model-tag> --think
   model small ollama/<model-tag>
   ```
3. Apply & clear cached discovery list if you removed models:
   ```bash
   chezmoi apply ~/.config/crush/crushrc
   rm -f ~/.local/share/crush/discovered_models/ollama.json
   ```

### Changing the Context Window
Always keep **both** Ollama (`OLLAMA_CONTEXT_LENGTH`) and Crush (`--context-window`) at the same value so Crush auto-compacts (~80% full) before Ollama truncates early turns:
1. Edit `OLLAMA_CONTEXT_LENGTH` in:
   * `~/.local/share/chezmoi/private_dot_config/private_fish/conf.d/ollama.fish`
   * `~/.local/share/chezmoi/private_dot_config/environment.d/20-ollama.conf`
2. Edit `--context-window` to match in `~/.local/share/chezmoi/private_dot_config/crush/crushrc`.
3. Apply and restart `ollama serve` (open a fresh Fish shell so new env vars are loaded):
   ```bash
   chezmoi apply ~/.config/crush/crushrc ~/.config/fish/conf.d/ollama.fish ~/.config/environment.d/20-ollama.conf
   systemctl --user set-environment OLLAMA_CONTEXT_LENGTH=131072   # match new value
   pkill ollama; ollama serve
   ```
   *(Verify with `ollama ps` while a model is loaded that `CONTEXT` and `PROCESSOR` match expectations.)*

### Useful Crush Commands & Shortcuts
* **Run Crush:** `crush` *(or `crush -yy` for sysadmin mode across future MCP tools too)*
* **Switch model:** `Ctrl+M` inside TUI
* **Toggle thinking:** `Ctrl+P` → `Enable/Disable Thinking Mode`
* **Expand/collapse thinking blocks:** Click the thinking header, or press `Tab` (focus chat) → `Space`
* **Delete all sessions in current project:**
  ```bash
  crush session list --json | jq -r '.[].id' | xargs -r -n1 crush session delete
  # or wipe the project's local Crush state completely:
  rm -rf .crush
  ```

### Syncing Changes to Chezmoi & GitHub
After editing any file under `~/.local/share/chezmoi/`:
```bash
chezmoi apply
git -C ~/.local/share/chezmoi add -A
git -C ~/.local/share/chezmoi commit -m "chore: update crush/ollama config"
git -C ~/.local/share/chezmoi push origin master
```

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
├── btop/
│   ├── btop.conf            # Dynamic system monitor configuration
│   └── themes/
│       └── material-you.theme # Generated Material You btop theme
├── ncmpcpp/
│   ├── config               # Dynamic MPD client theme & styling
│   ├── config-art           # Album art layout configuration
│   ├── catalog.conf
│   └── visualizer.conf
├── cava/
│   ├── config               # PipeWire 60 FPS visualizer configuration
│   └── themes/
│       └── material-you     # Generated 8-stop Material You spectral theme
├── chromium-flags.conf      # Wayland & theme launch flags
├── chromium-material-theme/ # Dynamic Material You extension
├── crush/
│   └── crushrc              # Crush AI agent config (Ollama + full permissions)
├── environment.d/
│   ├── 10-wayland.conf      # Native Wayland toolkit environment variables
│   └── 20-ollama.conf       # Ollama Vulkan iGPU + 128K context environment
├── fish/
│   └── conf.d/
│       └── ollama.fish      # Fish exports for Ollama Vulkan & context
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
