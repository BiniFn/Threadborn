from __future__ import annotations

from pathlib import Path
from shutil import copy2

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ANDROID_ASSETS = (
    ROOT / "android-app" / "app" / "src" / "main" / "assets" / "site" / "assets"
)

# These match the existing/old canvas sizes used by the site layout.
TARGETS = {
    "header": (1254, 330),
    "wide": (1254, 658),
}

# Crop windows are taken from the new 1254x1254 official logo artwork.
# They preserve the new logo while producing layout-friendly widths like the old assets.
CROPS = {
    "en": {
        "header": (0, 340, 1254, 670),
        "wide": (0, 145, 1254, 803),
    },
    "jp": {
        "header": (0, 340, 1254, 670),
        "wide": (0, 145, 1254, 803),
    },
}


def make_variant(lang: str, variant: str) -> Path:
    source = ASSETS / f"threadborn-logo-{lang}-new.png"
    target = ASSETS / f"threadborn-logo-{lang}-new-{variant}.png"
    size = TARGETS[variant]
    crop_box = CROPS[lang][variant]

    with Image.open(source).convert("RGBA") as image:
        cropped = image.crop(crop_box)
        if cropped.size != size:
            cropped = cropped.resize(size, Image.Resampling.LANCZOS)
        cropped.save(target, optimize=True)

    return target


def main() -> None:
    created: list[Path] = []
    for lang in ("en", "jp"):
        for variant in ("header", "wide"):
            created.append(make_variant(lang, variant))

    ANDROID_ASSETS.mkdir(parents=True, exist_ok=True)
    for path in created:
        copy2(path, ANDROID_ASSETS / path.name)

    for path in created:
        with Image.open(path) as image:
            print(f"{path.relative_to(ROOT)} {image.width}x{image.height}")


if __name__ == "__main__":
    main()
