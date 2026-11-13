"""
Common Color & File Utilities for change-wallpaper
"""

import re
from pathlib import Path


def get_xterm256_palette():
    palette = []
    ansi_16 = [
        (0, 0, 0), (205, 0, 0), (0, 205, 0), (205, 205, 0),
        (0, 0, 238), (205, 0, 205), (0, 205, 205), (229, 229, 229),
        (127, 127, 127), (255, 0, 0), (0, 255, 0), (255, 255, 0),
        (92, 92, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
    ]
    palette.extend(ansi_16)
    steps = [0, 95, 175, 215, 239, 255]
    for r in steps:
        for g in steps:
            for b in steps:
                palette.append((r, g, b))
    for i in range(24):
        v = 8 + i * 10
        palette.append((v, v, v))
    return palette


XTERM_PALETTE = get_xterm256_palette()


def hex_to_xterm256(hex_str):
    hx = hex_str.lstrip("#")
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    best_idx = 16
    min_dist = float("inf")
    for idx in range(16, 256):
        pr, pg, pb = XTERM_PALETTE[idx]
        rmean = (r + pr) / 2
        dr, dg, db = r - pr, g - pg, b - pb
        dist = (2 + rmean / 256) * (dr**2) + 4 * (dg**2) + (2 + (255 - rmean) / 256) * (db**2)
        if dist < min_dist:
            min_dist = dist
            best_idx = idx
    return str(best_idx)


def hex_to_rgb_tuple(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def interpolate_hex(c1_hex, c2_hex, t):
    c1, c2 = hex_to_rgb_tuple(c1_hex), hex_to_rgb_tuple(c2_hex)
    return "#{:02x}{:02x}{:02x}".format(
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def generate_hex_gradient(stops, num_steps=8):
    result = []
    num_segments = len(stops) - 1
    steps_per_seg = num_steps / max(1, num_segments)
    for i in range(num_steps):
        seg = min(int(i / steps_per_seg), num_segments - 1)
        t = (i - seg * steps_per_seg) / steps_per_seg
        result.append(interpolate_hex(stops[seg], stops[seg + 1], t))
    return result


def generate_gradient_xterm(stops, num_steps=18):
    result = []
    num_segments = len(stops) - 1
    steps_per_seg = num_steps / max(1, num_segments)
    for i in range(num_steps):
        seg = min(int(i / steps_per_seg), num_segments - 1)
        t = (i - seg * steps_per_seg) / steps_per_seg
        hx = interpolate_hex(stops[seg], stops[seg + 1], t)
        result.append(hex_to_xterm256(hx))
    dedup = []
    for c in result:
        if not dedup or dedup[-1] != c:
            dedup.append(c)
    return dedup


def update_ini_file(file_path: Path, kv_dict: dict, strip_patterns: list = None):
    if not file_path.is_file():
        return
    try:
        content = file_path.read_text(encoding="utf-8")
        for k, v in kv_dict.items():
            pattern = rf"^(\s*{re.escape(k)}\s*=\s*).*$"
            if re.search(pattern, content, flags=re.MULTILINE):
                content = re.sub(pattern, rf"\g<1>{v}", content, flags=re.MULTILINE)
            else:
                content = content.rstrip() + f"\n{k} = {v}\n"
        if strip_patterns:
            for p in strip_patterns:
                content = re.sub(p, "", content, flags=re.MULTILINE)
        file_path.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"  [Note] update {file_path.name}: {e}")
