from pathlib import Path
from PIL import Image

SOURCE_DIR = Path("assets/images/art-is-trash")
OUTPUT_DIR = SOURCE_DIR / "responsive"
WIDTHS = (480, 960)
QUALITY = 82

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for source in sorted(SOURCE_DIR.glob("*.jpg")):
    with Image.open(source) as image:
        image = image.convert("RGB")
        for width in WIDTHS:
            if image.width <= width:
                resized = image.copy()
            else:
                height = round(image.height * width / image.width)
                resized = image.resize((width, height), Image.Resampling.LANCZOS)
            output = OUTPUT_DIR / f"{source.stem}-{width}.webp"
            resized.save(output, "WEBP", quality=QUALITY, method=6)
            print(f"UPDATE responsive image: {output} ({resized.width}x{resized.height})")
