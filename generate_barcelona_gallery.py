from pathlib import Path
import base64
import html
import json
import unicodedata
from PIL import Image, ImageDraw, ImageFont

BASE = "https://urbanartsnews.com"
UPLOAD_DIR = Path("data/image_uploads")
ASSET_DIR = Path("assets/images/barcelona")
RESPONSIVE_DIR = ASSET_DIR / "responsive"
GALLERY_DIR = Path("cities/barcelona/gallery")

PHOTOS = [
    {"n": 1, "slug": "park-guell-mosaic-view-barcelona", "title": "Park Güell Mosaic Architecture and Panoramic Barcelona View", "description": "A panoramic view across Barcelona framed by the colourful mosaic architecture of Antoni Gaudí’s Park Güell. The photograph brings together one of the city’s most recognisable Modernist landmarks with Barcelona’s dense urban landscape, distant hills and Mediterranean atmosphere.", "alt": "Park Güell mosaic architecture framing a panoramic view across Barcelona", "portal_note": "Discover more street art, urban photography and contemporary artists on", "width": 1600, "height": 1066},
    {"n": 2, "slug": "barcelona-cathedral-gothic-quarter", "title": "Barcelona Cathedral in the Gothic Quarter", "description": "Barcelona Cathedral and its historic square in the heart of the Gothic Quarter.", "alt": "Barcelona Cathedral and square in the Gothic Quarter", "width": 1600, "height": 1280},
    {"n": 3, "slug": "sagrada-familia-barcelona-park-view", "title": "Sagrada Família from a Barcelona Park", "description": "The towers of the Sagrada Família rising above trees and a reflective pond in Barcelona.", "alt": "Sagrada Família viewed across a park and pond in Barcelona", "width": 1600, "height": 1200},
    {"n": 4, "slug": "barcelona-waterfront-w-hotel", "title": "Barcelona Waterfront and W Hotel", "description": "The Barcelona marina and distinctive W Hotel beside the Mediterranean waterfront.", "alt": "Barcelona marina and W Hotel on the waterfront", "width": 1600, "height": 1067},
    {"n": 5, "slug": "barcelona-skyline-mediterranean", "title": "Barcelona Skyline from the Mediterranean", "description": "A broad view of Barcelona's waterfront skyline, hills and city architecture from the sea.", "alt": "Barcelona waterfront skyline viewed from the Mediterranean Sea", "width": 1600, "height": 1066},
    {"n": 6, "slug": "barcelona-panoramic-city-view", "title": "Panoramic City View over Barcelona", "description": "Barcelona's dense cityscape and surrounding hills seen from a green elevated viewpoint.", "alt": "Panoramic Barcelona cityscape and hills from above", "width": 1600, "height": 900},
    {"n": 7, "slug": "park-guell-barcelona-sunset", "title": "Park Güell and Barcelona at Sunset", "description": "Gaudí's Park Güell architecture and the Barcelona skyline beneath a colourful sunset.", "alt": "Park Güell architecture and Barcelona skyline at sunset", "width": 1600, "height": 1059},
    {"n": 8, "slug": "gaudi-mosaic-window-barcelona-view", "title": "Gaudí Mosaic Window with Barcelona View", "description": "A Barcelona city view framed by a stone opening and colourful Gaudí-inspired mosaic details.", "alt": "Barcelona viewed through a stone window with colourful mosaic details", "width": 1600, "height": 1066},
    {"n": 9, "slug": "historic-central-barcelona-street", "title": "Historic Architecture in Central Barcelona", "description": "A central Barcelona avenue lined with ornate historic buildings and active city traffic.", "alt": "Historic buildings along a central Barcelona city street", "width": 1600, "height": 1200},
]

WATERMARK = "urbanartsnews.com"
FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
)

def esc(value):
    return html.escape(str(value), quote=True)

def watermark_image(image):
    """Return an RGB image with a legible, unobtrusive brand watermark."""
    image = image.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_size = max(18, round(image.width * 0.022))
    font_path = next((path for path in FONT_CANDIDATES if Path(path).exists()), None)
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    bbox = draw.textbbox((0, 0), WATERMARK, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = round(font_size * 0.62), round(font_size * 0.42)
    margin = max(14, round(image.width * 0.018))
    right = image.width - margin
    bottom = image.height - margin
    left = right - text_width - 2 * pad_x
    top = bottom - text_height - 2 * pad_y
    radius = max(8, round(font_size * 0.38))
    draw.rounded_rectangle((left, top, right, bottom), radius=radius, fill=(0, 0, 0, 145))
    draw.text((left + pad_x, top + pad_y - bbox[1]), WATERMARK, font=font, fill=(255, 255, 255, 225))
    return Image.alpha_composite(image, overlay).convert("RGB")

def seo_exif(photo):
    """Create embedded JPEG metadata that describes the photograph accurately."""
    exif = Image.Exif()
    keywords = "Barcelona; Urban Art; Barcelona Photography; Urban Arts News; Spain"
    full_description = f"{photo['title']}. {photo['description']}"
    ascii_description = unicodedata.normalize("NFKD", full_description).encode("ascii", "ignore").decode("ascii")
    exif[270] = ascii_description
    exif[315] = "Urban Arts News"
    exif[33432] = "Copyright Urban Arts News / respective copyright holder"
    exif[40091] = (photo["title"] + "\0").encode("utf-16le")
    exif[40092] = (full_description + "\0").encode("utf-16le")
    exif[40094] = (keywords + "\0").encode("utf-16le")
    return exif

def prepare_original(source, photo):
    """Apply watermark and SEO metadata once to a newly imported original."""
    with Image.open(source) as original:
        branded = watermark_image(original)
        branded.save(source, "JPEG", quality=88, optimize=True, progressive=True, exif=seo_exif(photo))

def decode_staged_images():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for photo in PHOTOS:
        staged = UPLOAD_DIR / f"barcelona-{photo['n']}.jpg.b64"
        target = ASSET_DIR / f"{photo['slug']}.jpg"
        if staged.exists():
            target.write_bytes(base64.b64decode(staged.read_text(encoding="utf-8")))
            prepare_original(target, photo)
            staged.unlink()
            print(f"IMPORT Barcelona image: {target}")

def responsive_images():
    RESPONSIVE_DIR.mkdir(parents=True, exist_ok=True)
    for photo in PHOTOS:
        source = ASSET_DIR / f"{photo['slug']}.jpg"
        with Image.open(source) as original:
            image = original.convert("RGB")
            photo["width"], photo["height"] = image.size
            for width in (480, 960):
                height = round(image.height * width / image.width)
                resized = image.resize((width, height), Image.Resampling.LANCZOS)
                output = RESPONSIVE_DIR / f"{photo['slug']}-{width}.webp"
                resized.save(output, "WEBP", quality=82, method=6)

def head(title, description, canonical, image, image_width, image_height, schema):
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#090909">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website"><meta property="og:url" content="{esc(canonical)}">
<meta property="og:site_name" content="Urban Arts News"><meta property="og:locale" content="en_US">
<meta property="og:image" content="{esc(image)}"><meta property="og:image:secure_url" content="{esc(image)}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="{image_width}">
<meta property="og:image:height" content="{image_height}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{esc(image)}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')}</script>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f5f5;color:#171717;font-family:Arial,Helvetica,sans-serif;line-height:1.6}}a{{color:inherit;text-decoration:none}}header{{background:#090909;color:#fff;padding:18px 5%;display:flex;justify-content:space-between;align-items:center}}.logo{{font-size:28px;font-weight:900;letter-spacing:-1px}}.logo span,.accent{{color:#ff5b21}}nav a{{margin-left:18px;font-size:13px;font-weight:800;text-transform:uppercase}}.hero{{background:#111;color:#fff;padding:75px 6%}}.hero small{{color:#ff5b21;font-weight:900;text-transform:uppercase}}.hero h1{{font-size:clamp(44px,7vw,82px);line-height:.96;letter-spacing:-3px;text-transform:uppercase;margin:12px 0 20px}}.hero p{{max-width:850px;color:#ccc;font-size:19px}}.container{{width:min(1320px,92%);margin:50px auto}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:25px}}.card,.photo{{background:#fff;box-shadow:0 6px 20px rgba(0,0,0,.09)}}.card img{{display:block;width:100%;height:330px;object-fit:cover}}.card-content,.caption{{padding:22px}}.card h2{{font-size:20px;line-height:1.25;margin:0 0 8px}}.card p,.caption p{{color:#555}}.photo{{padding:clamp(14px,4vw,42px)}}.photo img{{display:block;max-width:100%;height:auto;margin:auto}}.caption{{max-width:940px;margin:auto}}.caption h1{{font-size:clamp(30px,5vw,52px);line-height:1.05}}.button{{display:inline-block;background:#ff5b21;color:#fff;padding:13px 18px;font-weight:900;text-transform:uppercase;margin:10px 8px 0 0}}.credit{{font-size:13px;color:#777;border-top:1px solid #ddd;padding-top:14px}}footer{{background:#090909;color:#888;text-align:center;padding:35px;margin-top:60px}}@media(max-width:800px){{header{{display:block}}nav{{margin-top:12px}}nav a{{margin:0 12px 0 0}}.grid{{grid-template-columns:1fr}}.card img{{height:auto}}.hero{{padding:55px 6%}}}}
</style></head><body>
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/urban-art-city/barcelona/spain/">Barcelona</a><a href="/urban-art-cities/">Cities</a><a href="/artists/">Artists</a><a href="/subscribe/">Subscribe</a></nav></header>"""

def footer():
    return '<footer>© 2026 Urban Arts News · Barcelona Urban Art · City Photography</footer></body></html>'

def generate_detail(photo):
    slug = photo["slug"]
    canonical = f"{BASE}/cities/barcelona/gallery/{slug}/"
    image = f"{BASE}/assets/images/barcelona/{slug}.jpg"
    description = f"Barcelona Urban Art News: {photo['description']} Explore Urban Art Barcelona and city photography on Urban Arts News."
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":photo["title"],"description":description,"primaryImageOfPage":{"@id":canonical+"#image"}},
        {"@type":"ImageObject","@id":canonical+"#image","name":photo["title"],"description":description,"caption":photo["description"],"contentUrl":image,"url":canonical,"encodingFormat":"image/jpeg","width":{"@type":"QuantitativeValue","value":photo["width"],"unitCode":"E37"},"height":{"@type":"QuantitativeValue","value":photo["height"],"unitCode":"E37"},"contentLocation":{"@type":"Place","name":"Barcelona, Catalonia, Spain"},"creditText":"Urban Arts News Barcelona Gallery","copyrightNotice":"All rights reserved by the respective copyright holder","representativeOfPage":True,"keywords":["Barcelona Urban Art News","Urban Art Barcelona","Barcelona City Photography","Urban Arts News"]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Barcelona","item":BASE+"/cities/barcelona/"},{"@type":"ListItem","position":3,"name":"Barcelona Gallery","item":BASE+"/cities/barcelona/gallery/"},{"@type":"ListItem","position":4,"name":photo["title"],"item":canonical}]}
    ]}
    markup = head(photo["title"]+" | Barcelona Urban Arts News", description, canonical, image, photo["width"], photo["height"], schema)
    markup += f"""<main class="container"><article class="photo">
<picture><source type="image/webp" media="(max-width:600px)" srcset="/assets/images/barcelona/responsive/{slug}-480.webp"><source type="image/webp" media="(max-width:1100px)" srcset="/assets/images/barcelona/responsive/{slug}-960.webp"><img src="/assets/images/barcelona/{slug}.jpg" alt="{esc(photo['alt'])}" width="{photo['width']}" height="{photo['height']}" loading="eager" fetchpriority="high" decoding="async"></picture>
<div class="caption"><h1>{esc(photo['title'])}</h1><p>{esc(photo['description'])}</p>
<p><strong><a href="https://urbanartsnews.com/urban-art-city/barcelona/spain/">Barcelona Urban Art News</a></strong> presents this photograph as part of its visual documentation of <strong><a href="https://urbanartsnews.com/urban-art-city/barcelona/spain/">Urban Art Barcelona</a></strong>, city culture and the changing metropolitan landscape.</p>
{f'<p>{esc(photo["portal_note"])} <a href="https://urbanartsnews.com/"><strong>Urban Arts News</strong></a>.</p>' if photo.get('portal_note') else ''}
<p class="credit">Photograph supplied for publication to Urban Arts News. Rights remain with the respective copyright holder.</p>
<a class="button" href="/cities/barcelona/gallery/">Barcelona Gallery</a><a class="button" href="/urban-art-city/barcelona/spain/">Barcelona Urban Art</a>
</div></article></main>""" + footer()
    out = GALLERY_DIR / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(markup, encoding="utf-8")

def generate_gallery():
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    hero = PHOTOS[3]
    canonical = BASE + "/cities/barcelona/gallery/"
    image = BASE + f"/assets/images/barcelona/{hero['slug']}.jpg"
    description = "Explore nine original Barcelona photographs featuring Park Güell, the Gothic Quarter, Sagrada Família, the waterfront and city views on Urban Arts News."
    item_list = [{"@type":"ListItem","position":i+1,"url":BASE+f"/cities/barcelona/gallery/{p['slug']}/","name":p["title"]} for i,p in enumerate(PHOTOS)]
    schema={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,"name":"Barcelona Urban Photography Gallery","description":description,"mainEntity":{"@type":"ItemList","numberOfItems":9,"itemListElement":item_list}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Barcelona","item":BASE+"/cities/barcelona/"},{"@type":"ListItem","position":3,"name":"Barcelona Gallery","item":canonical}]}]}
    cards=""
    for i,p in enumerate(PHOTOS):
        attrs='loading="eager" fetchpriority="high"' if i==0 else 'loading="lazy"'
        cards += f"""<article class="card"><a href="/cities/barcelona/gallery/{p['slug']}/"><picture><source type="image/webp" srcset="/assets/images/barcelona/responsive/{p['slug']}-480.webp 480w, /assets/images/barcelona/responsive/{p['slug']}-960.webp 960w" sizes="(max-width:800px) 92vw, 30vw"><img src="/assets/images/barcelona/{p['slug']}.jpg" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {attrs} decoding="async"></picture></a><div class="card-content"><h2><a href="/cities/barcelona/gallery/{p['slug']}/">{esc(p['title'])}</a></h2><p>{esc(p['description'])}</p></div></article>"""
    markup=head("Barcelona Urban Photography Gallery | Urban Arts News",description,canonical,image,hero["width"],hero["height"],schema)
    markup+=f"""<section class="hero"><small>Urban Arts News · Barcelona Gallery</small><h1>Barcelona <span class="accent">City Gallery</span></h1><p>Nine original photographs documenting Park Güell, the Gothic Quarter, Sagrada Família, the waterfront and the visual identity surrounding Urban Art Barcelona.</p></section><main class="container"><h2>Barcelona Urban Art News and City Photography</h2><p>This curated gallery connects Barcelona city photography with the wider Urban Arts News archive. Each photograph has its own indexable page, descriptive metadata and links to the Barcelona urban-art directory.</p><div class="grid">{cards}</div></main>"""+footer()
    (GALLERY_DIR/"index.html").write_text(markup,encoding="utf-8")

def patch_city_page():
    path=Path("cities/barcelona/index.html")
    if not path.exists(): return
    text=path.read_text(encoding="utf-8")
    marker="/cities/barcelona/gallery/"
    if marker not in text:
        block='''<section class="related"><h2>Barcelona City Photography Gallery</h2><p>Explore nine original photographs of Park Güell, the Gothic Quarter, Sagrada Família, the waterfront and Barcelona city views.</p><a class="button" href="/cities/barcelona/gallery/">Explore Barcelona Gallery →</a></section>'''
        text=text.replace("</main>",block+"</main>")
        path.write_text(text,encoding="utf-8")

def update_sitemap():
    path=Path("sitemap.xml")
    text=path.read_text(encoding="utf-8")
    urls=[BASE+"/cities/barcelona/gallery/"]+[BASE+f"/cities/barcelona/gallery/{p['slug']}/" for p in PHOTOS]
    additions=""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions+=f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    text=text.replace("</urlset>",additions+"</urlset>")
    path.write_text(text,encoding="utf-8")

def image_sitemap():
    rows=[]
    for p in PHOTOS:
        page=BASE+f"/cities/barcelona/gallery/{p['slug']}/"
        image=BASE+f"/assets/images/barcelona/{p['slug']}.jpg"
        rows.append(f"  <url><loc>{page}</loc><image:image><image:loc>{image}</image:loc></image:image></url>")
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+"\n".join(rows)+"\n</urlset>\n"
    Path("image-sitemap-barcelona.xml").write_text(xml,encoding="utf-8")
    robots=Path("robots.txt")
    content=robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    line=f"Sitemap: {BASE}/image-sitemap-barcelona.xml"
    if line not in content:
        content=content.rstrip()+"\n"+line+"\n"
        robots.write_text(content,encoding="utf-8")

def main():
    decode_staged_images()
    responsive_images()
    for photo in PHOTOS: generate_detail(photo)
    generate_gallery()
    patch_city_page()
    update_sitemap()
    image_sitemap()
    print("DONE Barcelona gallery: 9 photographs")

if __name__=="__main__":
    main()
