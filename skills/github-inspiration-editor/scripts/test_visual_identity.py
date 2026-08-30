#!/usr/bin/env python3
"""Tests for deterministic visual identity generation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from generate_visual_identity import (
    GENERATOR_VERSION,
    MIN_ADJACENT_HUE_DISTANCE,
    MIN_ADJACENT_OKLAB_DISTANCE,
    colors_are_distinct,
    contrast_ratio,
    generate_visual_identity,
    hue_distance,
    hue_from_hex,
    perceptual_distance,
)


class VisualIdentityTests(unittest.TestCase):
    def test_same_inputs_are_deterministic(self) -> None:
        first = generate_visual_identity("immich-app/immich", "photo")
        second = generate_visual_identity("immich-app/immich", "photo")
        self.assertEqual(first, second)

    def test_repository_seed_changes_identity(self) -> None:
        first = generate_visual_identity("immich-app/immich", "photo")
        second = generate_visual_identity("usememos/memos", "photo")
        self.assertNotEqual((first.accent, first.variant), (second.accent, second.variant))

    def test_accent_is_readable_on_white(self) -> None:
        for seed in ("remotion-dev/remotion", "excalidraw/excalidraw", "immich-app/immich", "n8n-io/n8n"):
            identity = generate_visual_identity(seed)
            self.assertGreaterEqual(contrast_ratio(identity.accent, "#ffffff"), 4.5)

    def test_adjacent_color_avoidance(self) -> None:
        original = generate_visual_identity("immich-app/immich", "photo")
        adjusted = generate_visual_identity("immich-app/immich", "photo", avoid=(original.accent,))
        self.assertGreaterEqual(
            hue_distance(hue_from_hex(adjusted.accent), hue_from_hex(original.accent)),
            MIN_ADJACENT_HUE_DISTANCE,
        )
        self.assertGreaterEqual(perceptual_distance(adjusted.accent, original.accent), MIN_ADJACENT_OKLAB_DISTANCE)

    def test_known_green_sequence_is_rejected(self) -> None:
        self.assertFalse(colors_are_distinct("#588019", "#1c871f"))
        self.assertFalse(colors_are_distinct("#1c871f", "#198575"))

    def test_generated_feed_sequence_has_distinct_neighbors(self) -> None:
        projects = (
            ("remotion-dev/remotion", "video"),
            ("excalidraw/excalidraw", "design"),
            ("immich-app/immich", "photo"),
            ("n8n-io/n8n", "automation"),
        )
        accents: list[str] = []
        for seed, family_hint in projects:
            avoid = (accents[-1],) if accents else ()
            identity = generate_visual_identity(seed, family_hint, avoid=avoid)
            self.assertEqual(identity.generatorVersion, GENERATOR_VERSION)
            accents.append(identity.accent)
        for first, second in zip(accents, accents[1:]):
            self.assertTrue(colors_are_distinct(first, second), f"adjacent accents are too similar: {first}, {second}")

    def test_published_feed_has_distinct_neighbors(self) -> None:
        root = Path(__file__).resolve().parents[3]
        order = json.loads((root / "src/data/order.json").read_text(encoding="utf-8"))
        visuals = json.loads((root / "src/data/visuals.json").read_text(encoding="utf-8"))
        accents = {project_id: visual["accent"] for project_id, visual in visuals.items()}
        self.assertEqual(set(order), set(accents))
        for first_id, second_id in zip(order, order[1:]):
            self.assertTrue(
                colors_are_distinct(accents[first_id], accents[second_id]),
                f"published neighbors {first_id} and {second_id} are too similar: {accents[first_id]}, {accents[second_id]}",
            )

    def test_family_hint_limits_motif(self) -> None:
        identity = generate_visual_identity("n8n-io/n8n", "automation")
        self.assertIn(identity.motif, {"network", "path", "polyline"})

    def test_invalid_seed_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            generate_visual_identity("not-a-repository")


if __name__ == "__main__":
    unittest.main()
