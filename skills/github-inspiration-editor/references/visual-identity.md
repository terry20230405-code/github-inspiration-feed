# Deterministic visual identity

Every published project stores a small visual identity generated from a stable repository seed. The frontend renders the stored configuration; it does not choose a new identity on each page load.

## Stored fields

- `generatorVersion`: visual generator and renderer contract version. Version 2 adds perceptual neighbor avoidance; version 1 remains valid for already persisted identities.
- `seed`: the canonical `owner/repository` used when the identity was first generated. Keep it unchanged after repository renames so an existing card does not unexpectedly change.
- `accent`: restrained theme color with at least 4.5:1 contrast against white.
- `foreground`: `#000000` or `#ffffff`, whichever has stronger contrast on the accent.
- `motif`: one of `orbit`, `network`, `wave`, `radial`, `stack`, `grid`, `path`, or `polyline`.
- `variant`: deterministic integer used by the SVG renderer to choose element count, position, rotation, density, line weight, symmetry, and entry direction.

## Choosing a motif family

Use repository evidence and editorial understanding to choose the broad family hint. This hint is an internal generation input, not a display category and is not stored in the project record.

| Repository capability | Preferred families |
| --- | --- |
| Video or audio | `orbit`, `wave`, `path` |
| Drawing or design | `wave`, `stack`, `path`, `polyline` |
| Photos or personal media | `radial`, `grid`, `stack` |
| Automation or backend workflows | `network`, `path`, `polyline` |
| Data tools | `grid`, `stack`, `polyline` |
| AI systems | `radial`, `network`, `orbit` |

When no family is clearly supported, use `general`; the generator chooses from all families. Do not invent a product category just to choose a motif.

## Generate an identity

Run from the skill directory:

```bash
python scripts/generate_visual_identity.py owner/repository --family-hint photo
```

To keep nearby feed cards visually distinct, pass the accent of the immediately preceding card when appending. When inserting a project, pass both cards that will touch it:

```bash
python scripts/generate_visual_identity.py owner/repository --family-hint photo --avoid '#8a3f62' --avoid '#315e88'
```

Version 2 accepts a candidate only when it clears both a 72-degree hue gap and an OKLab perceptual-distance threshold from every supplied neighbor. It searches hues using the golden angle so a rejected green does not simply move to another nearby green. If no candidate satisfies every supplied color, generation stops instead of silently returning a collision. Pass immediate neighbors only; do not pass the entire historical feed.

The same seed, family hint, and avoidance set always produce the same output. Once accepted, persist the complete output. Later metadata refreshes must not regenerate it. When the algorithm changes, increment `generatorVersion`; do not rewrite existing identities merely to adopt the new version. A deliberate visual migration requested by the product owner is the exception and must update the stored version together with the accepted accent.

After adding, inserting, reordering, or deliberately migrating a published card, run from the project root:

```bash
npm run test:visual-identity
```

This test checks the generator and the actual `projectIds` feed order, so a sequence of individually valid but visually similar colors cannot pass unnoticed.

## Rendering limits

The frontend SVG renderer must:

- render from persisted `motif` and `variant` only;
- use approximately 5–12 simple SVG elements;
- inherit `accent` through `currentColor`;
- remain decorative with `aria-hidden="true"`;
- avoid network-loaded images, repository logos, and project-name CSS selectors;
- honor `prefers-reduced-motion` through the page's existing motion rules.
