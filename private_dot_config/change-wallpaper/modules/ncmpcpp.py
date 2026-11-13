"""
ncmpcpp Music Player Theme & UI Integration Updater
"""

from config import NCMPCPP_DIR
from utils import hex_to_xterm256, generate_gradient_xterm, update_ini_file

STRIP_KEYS = [
    r"^\s*main_window_highlight_color\s*=.*$\n?",
    r"^\s*active_column_color\s*=.*$\n?",
]


def update_ncmpcpp_file(file_path, kv_dict):
    update_ini_file(file_path, kv_dict, strip_patterns=STRIP_KEYS)


def update_ncmpcpp(pal):
    NCMPCPP_DIR.mkdir(parents=True, exist_ok=True)

    c_pri = hex_to_xterm256(pal["primary"])
    c_fg = hex_to_xterm256(pal["on_surface"])
    c_sec = hex_to_xterm256(pal["secondary"])
    c_ter = hex_to_xterm256(pal["tertiary"])
    c_bg_cont = hex_to_xterm256(pal["surface_container"])
    c_out = hex_to_xterm256(pal["outline"])
    c_teal = hex_to_xterm256(pal["teal"])
    c_purple = hex_to_xterm256(pal["purple"])

    stops = [pal["teal"], pal["primary"], pal["secondary"], pal["tertiary"], pal["purple"]]
    grad_indices = generate_gradient_xterm(stops, 18)
    vis_colors = '"' + ",".join(str(c) for c in grad_indices) + '"'

    alt_hdr_1 = '"$b$(' + str(c_teal) + ')╭───$(end) $b$(' + str(c_pri) + ')󰎆 {%t}|{%f}$/b$(end) $(' + str(c_teal) + ')───╮$(end)"'
    alt_hdr_2 = '"$b$(' + str(c_teal) + ')╰───$(end) $(' + str(c_sec) + ')󰠃 {%a}$/b$(end) {$b$(' + str(c_out) + ')• $/b$(end)$(' + str(c_ter) + ')󰀥 %b$/b$(end)} {$b$(' + str(c_out) + ')• $/b$(end)$(' + str(c_teal) + ')󰃭 %y$/b$(end)} $(' + str(c_teal) + ')───╯$(end)"'
    song_cols = f'"(4)[{c_out}]{{n}} (42)[{c_pri}]{{t}} (26)[{c_sec}]{{a}} (20)[{c_ter}]{{b}} (6)[{c_teal}]{{lr}}"'
    song_list = f'" $8%n$9 $({c_out})│$(end) $({c_pri})%t$(end) $({c_out})│$(end) $({c_sec})%a$(end) $R$({c_out})│$(end) $({c_teal})%l$(end) "'
    song_stat = f'"$b$({c_teal})󰐊 $({c_pri})%t$/b$(end) $({c_out})•$(end) $({c_sec})%a$(end) {{$({c_out})•$(end) $({c_ter})%b$(end)}}"'

    update_ncmpcpp_file(NCMPCPP_DIR / "config", {
        "colors_enabled": '"yes"',
        "header_window_color": f'"{c_pri}"',
        "volume_color": f'"{c_teal}"',
        "state_line_color": f'"{c_out}"',
        "state_flags_color": f'"{c_sec}"',
        "player_state_color": f'"{c_teal}"',
        "statusbar_color": f'"{c_fg}"',
        "statusbar_time_color": f'"{c_teal}"',
        "main_window_color": f'"{c_fg}"',
        "color1": f'"{c_fg}"',
        "color2": f'"{c_pri}"',
        "empty_tag_color": f'"{c_out}"',
        "window_border_color": f'"{c_out}"',
        "active_window_border": f'"{c_pri}"',
        "progressbar_color": f'"{c_bg_cont}"',
        "progressbar_elapsed_color": f'"{c_pri}"',
        "progressbar_look": '"━╸─"',
        "alternative_ui_separator_color": f'"{c_out}"',
        "alternative_header_first_line_format": alt_hdr_1,
        "alternative_header_second_line_format": alt_hdr_2,
        "song_status_format": song_stat,
        "song_columns_list_format": song_cols,
        "song_list_format": song_list,
        "now_playing_prefix": f'"$b$({c_teal})󰐊 $({c_pri})"',
        "now_playing_suffix": '"$/b$(end)"',
        "current_item_prefix": f'"$({c_pri})$r "',
        "current_item_suffix": '"$/r$(end)"',
        "current_item_inactive_column_prefix": f'"$({c_out})"',
        "current_item_inactive_column_suffix": '"$/r$(end)"',
        "selected_item_prefix": f'"$b$({c_teal})✔ $9"',
        "selected_item_suffix": '"$/b$(end)"',
        "modified_item_prefix": f'"$b$({c_ter})● $9"',
        "browser_playlist_prefix": f'"$b$({c_teal})󰲸 $9"',
        "visualizer_color": vis_colors,
    })

    update_ncmpcpp_file(NCMPCPP_DIR / "config-art", {
        "colors_enabled": '"yes"',
        "header_window_color": f'"{c_pri}"',
        "volume_color": f'"{c_teal}"',
        "state_line_color": f'"{c_out}"',
        "state_flags_color": f'"{c_sec}"',
        "player_state_color": f'"{c_teal}"',
        "statusbar_color": f'"{c_fg}"',
        "statusbar_time_color": f'"{c_teal}"',
        "main_window_color": f'"{c_fg}"',
        "color1": f'"{c_fg}"',
        "color2": f'"{c_pri}"',
        "empty_tag_color": f'"{c_out}"',
        "window_border_color": f'"{c_out}"',
        "active_window_border": f'"{c_pri}"',
        "progressbar_color": f'"{c_bg_cont}"',
        "progressbar_elapsed_color": f'"{c_pri}"',
        "progressbar_look": '"━╸─"',
        "alternative_ui_separator_color": f'"{c_out}"',
        "alternative_header_first_line_format": alt_hdr_1,
        "alternative_header_second_line_format": alt_hdr_2,
        "song_status_format": song_stat,
        "song_columns_list_format": song_cols,
        "song_list_format": song_list,
        "now_playing_prefix": f'"$b$({c_teal})󰐊 $({c_pri})"',
        "now_playing_suffix": '"$/b$(end)"',
        "current_item_prefix": f'"$({c_pri})$r "',
        "current_item_suffix": '"$/r$(end)"',
        "current_item_inactive_column_prefix": f'"$({c_out})"',
        "current_item_inactive_column_suffix": '"$/r$(end)"',
        "selected_item_prefix": f'"$b$({c_teal})✔ $9"',
        "selected_item_suffix": '"$/b$(end)"',
        "modified_item_prefix": f'"$b$({c_ter})● $9"',
        "browser_playlist_prefix": f'"$b$({c_teal})󰲸 $9"',
        "visualizer_color": vis_colors,
    })

    update_ncmpcpp_file(NCMPCPP_DIR / "catalog.conf", {
        "header_window_color": f'"{c_pri}"',
        "volume_color": f'"{c_teal}"',
        "state_line_color": f'"{c_out}"',
        "state_flags_color": f'"{c_pri}"',
        "main_window_color": f'"{c_fg}"',
        "color1": f'"{c_fg}"',
        "color2": f'"{c_pri}"',
        "progressbar_color": f'"{c_bg_cont}"',
        "progressbar_elapsed_color": f'"{c_pri}"',
        "progressbar_look": '"━╸─"',
        "statusbar_color": f'"{c_fg}"',
        "song_status_format": song_stat,
        "visualizer_color": vis_colors,
    })

    update_ncmpcpp_file(NCMPCPP_DIR / "visualizer.conf", {
        "header_window_color": f'"{c_pri}"',
        "volume_color": f'"{c_teal}"',
        "state_line_color": f'"{c_out}"',
        "state_flags_color": f'"{c_pri}"',
        "main_window_color": f'"{c_fg}"',
        "color1": f'"{c_fg}"',
        "color2": f'"{c_pri}"',
        "progressbar_color": f'"{c_bg_cont}"',
        "progressbar_elapsed_color": f'"{c_pri}"',
        "progressbar_look": '"━╸─"',
        "statusbar_color": f'"{c_fg}"',
        "song_status_format": song_stat,
        "visualizer_color": vis_colors,
    })
