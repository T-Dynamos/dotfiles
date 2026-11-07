#!/usr/bin/env python3
"""
Memento Mori - Desktop Lifespan Countdown Widget for Waybar
Calculates remaining weeks, days, and hours based on birth date (2007-04-21 04:00 AM)
and standard 80-year lifespan (2087-04-21 04:00 AM).
Displays percentage in the bar itself with right-to-left progress visualization.
"""

import datetime
import json
import sys

# User Birthdate: 21 April 2007, 04:00 AM
BIRTH_DATETIME = datetime.datetime(2007, 4, 21, 4, 0, 0)
# Lifespan: 80 years
TARGET_AGE = 80
TARGET_DATETIME = datetime.datetime(2007 + TARGET_AGE, 4, 21, 4, 0, 0)


def get_lifespan_data():
    now = datetime.datetime.now()

    diff = TARGET_DATETIME - now
    total_seconds = max(0, int(diff.total_seconds()))

    weeks = total_seconds // (7 * 24 * 3600)
    rem_seconds = total_seconds % (7 * 24 * 3600)
    days = rem_seconds // (24 * 3600)
    rem_seconds %= (24 * 3600)
    hours = rem_seconds // 3600

    total_span = (TARGET_DATETIME - BIRTH_DATETIME).total_seconds()
    lived_span = max(0, (now - BIRTH_DATETIME).total_seconds())
    pct = min(100.0, max(0.0, (lived_span / total_span) * 100))

    w_label = "week" if weeks == 1 else "weeks"
    d_label = "day" if days == 1 else "days"
    h_label = "hour" if hours == 1 else "hours"

    # Right-to-left progress bar track (48 characters to match text width)
    bar_len = 48
    filled = max(1, min(bar_len, int(round(bar_len * (pct / 100.0)))))
    unfilled = bar_len - filled
    progress_bar = (
        f"<span alpha='55%'>{'─' * unfilled}</span>"
        f"<span font_weight='bold'>╸</span>"
        f"<span font_weight='bold'>{'━' * max(0, filled - 1)}</span>"
    )

    # Aesthetic single-line display with percentage in the bar itself
    text = (
        f"<span size='x-large' font_weight='bold'>{weeks:,}</span> <span size='small' alpha='80%'>{w_label}</span>  •  "
        f"<span size='x-large' font_weight='bold'>{days}</span> <span size='small' alpha='80%'>{d_label}</span>  •  "
        f"<span size='x-large' font_weight='bold'>{hours}</span> <span size='small' alpha='80%'>{h_label}</span> <span size='small' alpha='70%'>left</span>  •  "
        f"<span size='x-large' font_weight='bold'>{pct:.1f}%</span>"
    )

    alt_text = f"󱑎 {weeks:,} {w_label}, {days} {d_label}, {hours} {h_label} left ({pct:.1f}% lived)"

    return {
        "text": text,
        "alt": alt_text,
        "class": "memento-mori",
        "percentage": round(pct, 1)
    }


if __name__ == "__main__":
    data = get_lifespan_data()
    print(json.dumps(data))
    sys.stdout.flush()
