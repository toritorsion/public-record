#!/usr/bin/env python3
"""
Generate monochrome ransom-style masthead titles from the real PNG letter pack.

Default output:
  - assets/generated-titles/residual.png
  - assets/generated-titles/first-day.png
  - assets/generated-titles/catalog.png
  - preview/ransom-titles.html
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from PIL import Image, ImageChops, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[2]
ASSET_PACK = (
    ROOT
    / "PUBLIC_RECORD_WE_WERE_THERE_SITE_ASSETS"
    / "11_DESIGN ELEMENTS"
    / "1RANSOM LETTERS"
)
OUTPUT_DIR = ROOT / "assets" / "generated-titles"
OPTIONS_DIR = OUTPUT_DIR / "_options"
PREVIEW_FILE = ROOT / "preview" / "ransom-titles.html"

DEFAULT_TITLES: Sequence[Tuple[str, str]] = (
    ("residual", "RESIDUAL"),
    ("first-day", "FIRST DAY"),
    ("catalog", "CATALOG"),
)

STYLE_PRESETS = {
    "residual": {
        "base_height": 330,
        "min_width": 2700,
        "min_height": 640,
        "space_factor": 0.32,
        "tracking_factor": 0.018,
        "tracking_jitter": 0.020,
        "scale_jitter": 0.055,
        "rotate_max": 2.0,
        "y_jitter": 0.055,
        "density_target": 0.88,
    },
    "first-day": {
        "base_height": 320,
        "min_width": 2600,
        "min_height": 620,
        "space_factor": 0.35,
        "tracking_factor": 0.030,
        "tracking_jitter": 0.020,
        "scale_jitter": 0.050,
        "rotate_max": 1.9,
        "y_jitter": 0.050,
        "density_target": 0.84,
    },
    "catalog": {
        "base_height": 300,
        "min_width": 2400,
        "min_height": 600,
        "space_factor": 0.34,
        "tracking_factor": 0.048,
        "tracking_jitter": 0.018,
        "scale_jitter": 0.045,
        "rotate_max": 1.7,
        "y_jitter": 0.045,
        "density_target": 0.80,
    },
    "default": {
        "base_height": 310,
        "min_width": 2400,
        "min_height": 600,
        "space_factor": 0.34,
        "tracking_factor": 0.034,
        "tracking_jitter": 0.018,
        "scale_jitter": 0.050,
        "rotate_max": 1.8,
        "y_jitter": 0.050,
        "density_target": 0.82,
    },
}


@dataclass(frozen=True)
class VariantStat:
    path: Path
    score: float
    width: int
    height: int


def slugify(value: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return out or "title"


def parse_titles(raw_titles: Sequence[str]) -> List[Tuple[str, str]]:
    if not raw_titles:
        return list(DEFAULT_TITLES)

    parsed: List[Tuple[str, str]] = []
    for raw in raw_titles:
        if "=" in raw:
            slug, text = raw.split("=", 1)
            parsed.append((slugify(slug), text.strip()))
        else:
            text = raw.strip()
            parsed.append((slugify(text), text))
    return parsed


def alpha_coverage(mask: Image.Image) -> float:
    hist = mask.histogram()
    weighted = sum(value * count for value, count in enumerate(hist)) / 255.0
    total = mask.width * mask.height
    return weighted / total if total else 0.0


def discover_asset_map(asset_root: Path) -> Dict[str, List[Path]]:
    """
    Build a character map automatically from real file names/folders.
    """
    char_map: Dict[str, List[Path]] = {}

    def add_char(char: str, path: Path) -> None:
        char = char.upper()
        char_map.setdefault(char, []).append(path)

    for png in sorted(asset_root.rglob("*.png")):
        path_parts = {part.lower() for part in png.parts}
        parent = png.parent.name
        stem = png.stem

        # Primary A-Z folders
        if "png letter_a-m" in path_parts or "png letter_n-z" in path_parts:
            if len(parent) == 1 and parent.isalpha() and re.match(
                rf"^{re.escape(parent)}-\d+$", stem, re.IGNORECASE
            ):
                add_char(parent, png)
            continue

        # Numbers and special characters package
        if "png letters_01" in path_parts:
            if len(parent) == 1 and parent.isdigit() and re.match(
                rf"^{re.escape(parent)}-\d+$", stem, re.IGNORECASE
            ):
                add_char(parent, png)
                continue

            token = stem.lower().split("-")[0]
            special_map = {
                "dash": "-",
                "point": ".",
                "comma": ",",
                "plus": "+",
                "slash": "/",
                "question": "?",
                "esclamation": "!",
                "quotation": '"',
                "semicolon": ";",
                "colon": ":",
                "percent": "%",
                "dollar": "$",
                "and": "&",
                "at": "@",
            }
            if token in special_map:
                add_char(special_map[token], png)

    for key in list(char_map.keys()):
        char_map[key] = sorted(char_map[key])
    return char_map


def preprocess_variant(path: Path) -> Tuple[Image.Image, float]:
    """
    Convert a letter to high-contrast monochrome while preserving transparency.
    Returns (processed_image, strength_score).
    """
    src = Image.open(path).convert("RGBA")
    alpha = src.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0)), 0.0

    src = src.crop(bbox)
    alpha = alpha.crop(bbox)
    gray = ImageOps.grayscale(src)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.7)

    # Binary split to hard black/white inside the existing alpha shape.
    binary = gray.point(lambda p: 255 if p >= 146 else 0, mode="L")
    white_mask = ImageChops.multiply(binary, alpha)
    black_mask = ImageChops.multiply(ImageOps.invert(binary), alpha)

    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    out.paste((246, 246, 242, 255), (0, 0), white_mask)
    out.paste((11, 11, 10, 255), (0, 0), black_mask)

    # Score "strength" for monochrome readability.
    coverage = alpha_coverage(alpha)
    white_cov = alpha_coverage(white_mask)
    black_cov = alpha_coverage(black_mask)
    filled = max(white_cov + black_cov, 1e-6)
    ink_ratio = black_cov / filled

    # Aim for clear figure/ground and enough visual weight.
    balance = max(0.0, 1.0 - abs(ink_ratio - 0.30) / 0.30)
    density = max(0.0, 1.0 - abs(coverage - 0.62) / 0.62)
    score = 0.65 * balance + 0.35 * density

    return out, score


class VariantLibrary:
    def __init__(self, char_map: Dict[str, List[Path]]):
        self.char_map = char_map
        self._stats_cache: Dict[str, List[VariantStat]] = {}
        self._image_cache: Dict[Path, Image.Image] = {}

    def has_char(self, char: str) -> bool:
        return char.upper() in self.char_map

    def stats_for(self, char: str) -> List[VariantStat]:
        char = char.upper()
        if char in self._stats_cache:
            return self._stats_cache[char]

        stats: List[VariantStat] = []
        for path in self.char_map.get(char, []):
            processed, score = preprocess_variant(path)
            self._image_cache[path] = processed
            stats.append(
                VariantStat(path=path, score=score, width=processed.width, height=processed.height)
            )

        stats.sort(key=lambda item: item.score, reverse=True)
        self._stats_cache[char] = stats
        return stats

    def image_for(self, path: Path) -> Image.Image:
        cached = self._image_cache.get(path)
        if cached is None:
            processed, _ = preprocess_variant(path)
            self._image_cache[path] = processed
            cached = processed
        return cached.copy()


def weighted_pick(rng: random.Random, variants: List[VariantStat]) -> VariantStat:
    if not variants:
        raise ValueError("No variants provided for weighted_pick")

    shortlist = variants[: max(8, len(variants) // 2)]
    weights = [max(0.05, variant.score) for variant in shortlist]
    return rng.choices(shortlist, weights=weights, k=1)[0]


def compose_word_image(
    text: str,
    slug: str,
    library: VariantLibrary,
    rng: random.Random,
) -> Tuple[Image.Image, Dict[str, object]]:
    style = STYLE_PRESETS.get(slug, STYLE_PRESETS["default"])

    text_up = text.upper()
    base_h = int(style["base_height"])
    baseline = int(base_h * 1.18)
    space_w = int(base_h * float(style["space_factor"]))
    tracking = base_h * float(style["tracking_factor"])
    tracking_jitter = base_h * float(style["tracking_jitter"])
    scale_jitter = float(style["scale_jitter"])
    rotate_max = float(style["rotate_max"])
    y_jitter = base_h * float(style["y_jitter"])

    placements = []
    cursor_x = 0
    glyph_scores: List[float] = []
    selected_paths: List[str] = []
    scales: List[float] = []
    rotations: List[float] = []
    skipped_chars: List[str] = []

    for char in text_up:
        if char == " ":
            cursor_x += space_w
            continue

        if not library.has_char(char):
            skipped_chars.append(char)
            continue

        options = library.stats_for(char)
        if not options:
            skipped_chars.append(char)
            continue

        chosen = weighted_pick(rng, options)
        glyph = library.image_for(chosen.path)

        scale = 1.0 + rng.uniform(-scale_jitter, scale_jitter)
        target_h = max(48, int(base_h * scale))
        target_w = max(16, int(glyph.width * (target_h / glyph.height)))
        glyph = glyph.resize((target_w, target_h), Image.LANCZOS)

        rotation = rng.uniform(-rotate_max, rotate_max)
        glyph = glyph.rotate(rotation, expand=True, resample=Image.BICUBIC)

        y_offset = int(rng.uniform(-y_jitter, y_jitter))
        y = baseline - glyph.height + y_offset

        placements.append((glyph, cursor_x, y))
        glyph_scores.append(chosen.score)
        selected_paths.append(str(chosen.path.relative_to(ROOT)))
        scales.append(scale)
        rotations.append(abs(rotation))

        letter_spacing = int(tracking + rng.uniform(-tracking_jitter, tracking_jitter))
        min_spacing = -int(base_h * 0.04)
        cursor_x += glyph.width + max(min_spacing, letter_spacing)

    if not placements:
        raise RuntimeError(f'No supported characters found in "{text}"')

    min_x = min(x for _, x, _ in placements)
    min_y = min(y for _, _, y in placements)
    max_x = max(x + glyph.width for glyph, x, _ in placements)
    max_y = max(y + glyph.height for glyph, _, y in placements)

    pad_x = int(base_h * 0.18)
    pad_y = int(base_h * 0.18)
    tight_w = (max_x - min_x) + pad_x * 2
    tight_h = (max_y - min_y) + pad_y * 2
    tight_img = Image.new("RGBA", (tight_w, tight_h), (0, 0, 0, 0))

    for glyph, x, y in placements:
        tight_img.alpha_composite(glyph, (x - min_x + pad_x, y - min_y + pad_y))

    final_w = max(int(style["min_width"]), tight_w)
    final_h = max(int(style["min_height"]), tight_h)
    final_img = Image.new("RGBA", (final_w, final_h), (0, 0, 0, 0))
    origin_x = (final_w - tight_w) // 2
    origin_y = (final_h - tight_h) // 2
    final_img.alpha_composite(tight_img, (origin_x, origin_y))

    avg_score = sum(glyph_scores) / len(glyph_scores)
    avg_rotation = sum(rotations) / max(len(rotations), 1)
    avg_scale_deviation = sum(abs(s - 1.0) for s in scales) / max(len(scales), 1)
    density_ratio = tight_w / final_w
    density_target = float(style["density_target"])
    density_score = max(0.0, 1.0 - abs(density_ratio - density_target) / max(0.01, density_target))
    neatness_score = max(
        0.0,
        1.0 - (avg_rotation / max(0.1, rotate_max)) * 0.45 - (avg_scale_deviation / max(0.01, scale_jitter)) * 0.20,
    )

    composition_score = (avg_score * 0.55) + (density_score * 0.30) + (neatness_score * 0.15)

    meta = {
        "text": text_up,
        "score": round(composition_score, 4),
        "avg_letter_score": round(avg_score, 4),
        "density_ratio": round(density_ratio, 4),
        "selected_variants": selected_paths,
        "skipped_characters": skipped_chars,
        "size": {"width": final_w, "height": final_h},
    }
    return final_img, meta


def generate_for_title(
    slug: str,
    text: str,
    library: VariantLibrary,
    options_per_title: int,
    base_seed: int,
) -> Dict[str, object]:
    OPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    slug_hash = int(hashlib.sha1(slug.encode("utf-8")).hexdigest()[:8], 16)
    variants = []

    for index in range(options_per_title):
        seed = base_seed + slug_hash + (index * 7907)
        rng = random.Random(seed)
        image, meta = compose_word_image(text=text, slug=slug, library=library, rng=rng)
        option_name = f"{slug}-{index + 1:02d}.png"
        option_path = OPTIONS_DIR / option_name
        image.save(option_path, format="PNG", optimize=True, compress_level=9)
        meta.update({"seed": seed, "file": option_name})
        variants.append(meta)

    variants.sort(key=lambda row: row["score"], reverse=True)
    best = variants[0]
    best_source = OPTIONS_DIR / best["file"]
    final_name = f"{slug}.png"
    final_path = OUTPUT_DIR / final_name
    best_image = Image.open(best_source).convert("RGBA")
    best_image.save(final_path, format="PNG", optimize=True, compress_level=9)

    return {
        "slug": slug,
        "text": text,
        "final_file": final_name,
        "final_source_option": best["file"],
        "final_score": best["score"],
        "variants": variants,
    }


def write_preview(manifest: Dict[str, object]) -> None:
    PREVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    title_blocks = []

    for item in manifest["titles"]:
        options_html = []
        for option in item["variants"]:
            options_html.append(
                f"""
                <figure class="option">
                  <img src="../assets/generated-titles/_options/{option['file']}" alt="{item['text']} option">
                  <figcaption>{option['file']} &middot; score {option['score']}</figcaption>
                </figure>
                """
            )

        block = f"""
        <section class="title-block">
          <h2>{item['text']}</h2>
          <div class="final-wrap">
            <img class="final" src="../assets/generated-titles/{item['final_file']}" alt="{item['text']} final title">
            <p>Final: <code>{item['final_file']}</code> (source option: <code>{item['final_source_option']}</code>)</p>
          </div>
          <div class="options-grid">
            {''.join(options_html)}
          </div>
        </section>
        """
        title_blocks.append(block)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ransom Title Preview</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0f0f0d;
      --panel: #1a1a18;
      --line: #393934;
      --text: #ece9e0;
      --muted: #8d8a82;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 28px;
      font-family: "Newsreader", Georgia, serif;
      background: var(--bg);
      color: var(--text);
    }}
    h1 {{
      margin: 0 0 20px;
      letter-spacing: .04em;
      text-transform: uppercase;
      font-size: 28px;
    }}
    .title-block {{
      border: 1px solid var(--line);
      background: var(--panel);
      margin-bottom: 26px;
      padding: 16px;
    }}
    h2 {{
      margin: 0 0 10px;
      font-size: 17px;
      text-transform: uppercase;
      letter-spacing: .09em;
      color: var(--muted);
    }}
    .final-wrap {{
      border: 1px solid var(--line);
      background: #11110f;
      padding: 18px;
      margin-bottom: 14px;
    }}
    .final {{
      width: min(100%, 1100px);
      display: block;
      margin: 0 auto;
    }}
    .final-wrap p {{
      margin: 10px 0 0;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .05em;
    }}
    .options-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 10px;
    }}
    .option {{
      margin: 0;
      border: 1px solid var(--line);
      background: #10100f;
      padding: 10px;
    }}
    .option img {{
      width: 100%;
      display: block;
    }}
    figcaption {{
      margin-top: 6px;
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .05em;
      word-break: break-all;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      color: #f1efe8;
    }}
  </style>
</head>
<body>
  <h1>Ransom Title Generator Preview</h1>
  {''.join(title_blocks)}
</body>
</html>
"""
    PREVIEW_FILE.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate monochrome ransom masthead titles.")
    parser.add_argument(
        "--asset-root",
        type=Path,
        default=ASSET_PACK,
        help="Path to ransom letter pack root.",
    )
    parser.add_argument(
        "--title",
        action="append",
        default=[],
        help='Title spec as "slug=WORDS" (can be repeated). Defaults: residual, first-day, catalog.',
    )
    parser.add_argument(
        "--options-per-title",
        type=int,
        default=4,
        help="How many options to generate per title before auto-selecting the final.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260314,
        help="Base random seed.",
    )
    args = parser.parse_args()

    titles = parse_titles(args.title)
    char_map = discover_asset_map(args.asset_root)
    library = VariantLibrary(char_map)

    manifest: Dict[str, object] = {
        "asset_root": str(args.asset_root.relative_to(ROOT)),
        "seed": args.seed,
        "titles": [],
    }

    for slug, text in titles:
        result = generate_for_title(
            slug=slug,
            text=text,
            library=library,
            options_per_title=max(2, args.options_per_title),
            base_seed=args.seed,
        )
        manifest["titles"].append(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    write_preview(manifest)

    print("Generated titles:")
    for title in manifest["titles"]:
        print(f"  - assets/generated-titles/{title['final_file']}")
    print("Preview:")
    print("  - preview/ransom-titles.html")


if __name__ == "__main__":
    main()
