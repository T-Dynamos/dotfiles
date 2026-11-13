"""
Wofi Application Launcher Theme Updater
"""

from config import WOFI_DIR


def update_wofi(pal):
    WOFI_DIR.mkdir(parents=True, exist_ok=True)
    style_css = WOFI_DIR / "style.css"
    content = f"""* {{
  font-family: JetBrainsMono Nerd Font, Roboto, sans-serif;
  font-size: 14px;
}}

window {{
  margin: 0px;
  background-color: transparent;
  border: none;
}}

#window {{
  margin: 0px;
  background-color: transparent;
  border: none;
}}

#outer-box {{
  margin: 0px;
  padding: 14px;
  background-color: {pal["surface"]};
  border: 1.5px solid {pal["outline_variant"]};
  border-radius: 20px;
  box-shadow: none;
}}

#input {{
  margin: 6px 6px 14px 6px;
  padding: 10px 16px;
  border: 1px solid {pal["outline_variant"]};
  border-radius: 22px;
  color: {pal["on_surface"]};
  background-color: {pal["surface_container_lowest"]};
}}

#input:focus {{
  border: 1px solid {pal["primary"]};
  box-shadow: 0 0 0 1px {pal["primary"]};
}}

#scroll {{
  margin: 0px;
  border: none;
}}

#inner-box {{
  margin: 4px;
  border: none;
  background-color: transparent;
}}

#entry {{
  margin: 3px 4px;
  padding: 8px 12px;
  border-radius: 14px;
  border: none;
  color: {pal["on_surface"]};
  background-color: transparent;
  transition: all 0.15s ease;
}}

#entry:selected {{
  background-color: {pal["surface_container_high"]};
  color: {pal["primary"]};
  font-weight: 600;
}}

#text {{
  margin: 2px 8px;
  border: none;
  color: inherit;
}}

#img {{
  margin-right: 8px;
  background-color: transparent;
}}
"""
    style_css.write_text(content)
