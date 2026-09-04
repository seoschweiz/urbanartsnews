#!/usr/bin/env python3
"""Create bright, correctly cropped Open Graph cards for artist profiles."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "images" / "social" / "artists"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CITY_IMAGES = {
    "Badalona": ROOT / "assets/images/badalona/pont-del-petroli-sunset-badalona.jpg",
    "Buenos Aires": ROOT / "assets/images/buenos-aires/colorful-buenos-aires-side-street.jpg",
    "Los Angeles": ROOT / "assets/images/los-angeles/los-angeles-skyline-sunset-view.jpg",
    "Ontario, California": ROOT / "assets/images/los-angeles/downtown-los-angeles-night-reflections.jpg",
    "Venice": ROOT / "assets/images/urban-art-gallery-news/colourful-art-editions-gallery-display.jpg",
}
DEFAULT_IMAGE = ROOT / "assets/images/barcelona/park-guell-mosaic-public-art.jpg"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def artist_photo(artist):
    folder = ROOT / "assets" / "images" / artist["slug"]
    photos = sorted(folder.glob("*.jpg")) if folder.exists() else []
    return photos[0] if photos else CITY_IMAGES.get(artist["city"], DEFAULT_IMAGE)


def fit_name(draw, name, max_width):
    size = 74
    while size > 42:
        candidate = font(size, bold=True)
        if draw.textbbox((0, 0), name, font=candidate)[2] <= max_width:
            return candidate
        size -= 2
    return font(42, bold=True)


def create_card(artist):
    source = Image.open(artist_photo(artist)).convert("RGB")
    source = ImageOps.fit(source, (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    source = ImageEnhance.Brightness(source).enhance(1.08)
    canvas = source.copy()

    # A translucent light panel keeps every card bright and readable in WhatsApp.
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 700, 630), fill=(255, 255, 255, 242))
    od.rectangle((0, 0, 18, 630), fill=(255, 91, 33, 255))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(canvas)

    draw.text((68, 58), "URBAN ARTS NEWS", font=font(29, bold=True), fill="#ff5b21")
    draw.text((68, 160), "ARTIST PROFILE", font=font(22, bold=True), fill="#505050")
    name_font = fit_name(draw, artist["name"].upper(), 575)
    draw.multiline_text((68, 205), artist["name"].upper(), font=name_font, fill="#111111", spacing=4)
    draw.line((68, 445, 590, 445), fill="#ff5b21", width=7)
    draw.text((68, 478), f'{artist["city"]} · {artist["country"]}', font=font(26), fill="#333333")
    draw.text((68, 555), "urbanartsnews.com", font=font(23, bold=True), fill="#111111")

    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / f'{artist["slug"]}.jpg', "JPEG", quality=91, optimize=True, progressive=True)


def main():
    artists = json.loads((ROOT / "data/artists.json").read_text(encoding="utf-8"))
    for artist in artists:
        create_card(artist)
    print(f"Created {len(artists)} artist share cards in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
