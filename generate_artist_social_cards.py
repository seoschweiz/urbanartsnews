from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

OUT = Path("assets/images/social")
DATA = Path("data/artists.json")
GENERIC = Path("assets/images/urban-art-gallery-news/colourful-art-editions-gallery-display.jpg")
SPECIAL = {
    "art-is-trash": Path("assets/images/art-is-trash/mattress-chair-street-art-barcelona.jpg"),
    "ashwan": Path("assets/images/ashwan/ashwan-gold-black-letter-sculpture.jpg"),
}
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

def cover(source):
    with Image.open(source) as original:
        image = original.convert("RGB")
    scale = max(1200 / image.width, 630 / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (image.width - 1200) // 2)
    top = max(0, (image.height - 630) // 2)
    image = image.crop((left, top, left + 1200, top + 630))
    return ImageEnhance.Color(image).enhance(1.08)

def fit_text(draw, text, max_width, start_size, min_size=34):
    size = start_size
    while size > min_size:
        f = font(FONT_BOLD, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
        size -= 2
    return font(FONT_BOLD, min_size)

def make_card(artist):
    slug = artist["slug"]
    source = SPECIAL.get(slug, GENERIC)
    if not source.exists():
        source = GENERIC
    image = cover(source).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1200, 630), fill=(6, 6, 6, 70))
    od.rounded_rectangle((50, 54, 820, 576), radius=28, fill=(255, 255, 255, 238))
    od.rectangle((50, 54, 68, 576), fill=(255, 91, 33, 255))
    image = Image.alpha_composite(image, overlay)
    draw = ImageDraw.Draw(image)
    orange = (255, 91, 33, 255)
    dark = (16, 16, 16, 255)
    grey = (70, 70, 70, 255)
    draw.text((98, 96), "URBAN ARTS NEWS", font=font(FONT_BOLD, 31), fill=orange)
    name = artist["name"].upper()
    name_font = fit_text(draw, name, 650, 76)
    draw.text((98, 170), name, font=name_font, fill=dark)
    city = f'{artist.get("city", "")}, {artist.get("country", "")}'.strip(", ")
    draw.text((100, 285), "URBAN ARTIST", font=font(FONT_BOLD, 27), fill=grey)
    draw.text((100, 332), city, font=font(FONT_REGULAR, 31), fill=dark)
    draw.line((100, 408, 740, 408), fill=(210, 210, 210, 255), width=2)
    draw.text((100, 447), "Discover the artist profile", font=font(FONT_REGULAR, 27), fill=grey)
    draw.text((100, 500), "UrbanArtsNews.com", font=font(FONT_BOLD, 30), fill=orange)
    output = OUT / f"{slug}-whatsapp-preview.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"OG card: {output}")

def main():
    artists = json.loads(DATA.read_text(encoding="utf-8"))
    for artist in artists:
        make_card(artist)
    print(f"Generated {len(artists)} artist social preview cards.")

if __name__ == "__main__":
    main()
