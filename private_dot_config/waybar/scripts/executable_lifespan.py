#!/usr/bin/env python3
"""
Memento Mori - Desktop Lifespan Countdown Widget for Waybar
Calculates remaining weeks, days, and hours based on birth date (2007-04-21 04:00 AM)
and standard 80-year lifespan (2087-04-21 04:00 AM).
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
    lived_weeks = int(lived_span // (7 * 86400))

    w_label = "week" if weeks == 1 else "weeks"
    d_label = "day" if days == 1 else "days"
    h_label = "hour" if hours == 1 else "hours"

    # Multi-line aesthetic display
    text = (
        f"<span size='small' letter_spacing='3000' alpha='70%' font_weight='bold'>M E M E N T O   M O R I</span>\n"
        f"<span size='x-large' font_weight='bold'>{weeks:,}</span> <span size='small' alpha='80%'>{w_label}</span>  •  "
        f"<span size='x-large' font_weight='bold'>{days}</span> <span size='small' alpha='80%'>{d_label}</span>  •  "
        f"<span size='x-large' font_weight='bold'>{hours}</span> <span size='small' alpha='80%'>{h_label}</span> <span size='small' alpha='70%'>left</span>"
    )

    alt_text = f"󱑎 {weeks:,} {w_label}, {days} {d_label}, {hours} {h_label} left (~{pct:.1f}% lived)"

    tooltip = (
        f"⏳ MEMENTO MORI\n"
        f"─────────────────────────────────────\n"
        f"Born: 21 April 2007, 04:00 AM\n"
        f"Target (80 yrs): 21 April 2087\n"
        f"Time Elapsed: {pct:.2f}% ({lived_weeks:,} weeks lived)\n"
        f"Time Remaining: {weeks:,} {w_label}, {days} {d_label}, {hours} {h_label}\n"
        f"─────────────────────────────────────\n"
        f"\"You could leave life right now.\nLet that determine what you do and say and think.\"\n— Marcus Aurelius"
    )

    return {
        "text": text,
        "alt": alt_text,
        "tooltip": tooltip,
        "class": "memento-mori",
        "percentage": round(pct, 1)
    }


if __name__ == "__main__":
    data = get_lifespan_data()
    print(json.dumps(data))
    sys.stdout.flush()
