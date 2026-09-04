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

def square_photo(source):
    with Image.open(source) as original:
        image = original.convert("RGB")
    scale = max(630 / image.width, 630 / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (image.width - 630) // 2)
    top = max(0, (image.height - 630) // 2)
    image = image.crop((left, top, left + 630, top + 630))
    return ImageEnhance.Color(image).enhance(1.08)

def fit_text(draw, text, max_width, start_size, min_size=34):
    size = start_size
    while size > min_size:
        selected = font(FONT_BOLD, size)
        if draw.textbbox((0, 0), text, font=selected)[2] <= max_width:
            return selected
        size -= 2
    return font(FONT_BOLD, min_size)

def make_card(artist):
    slug = artist["slug"]
    source = SPECIAL.get(slug, GENERIC)
    if not source.exists():
        source = GENERIC

    card = Image.new("RGB", (1200, 630), (250, 249, 247))
    card.paste(square_photo(source), (0, 0))
    draw = ImageDraw.Draw(card)
    orange = (255, 91, 33)
    dark = (16, 16, 16)
    grey = (79, 79, 79)

    draw.rectangle((630, 0, 1200, 18), fill=orange)
    draw.text((680, 70), "URBAN ARTS NEWS", font=font(FONT_BOLD, 27), fill=orange)
    name = artist["name"].upper()
    name_font = fit_text(draw, name, 465, 61)
    draw.text((680, 155), name, font=name_font, fill=dark)
    city = f'{artist.get("city", "")}, {artist.get("country", "")}'.strip(", ")
    draw.text((682, 285), "URBAN ARTIST", font=font(FONT_BOLD, 23), fill=grey)
    draw.text((682, 332), city, font=font(FONT_REGULAR, 27), fill=dark)
    draw.line((682, 407, 1138, 407), fill=(205, 205, 205), width=2)
    draw.text((682, 451), "Discover the artist profile", font=font(FONT_REGULAR, 23), fill=grey)
    draw.text((682, 512), "UrbanArtsNews.com", font=font(FONT_BOLD, 27), fill=orange)

    output = OUT / f"{slug}-whatsapp-preview-v2.jpg"
    output.parent.mkdir(parents=True, exist_ok=True)
    card.save(output, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"OG card: {output}")

def main():
    artists = json.loads(DATA.read_text(encoding="utf-8"))
    for artist in artists:
        make_card(artist)
    print(f"Generated {len(artists)} desktop-safe artist social preview cards.")

if __name__ == "__main__":
    main()
