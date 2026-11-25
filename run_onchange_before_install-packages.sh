#!/usr/bin/env bash
set -euo pipefail

# Install missing Arch packages, Python dependencies, and Charmbracelet Crush
# before chezmoi applies dotfiles.

ARCH_PACKAGES=(
  # Window manager & Wayland core
  sway
  swaybg
  swaylock
  swaync
  waybar
  wofi
  xorg-xwayland
  xorg-xrdb
  xdg-desktop-portal
  xdg-desktop-portal-wlr
  lxqt-policykit

  # Terminal, editor, browser & file manager
  kitty
  fish
  neovim
  firefox
  thunar
  btop

  # Screenshots, clipboard, audio, power & networking
  grim
  slurp
  jq
  wl-clipboard
  wf-recorder
  hyprpicker
  brightnessctl
  pamixer
  playerctl
  libpulse
  networkmanager
  networkmanager-dmenu
  bluez
  bluez-utils

  # Media, fonts & toolchains
  mpd
  ncmpcpp
  ttf-jetbrains-mono-nerd
  python
  python-pip
  python-pillow
  go

  # Local AI stack
  ollama-vulkan
)

AUR_PACKAGES=(
  woomer-sway
)

if command -v pacman >/dev/null 2>&1; then
  missing_arch=()
  for pkg in "${ARCH_PACKAGES[@]}"; do
    if ! pacman -Qq "$pkg" >/dev/null 2>&1; then
      missing_arch+=("$pkg")
    fi
  done

  if [ "${#missing_arch[@]}" -gt 0 ]; then
    echo "Installing missing Arch packages: ${missing_arch[*]}"
    sudo pacman -S --needed --noconfirm "${missing_arch[@]}"
  fi

  aur_helper=""
  if command -v yay >/dev/null 2>&1; then
    aur_helper="yay"
  elif command -v paru >/dev/null 2>&1; then
    aur_helper="paru"
  fi

  if [ -n "$aur_helper" ]; then
    missing_aur=()
    for pkg in "${AUR_PACKAGES[@]}"; do
      if ! pacman -Qq "$pkg" >/dev/null 2>&1; then
        missing_aur+=("$pkg")
      fi
    done
    if [ "${#missing_aur[@]}" -gt 0 ]; then
      echo "Installing missing AUR packages via $aur_helper: ${missing_aur[*]}"
      "$aur_helper" -S --needed --noconfirm "${missing_aur[@]}"
    fi
  fi
fi

# Ensure Material You Python dependency is installed
if command -v python3 >/dev/null 2>&1 && ! python3 -c "import materialyoucolor" >/dev/null 2>&1; then
  echo "Installing materialyoucolor Python package..."
  pip install --user --break-system-packages materialyoucolor
fi

# Install Charmbracelet Crush if missing
if ! command -v crush >/dev/null 2>&1; then
  if command -v go >/dev/null 2>&1; then
    echo "Installing charmbracelet/crush via go install..."
    go install github.com/charmbracelet/crush@latest
    mkdir -p "$HOME/.local/bin"
    ln -sf "$(go env GOPATH)/bin/crush" "$HOME/.local/bin/crush"
  else
    echo "Warning: 'go' is not installed; skipping charmbracelet/crush installation." >&2
  fi
fi
