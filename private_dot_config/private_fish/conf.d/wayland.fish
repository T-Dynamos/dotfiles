# Wayland Toolkit Environment Variables
# Ensures native Wayland backend for applications launched from fish shell

set -gx MOZ_ENABLE_WAYLAND 1
set -gx QT_QPA_PLATFORM "wayland;xcb"
set -gx QT_WAYLAND_DISABLE_WINDOWDECORATION 1
set -gx QT_SCALE_FACTOR_ROUNDING_POLICY PassThrough
set -gx QT_AUTO_SCREEN_SCALE_FACTOR 1
set -gx GDK_BACKEND "wayland,x11"
set -gx CLUTTER_BACKEND wayland
set -gx SDL_VIDEODRIVER wayland
set -gx ELECTRON_OZONE_PLATFORM_HINT auto
set -gx _JAVA_AWT_WM_NONREPARENTING 1
