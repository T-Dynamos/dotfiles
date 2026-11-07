#!/usr/bin/env bash
# toggle-floating.sh: Toggle floating window with dynamic border
# Adds border pixel 2 when floating, removes border when tiled

python3 - << 'EOF'
import subprocess
import json
import sys

try:
    res = subprocess.run(['swaymsg', '-t', 'get_tree'], capture_output=True, text=True, timeout=2)
    tree = json.loads(res.stdout)

    def check_floating(node, in_floating=False):
        if node.get('focused'):
            return in_floating or node.get('type') == 'floating_con'
        for fn in node.get('floating_nodes', []):
            res = check_floating(fn, in_floating=True)
            if res is not None:
                return res
        for tn in node.get('nodes', []):
            res = check_floating(tn, in_floating=in_floating)
            if res is not None:
                return res
        return None

    is_float = check_floating(tree)
    if is_float:
        subprocess.run(['swaymsg', 'floating disable; border none'])
    else:
        subprocess.run(['swaymsg', 'floating enable; border pixel 2'])
except Exception:
    subprocess.run(['swaymsg', 'floating toggle; border toggle'])
EOF
