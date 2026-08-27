#!/usr/bin/env python3
"""Generate a stable, constrained visual identity for a GitHub repository."""

from __future__ import annotations

import argparse
import colorsys
import json
import math
import re
from dataclasses import asdict, dataclass


GENERATOR_VERSION = 2
MIN_ADJACENT_HUE_DISTANCE = 72
MIN_ADJACENT_OKLAB_DISTANCE = 0.15
GOLDEN_ANGLE = 137.50776405003785
MAX_COLOR_CANDIDATES = 48
FULL_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
MOTIFS = ("orbit", "network", "wave", "radial", "stack", "grid", "path", "polyline")
FAMILY_MOTIFS = {
    "video": ("orbit", "wave", "path"),
    "design": ("wave", "stack", "path", "polyline"),
    "photo": ("radial", "grid", "stack"),
    "automation": ("network", "path", "polyline"),
    "data": ("grid", "stack", "polyline"),
    "ai": ("radial", "network", "orbit"),
    "general": MOTIFS,
}


@dataclass(frozen=True)
class VisualIdentity:
    generatorVersion: int
    seed: str
    accent: str
    foreground: str
    motif: str
    variant: int


def fnv1a_32(value: str) -> int:
    result = 0x811C9DC5
    for byte in value.encode("utf-8"):
        result ^= byte
        result = (result * 0x01000193) & 0xFFFFFFFF
    return result


def hsl_to_hex(hue: float, saturation: float, lightness: float) -> str:
    red, green, blue = colorsys.hls_to_rgb((hue % 360) / 360, lightness / 100, saturation / 100)
    return f"#{round(red * 255):02x}{round(green * 255):02x}{round(blue * 255):02x}"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def relative_luminance(value: str) -> float:
    channels = []
    for channel in hex_to_rgb(value):
        normalized = channel / 255
        channels.append(normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def hue_from_hex(value: str) -> float:
    red, green, blue = (channel / 255 for channel in hex_to_rgb(value))
    hue, _, _ = colorsys.rgb_to_hsv(red, green, blue)
    return hue * 360


def hue_distance(first: float, second: float) -> float:
    distance = abs(first - second) % 360
    return min(distance, 360 - distance)


def oklab_from_hex(value: str) -> tuple[float, float, float]:
    def linearize(channel: int) -> float:
        normalized = channel / 255
        return normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4

    red, green, blue = (linearize(channel) for channel in hex_to_rgb(value))
    long = 0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue
    medium = 0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue
    short = 0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue
    long_root, medium_root, short_root = math.cbrt(long), math.cbrt(medium), math.cbrt(short)
    return (
        0.2104542553 * long_root + 0.7936177850 * medium_root - 0.0040720468 * short_root,
        1.9779984951 * long_root - 2.4285922050 * medium_root + 0.4505937099 * short_root,
        0.0259040371 * long_root + 0.7827717662 * medium_root - 0.8086757660 * short_root,
    )


def perceptual_distance(first: str, second: str) -> float:
    return math.dist(oklab_from_hex(first), oklab_from_hex(second))


def colors_are_distinct(first: str, second: str) -> bool:
    return (
        hue_distance(hue_from_hex(first), hue_from_hex(second)) >= MIN_ADJACENT_HUE_DISTANCE
        and perceptual_distance(first, second) >= MIN_ADJACENT_OKLAB_DISTANCE
    )


def accessible_accent(hue: float, saturation: float, initial_lightness: float) -> str:
    lightness = initial_lightness
    accent = hsl_to_hex(hue, saturation, lightness)
    while contrast_ratio(accent, "#ffffff") < 4.5 and lightness > 20:
        lightness -= 1
        accent = hsl_to_hex(hue, saturation, lightness)
    return accent


def generate_visual_identity(
    seed: str,
    family_hint: str = "general",
    motif: str | None = None,
    avoid: tuple[str, ...] = (),
) -> VisualIdentity:
    if not FULL_NAME.fullmatch(seed):
        raise ValueError("seed must use canonical owner/repository form")
    if family_hint not in FAMILY_MOTIFS:
        raise ValueError(f"unknown family hint: {family_hint}")
    if motif is not None and motif not in MOTIFS:
        raise ValueError(f"unknown motif: {motif}")
    if any(not HEX.fullmatch(color) for color in avoid):
        raise ValueError("avoid colors must be six-digit hex values")

    normalized_seed = seed.lower()
    color_seed = fnv1a_32(f"{normalized_seed}:color")
    base_hue = color_seed % 360
    saturation = 58 + ((color_seed >> 9) % 13)
    lightness = 43 + ((color_seed >> 17) % 6)
    accent = accessible_accent(float(base_hue), saturation, lightness)
    if avoid:
        for attempt in range(MAX_COLOR_CANDIDATES):
            candidate_hue = (base_hue + attempt * GOLDEN_ANGLE) % 360
            candidate = accessible_accent(candidate_hue, saturation, lightness)
            if all(colors_are_distinct(candidate, existing) for existing in avoid):
                accent = candidate
                break
        else:
            raise ValueError(
                "cannot find a sufficiently distinct accent; pass only the immediately adjacent colors or reorder the feed"
            )

    black_contrast = contrast_ratio(accent, "#000000")
    white_contrast = contrast_ratio(accent, "#ffffff")
    foreground = "#000000" if black_contrast >= white_contrast else "#ffffff"

    motif_options = FAMILY_MOTIFS[family_hint]
    chosen_motif = motif or motif_options[fnv1a_32(f"{normalized_seed}:motif") % len(motif_options)]
    variant = fnv1a_32(f"{normalized_seed}:variant")
    return VisualIdentity(GENERATOR_VERSION, seed, accent, foreground, chosen_motif, variant)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", help="Canonical GitHub owner/repository")
    parser.add_argument("--family-hint", choices=tuple(FAMILY_MOTIFS), default="general")
    parser.add_argument("--motif", choices=MOTIFS)
    parser.add_argument("--avoid", action="append", default=[], help="Existing six-digit hex accent; repeat as needed")
    args = parser.parse_args()
    try:
        identity = generate_visual_identity(args.seed, args.family_hint, args.motif, tuple(args.avoid))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(asdict(identity), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
