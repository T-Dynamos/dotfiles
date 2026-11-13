"""
Material You Dynamic Palette Extraction
"""

import sys
from pathlib import Path
from PIL import Image

from materialyoucolor.quantize import ImageQuantizeCelebi
from materialyoucolor.score.score import Score
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.blend.blend import Blend
from materialyoucolor.utils.color_utils import hex_from_argb

SCHEMES = {
    "expressive": SchemeExpressive,
    "tonal-spot": SchemeTonalSpot,
    "vibrant": SchemeVibrant,
    "fruit-salad": SchemeFruitSalad,
    "rainbow": SchemeRainbow,
}


def hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)


def extract_palette(image_path, is_dark=True, scheme_name="expressive"):
    seed = None
    path_str = str(image_path)
    if Path(image_path).is_file():
        try:
            colors = ImageQuantizeCelebi(path_str, 5, 128)
            ranked = Score.score(colors)
            if ranked:
                seed = ranked[0]
        except Exception as e:
            print(f"[Warning] Failed to quantize image with C++ celebi: {e}", file=sys.stderr)

    if seed is None:
        seed = 0xFF6750A4  # Default Material purple seed

    scheme_cls = SCHEMES.get(scheme_name.lower(), SchemeExpressive)
    scheme = scheme_cls(Hct.from_int(seed), is_dark, 0.0)
    mdc = MaterialDynamicColors()

    def get_c(name):
        return getattr(mdc, name).get_hex(scheme)[:7]

    def harm_tone(color_int, tone):
        h = Hct.from_int(Blend.harmonize(color_int, seed))
        h.tone = tone
        return hex_from_argb(h.to_int())[:7]

    return {
        "seed": hex_from_argb(seed)[:7],
        "surface": get_c("surface"),
        "surface_container": get_c("surfaceContainer"),
        "surface_container_high": get_c("surfaceContainerHigh"),
        "surface_container_lowest": get_c("surfaceContainerLowest"),
        "on_surface": get_c("onSurface"),
        "on_surface_variant": get_c("onSurfaceVariant"),
        "outline": get_c("outline"),
        "outline_variant": get_c("outlineVariant"),
        "primary": get_c("primary"),
        "on_primary": get_c("onPrimary"),
        "primary_container": get_c("primaryContainer"),
        "on_primary_container": get_c("onPrimaryContainer"),
        "secondary": get_c("secondary"),
        "on_secondary": get_c("onSecondary"),
        "secondary_container": get_c("secondaryContainer"),
        "on_secondary_container": get_c("onSecondaryContainer"),
        "tertiary": get_c("tertiary"),
        "on_tertiary": get_c("onTertiary"),
        "tertiary_container": get_c("tertiaryContainer"),
        "on_tertiary_container": get_c("onTertiaryContainer"),
        "error": get_c("error"),
        "on_error": get_c("onError"),
        "error_container": get_c("errorContainer"),
        "on_error_container": get_c("onErrorContainer"),
        "green": harm_tone(0xFF4CAF50, 80),
        "green_bright": harm_tone(0xFF4CAF50, 90),
        "green_dark": harm_tone(0xFF4CAF50, 20),
        "yellow": harm_tone(0xFFFFEB3B, 80),
        "yellow_bright": harm_tone(0xFFFFEB3B, 90),
        "yellow_dark": harm_tone(0xFFFFEB3B, 20),
        "teal": harm_tone(0xFF00BCD4, 80),
        "teal_bright": harm_tone(0xFF00BCD4, 90),
        "teal_dark": harm_tone(0xFF00BCD4, 20),
        "purple": harm_tone(0xFFAB47BC, 80),
        "purple_bright": harm_tone(0xFFAB47BC, 90),
        "purple_dark": harm_tone(0xFFAB47BC, 20),
        "peach": harm_tone(0xFFFF8A65, 80),
        "peach_bright": harm_tone(0xFFFF8A65, 90),
        "peach_dark": harm_tone(0xFFFF8A65, 20),
    }
