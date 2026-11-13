"""
Firefox Browser Material You Theme & Live Reload Updater
"""

import json
import shutil
import socket
import subprocess
from pathlib import Path
from config import FIREFOX_PROFILES_DIR, HOME

MOZILLA_DIR = FIREFOX_PROFILES_DIR


def reload_firefox_live(pal):
    """
    Connect to Firefox via Marionette protocol (TCP 127.0.0.1:2828)
    and live-reload CSS variables across all active Firefox windows
    without requiring a browser restart.
    """
    vars_dict = {
        "--md-surface": pal["surface"],
        "--md-surface-container": pal["surface_container"],
        "--md-surface-container-high": pal["surface_container_high"],
        "--md-surface-container-lowest": pal["surface_container_lowest"],
        "--md-on-surface": pal["on_surface"],
        "--md-on-surface-variant": pal["on_surface_variant"],
        "--md-primary": pal["primary"],
        "--md-primary-container": pal["primary_container"],
        "--md-on-primary-container": pal["on_primary_container"],
        "--md-secondary": pal["secondary"],
        "--md-outline": pal["outline"],
        "--md-outline-variant": pal["outline_variant"],
        "--md-error": pal["error"],
        "--md-green": pal["green"],
    }

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        sock.connect(("127.0.0.1", 2828))

        def read_frame():
            len_buf = bytearray()
            while True:
                c = sock.recv(1)
                if not c or c == b":":
                    break
                len_buf.extend(c)
            if not len_buf:
                return None
            n = int(len_buf.decode("utf-8"))
            data = bytearray()
            while len(data) < n:
                chunk = sock.recv(n - len(data))
                if not chunk:
                    break
                data.extend(chunk)
            return json.loads(data.decode("utf-8"))

        def send_frame(msg_id, cmd, params):
            payload = json.dumps([0, msg_id, cmd, params])
            sock.sendall(f"{len(payload)}:{payload}".encode("utf-8"))
            return read_frame()

        # 1. Read greeting
        read_frame()

        # 2. Start session
        send_frame(1, "WebDriver:NewSession", {"capabilities": {}})

        # 3. Set chrome context
        send_frame(2, "Marionette:SetContext", {"value": "chrome"})

        # 4. Execute script to update all open chrome windows and load sheet
        css_rules = " ".join([f"{k}: {v} !important;" for k, v in vars_dict.items()])
        script = f"""
        const sss = Cc["@mozilla.org/content/style-sheet-service;1"].getService(Ci.nsIStyleSheetService);
        const ios = Cc["@mozilla.org/network/io-service;1"].getService(Ci.nsIIOService);
        const wm = Cc["@mozilla.org/appshell/window-mediator;1"].getService(Ci.nsIWindowMediator);

        const dataUri = ios.newURI("data:text/css,:root {{ {css_rules} }}");
        if (sss.sheetRegistered(dataUri, sss.USER_SHEET)) {{
            sss.unregisterSheet(dataUri, sss.USER_SHEET);
        }}
        sss.loadAndRegisterSheet(dataUri, sss.USER_SHEET);

        const fixCss = `
        #remote-control-box,
        #urlbar-remote-control-notification-anchor,
        .urlbar-icon[aria-label*="remote control"],
        .urlbar-icon[tooltiptext*="remote control"] {{
          display: none !important;
        }}
        #urlbar-background,
        .urlbar-background,
        #urlbar[remote-control] .urlbar-background,
        #urlbar[remote-control] #urlbar-background {{
          background-image: none !important;
        }}
        `;
        const fixUri = ios.newURI("data:text/css," + encodeURIComponent(fixCss));
        if (sss.sheetRegistered(fixUri, sss.USER_SHEET)) {{
            sss.unregisterSheet(fixUri, sss.USER_SHEET);
        }}
        sss.loadAndRegisterSheet(fixUri, sss.USER_SHEET);

        const vars = {json.dumps(vars_dict)};
        const enumerator = wm.getEnumerator("navigator:browser");
        let count = 0;
        while (enumerator.hasMoreElements()) {{
            const win = enumerator.getNext();
            if (win && win.document && win.document.documentElement) {{
                for (const [k, v] of Object.entries(vars)) {{
                    win.document.documentElement.style.setProperty(k, v, "important");
                }}
                const bgs = win.document.querySelectorAll(".urlbar-background");
                for (const b of bgs) {{
                    b.style.setProperty("background-image", "none", "important");
                }}
                const rcBox = win.document.getElementById("remote-control-box");
                if (rcBox) rcBox.style.setProperty("display", "none", "important");
                count++;
            }}
        }}
        return count;
        """
        send_frame(3, "WebDriver:ExecuteScript", {"script": script})
        try:
            send_frame(4, "WebDriver:DeleteSession", {})
        except Exception:
            pass
        sock.close()
        print("  Firefox theme live-reloaded successfully via Marionette!")
    except (ConnectionRefusedError, socket.timeout, OSError):
        pass
    except Exception as e:
        print(f"  [Note] Firefox live reload note: {e}")


def update_firefox(pal):
    if not MOZILLA_DIR.is_dir():
        # Try to initialize default profile if firefox is present
        try:
            subprocess.run(
                ["firefox", "--headless", "-CreateProfile", "default-release"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
        except Exception:
            pass

    if not MOZILLA_DIR.is_dir():
        return

    # Master CSS templates for new/existing profiles
    master_dir = HOME / ".config" / "firefox-material"
    user_chrome_src = master_dir / "userChrome.css"
    user_content_src = master_dir / "userContent.css"

    # Find all profile directories
    profiles = [p for p in MOZILLA_DIR.iterdir() if p.is_dir() and ((p / "prefs.js").is_file() or (p / "user.js").is_file() or (p / "chrome").is_dir() or "default" in p.name)]
    for prof in profiles:
        chrome_dir = prof / "chrome"
        chrome_dir.mkdir(parents=True, exist_ok=True)

        colors_css = chrome_dir / "colors.css"
        colors_content = f""":root {{
  --md-surface: {pal["surface"]};
  --md-surface-container: {pal["surface_container"]};
  --md-surface-container-high: {pal["surface_container_high"]};
  --md-surface-container-lowest: {pal["surface_container_lowest"]};
  --md-on-surface: {pal["on_surface"]};
  --md-on-surface-variant: {pal["on_surface_variant"]};
  --md-primary: {pal["primary"]};
  --md-primary-container: {pal["primary_container"]};
  --md-on-primary-container: {pal["on_primary_container"]};
  --md-secondary: {pal["secondary"]};
  --md-outline: {pal["outline"]};
  --md-outline-variant: {pal["outline_variant"]};
  --md-error: {pal["error"]};
  --md-green: {pal["green"]};
}}
"""
        colors_css.write_text(colors_content)

        # Copy master templates so any new laptop installation automatically gets full theme
        if user_chrome_src.is_file():
            shutil.copy2(user_chrome_src, chrome_dir / "userChrome.css")
        if user_content_src.is_file():
            shutil.copy2(user_content_src, chrome_dir / "userContent.css")

        # Ensure user.js enables custom stylesheets
        user_js = prof / "user.js"
        existing = user_js.read_text() if user_js.is_file() else ""
        additions = []
        if "toolkit.legacyUserProfileCustomizations.stylesheets" not in existing:
            additions.append('user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);')
        if "svg.context-properties.content.enabled" not in existing:
            additions.append('user_pref("svg.context-properties.content.enabled", true);')
        if "browser.newtabpage.activity-stream.testing.shouldInitializeFeeds" not in existing:
            additions.append('user_pref("browser.newtabpage.activity-stream.testing.shouldInitializeFeeds", true);')
        if "browser.startup.page" not in existing:
            additions.append('user_pref("browser.startup.page", 3);')

        if additions:
            with open(user_js, "a", encoding="utf-8") as f:
                f.write("\n" + "\n".join(additions) + "\n")

    # Trigger live reload on active Firefox session
    reload_firefox_live(pal)
