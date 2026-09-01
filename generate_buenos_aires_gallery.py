from pathlib import Path
import base64
import html
import json
from PIL import Image

BASE = "https://urbanartsnews.com"
UPLOAD_DIR = Path("data/image_uploads")
ASSET_DIR = Path("assets/images/buenos-aires")
RESPONSIVE_DIR = ASSET_DIR / "responsive"
GALLERY_DIR = Path("cities/buenos-aires/gallery")

PHOTOS = [
    {"n": 1, "slug": "historic-pedestrian-street-buenos-aires", "title": "Historic Pedestrian Street in Buenos Aires", "description": "A broad pedestrian street surrounded by ornate historic architecture in central Buenos Aires.", "alt": "Historic buildings along a pedestrian street in Buenos Aires", "width": 1600, "height": 1200},
    {"n": 2, "slug": "central-buenos-aires-city-corner", "title": "Central Buenos Aires City Corner", "description": "A lively central Buenos Aires intersection framed by trees, historic façades and contemporary street life.", "alt": "Central Buenos Aires intersection with historic buildings", "width": 1600, "height": 1066},
    {"n": 3, "slug": "busy-downtown-buenos-aires-avenue", "title": "Busy Downtown Buenos Aires Avenue", "description": "Dense traffic and tall city buildings define a busy avenue through Downtown Buenos Aires.", "alt": "Busy avenue with traffic and tall buildings in Downtown Buenos Aires", "width": 1600, "height": 900},
    {"n": 4, "slug": "colorful-buenos-aires-side-street", "title": "Colourful Side Street in Buenos Aires", "description": "A narrow Buenos Aires street with colourful storefront details and historic urban architecture.", "alt": "Colourful storefront on a narrow Buenos Aires city street", "width": 1600, "height": 1066},
    {"n": 5, "slug": "historic-street-scene-buenos-aires", "title": "Historic Street Scene in Buenos Aires", "description": "Pedestrians cross a sunlit historic street between the dense architectural façades of Buenos Aires.", "alt": "Pedestrians crossing a historic street in Buenos Aires", "width": 1600, "height": 1068},
    {"n": 6, "slug": "obelisk-buenos-aires-city-avenue", "title": "Obelisk of Buenos Aires from a City Avenue", "description": "The Obelisk of Buenos Aires rises above traffic and historic buildings on a central city avenue.", "alt": "Obelisk of Buenos Aires above traffic on a city avenue", "width": 1600, "height": 900},
    {"n": 7, "slug": "buenos-aires-skyline-obelisk-view", "title": "Buenos Aires Skyline and Obelisk View", "description": "An elevated city view across Buenos Aires with the Obelisk standing prominently in the skyline.", "alt": "Buenos Aires skyline and Obelisk viewed from above", "width": 1600, "height": 1178},
    {"n": 8, "slug": "historic-tower-street-buenos-aires", "title": "Historic Tower and Street in Buenos Aires", "description": "A green-domed historic tower anchors a leafy street scene in central Buenos Aires.", "alt": "Historic green-domed tower along a street in Buenos Aires", "width": 1600, "height": 1200},
    {"n": 9, "slug": "avenida-9-de-julio-obelisk-buenos-aires", "title": "Avenida 9 de Julio and the Buenos Aires Obelisk", "description": "The broad Avenida 9 de Julio leads toward the iconic Obelisk in the centre of Buenos Aires.", "alt": "Avenida 9 de Julio leading toward the Obelisk in Buenos Aires", "width": 1600, "height": 1200},
]

SEO_UPDATES = [
    {"title":"Avenida 9 de Julio and Historic Buenos Aires Architecture","description":"A broad pedestrian crossing opens onto Avenida 9 de Julio amid the historic architecture of central Buenos Aires. The generous public space and distant urban landmarks emphasise the monumental scale of the avenue. Urban art introduces a more personal scale to this setting through images and interventions that reflect the city’s diverse communities.","meta_description":"Explore Avenida 9 de Julio, historic architecture and an open pedestrian crossing in central Buenos Aires.","alt":"Avenida 9 de Julio and historic architecture in central Buenos Aires"},
    {"title":"Central Buenos Aires Intersection and Street Life","description":"Trees, historic façades and pedestrians frame a lively intersection in central Buenos Aires. The layered streetscape combines traditional architecture with the movement and visual signals of contemporary city life. Urban art builds on this mixture by turning walls, shutters and public surfaces into spaces for cultural expression.","meta_description":"View a lively central Buenos Aires intersection with trees, historic façades and contemporary street life.","alt":"Central Buenos Aires intersection with trees and historic façades"},
    {"title":"Busy Downtown Buenos Aires Avenue and Obelisk View","description":"Dense traffic fills a Downtown Buenos Aires avenue while the Obelisk appears between tall city buildings in the distance. The compressed perspective captures the intensity, movement and vertical rhythm of the metropolitan centre. Urban art responds to this energy with bold images designed to communicate amid the visual density of the street.","meta_description":"See a busy Downtown Buenos Aires avenue, dense traffic, tall buildings and the distant Obelisk.","alt":"Busy Downtown Buenos Aires avenue with traffic and the distant Obelisk"},
    {"title":"Colourful Storefront on a Buenos Aires Side Street","description":"A vividly painted storefront brings red and green colour to a narrow street lined with historic Buenos Aires architecture. The intimate scene contrasts everyday commercial activity with the decorative character of the surrounding façades. This use of colour shows how urban art and creative design can give an ordinary side street a memorable identity.","meta_description":"Explore a colourful storefront and historic architecture on a narrow side street in Buenos Aires.","alt":"Colourful painted storefront on a narrow Buenos Aires side street"},
    {"title":"Pedestrians on a Sunlit Historic Buenos Aires Street","description":"Pedestrians cross a sunlit street between the dense historic façades of central Buenos Aires. Strong shadows, architectural detail and everyday movement create a cinematic urban composition. Urban art emerges from the same lived environment, recording local experiences and adding contemporary layers to historic neighbourhoods.","meta_description":"View pedestrians crossing a sunlit historic street between dense architectural façades in Buenos Aires.","alt":"Pedestrians crossing a sunlit historic street in Buenos Aires"},
    {"title":"Buenos Aires Obelisk Above a Central City Avenue","description":"The Obelisk of Buenos Aires rises above traffic, buses and ornate buildings on a central avenue. Its clear geometric form acts as a powerful orientation point within the busy metropolitan landscape. Like urban art, the monument demonstrates how a single visual statement can shape collective memory and city identity.","meta_description":"See the Buenos Aires Obelisk rising above traffic and historic buildings on a central city avenue.","alt":"Buenos Aires Obelisk rising above traffic on a central avenue"},
    {"title":"Buenos Aires Skyline and Obelisk from an Elevated View","description":"An elevated terrace overlooks the Buenos Aires skyline with the Obelisk standing prominently among illuminated towers. Roads, high-rise buildings and evening light reveal the scale of the modern city centre. At street level, urban art provides a closer view of the people, stories and neighbourhood identities contained within this panorama.","meta_description":"Explore the Buenos Aires skyline and Obelisk from an elevated city viewpoint in warm evening light.","alt":"Buenos Aires skyline and Obelisk viewed from an elevated terrace"},
    {"title":"Historic Green-Domed Tower on a Buenos Aires Street","description":"A green-domed historic tower anchors a leafy street between the architectural façades of central Buenos Aires. Trees and street-level activity soften the strong vertical lines of the surrounding buildings. Urban art adds another living layer to such historic settings by connecting inherited architecture with contemporary voices.","meta_description":"View a historic green-domed tower, leafy street and central Buenos Aires architecture.","alt":"Historic green-domed tower along a leafy street in central Buenos Aires"},
    {"title":"Avenida 9 de Julio Leading to the Buenos Aires Obelisk","description":"The broad Avenida 9 de Julio leads directly toward the iconic Obelisk in the centre of Buenos Aires. Traffic, signs and surrounding façades create a layered portrait of one of the city’s most recognisable urban corridors. Its scale offers a dramatic context for urban art, public imagery and visual culture across the Argentine capital.","meta_description":"Explore Avenida 9 de Julio leading toward the iconic Buenos Aires Obelisk through the city centre.","alt":"Avenida 9 de Julio leading toward the Obelisk in central Buenos Aires"},
]
for photo, update in zip(PHOTOS, SEO_UPDATES, strict=True):
    photo.update(update)

def esc(value):
    return html.escape(str(value), quote=True)

def link_buenos_aires(value):
    city_link = '<a href="/cities/buenos-aires/" title="Buenos Aires Urban Art"><strong>Buenos Aires</strong></a>'
    return esc(value).replace("Buenos Aires", city_link)

def decode_staged_images():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for photo in PHOTOS:
        staged = UPLOAD_DIR / f"buenos-aires-{photo['n']}.jpg.b64"
        target = ASSET_DIR / f"{photo['slug']}.jpg"
        if staged.exists():
            target.write_bytes(base64.b64decode(staged.read_text(encoding="utf-8")))
            staged.unlink()
            print(f"IMPORT Buenos Aires image: {target}")

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
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/cities/buenos-aires/">Buenos Aires</a><a href="/urban-art-cities/">Cities</a><a href="/artists/">Artists</a><a href="/subscribe/">Subscribe</a></nav></header>"""

def footer():
    return '<footer>© 2026 Urban Arts News · <a href="/cities/buenos-aires/" title="Buenos Aires Urban Art"><strong>Buenos Aires</strong></a> Urban Art · City Photography</footer></body></html>'

def generate_detail(photo):
    slug = photo["slug"]
    canonical = f"{BASE}/cities/buenos-aires/gallery/{slug}/"
    image = f"{BASE}/assets/images/buenos-aires/{slug}.jpg"
    description = photo["meta_description"]
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":photo["title"],"description":description,"primaryImageOfPage":{"@id":canonical+"#image"}},
        {"@type":"ImageObject","@id":canonical+"#image","name":photo["title"],"description":description,"caption":photo["description"],"contentUrl":image,"url":canonical,"encodingFormat":"image/jpeg","width":{"@type":"QuantitativeValue","value":photo["width"],"unitCode":"E37"},"height":{"@type":"QuantitativeValue","value":photo["height"],"unitCode":"E37"},"contentLocation":{"@type":"Place","name":"Buenos Aires, Argentina"},"creditText":"Pexels contributor via Pexels","copyrightNotice":"Used under the Pexels License; rights remain with the respective contributor","representativeOfPage":True,"keywords":["Buenos Aires Urban Art News","Urban Art Buenos Aires","Buenos Aires City Photography","Urban Arts News"]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Buenos Aires","item":BASE+"/cities/buenos-aires/"},{"@type":"ListItem","position":3,"name":"Buenos Aires Gallery","item":BASE+"/cities/buenos-aires/gallery/"},{"@type":"ListItem","position":4,"name":photo["title"],"item":canonical}]}
    ]}
    markup = head(photo["title"]+" | Buenos Aires Urban Arts News", description, canonical, image, photo["width"], photo["height"], schema)
    markup += f"""<main class="container"><article class="photo">
<picture><source type="image/webp" media="(max-width:600px)" srcset="/assets/images/buenos-aires/responsive/{slug}-480.webp"><source type="image/webp" media="(max-width:1100px)" srcset="/assets/images/buenos-aires/responsive/{slug}-960.webp"><img src="/assets/images/buenos-aires/{slug}.jpg" alt="{esc(photo['alt'])}" width="{photo['width']}" height="{photo['height']}" loading="eager" fetchpriority="high" decoding="async"></picture>
<div class="caption"><h1>{esc(photo['title'])}</h1><p>{esc(photo['description'])}</p>
<p><strong><a href="https://urbanartsnews.com/cities/buenos-aires/">Buenos Aires Urban Art News</a></strong> presents this photograph as part of its visual documentation of <strong><a href="https://urbanartsnews.com/cities/buenos-aires/">Urban Art Buenos Aires</a></strong>, city culture and the changing metropolitan landscape.</p>
<p>Discover more urban photography, contemporary artists and city culture on <a href="https://urbanartsnews.com/"><strong>Urban Arts News</strong></a>.</p>
<p class="credit">Photo via <a href="https://www.pexels.com/"><strong>Pexels</strong></a>, used under the <a href="https://www.pexels.com/license/">Pexels License</a>. Rights remain with the respective contributor.</p>
<a class="button" href="/cities/buenos-aires/gallery/">Buenos Aires Gallery</a><a class="button" href="/cities/buenos-aires/">Buenos Aires Urban Art</a>
</div></article></main>""" + footer()
    out = GALLERY_DIR / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(markup, encoding="utf-8")

def generate_gallery():
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    hero = PHOTOS[3]
    canonical = BASE + "/cities/buenos-aires/gallery/"
    image = BASE + f"/assets/images/buenos-aires/{hero['slug']}.jpg"
    description = "Explore nine original Buenos Aires photographs featuring historic streets, Downtown avenues, the Obelisk and city skyline views on Urban Arts News."
    item_list = [{"@type":"ListItem","position":i+1,"url":BASE+f"/cities/buenos-aires/gallery/{p['slug']}/","name":p["title"]} for i,p in enumerate(PHOTOS)]
    schema={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,"name":"Buenos Aires Urban Photography Gallery","description":description,"mainEntity":{"@type":"ItemList","numberOfItems":9,"itemListElement":item_list}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Buenos Aires","item":BASE+"/cities/buenos-aires/"},{"@type":"ListItem","position":3,"name":"Buenos Aires Gallery","item":canonical}]}]}
    cards=""
    for i,p in enumerate(PHOTOS):
        attrs='loading="eager" fetchpriority="high"' if i==0 else 'loading="lazy"'
        cards += f"""<article class="card"><a href="/cities/buenos-aires/gallery/{p['slug']}/"><picture><source type="image/webp" srcset="/assets/images/buenos-aires/responsive/{p['slug']}-480.webp 480w, /assets/images/buenos-aires/responsive/{p['slug']}-960.webp 960w" sizes="(max-width:800px) 92vw, 30vw"><img src="/assets/images/buenos-aires/{p['slug']}.jpg" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {attrs} decoding="async"></picture></a><div class="card-content"><h2>{link_buenos_aires(p['title'])}</h2><p>{link_buenos_aires(p['description'])}</p><a href="/cities/buenos-aires/gallery/{p['slug']}/">View photograph →</a></div></article>"""
    markup=head("Buenos Aires Urban Photography Gallery | Urban Arts News",description,canonical,image,hero["width"],hero["height"],schema)
    markup+=f"""<section class="hero"><small>Urban Arts News · {link_buenos_aires('Buenos Aires')} Gallery</small><h1>{link_buenos_aires('Buenos Aires')} <span class="accent">City Gallery</span></h1><p>{link_buenos_aires('Nine original photographs documenting historic streets, central avenues, the Obelisk and the visual identity surrounding Urban Art Buenos Aires.')}</p></section><main class="container"><h2>{link_buenos_aires('Buenos Aires Urban Art News and City Photography')}</h2><p>{link_buenos_aires('This curated gallery connects Buenos Aires city photography with the wider Urban Arts News archive. Each photograph has its own indexable page, descriptive metadata and links to the Buenos Aires urban-art directory.')}</p><div class="grid">{cards}</div></main>"""+footer()
    (GALLERY_DIR/"index.html").write_text(markup,encoding="utf-8")

def patch_city_page():
    path=Path("cities/buenos-aires/index.html")
    if not path.exists(): return
    text=path.read_text(encoding="utf-8")
    marker="/cities/buenos-aires/gallery/"
    if marker not in text:
        block='''<section class="related"><h2>Buenos Aires City Photography Gallery</h2><p>Explore nine original photographs of historic streets, Downtown avenues, the Obelisk and Buenos Aires city views.</p><a class="button" href="/cities/buenos-aires/gallery/">Explore Buenos Aires Gallery →</a></section>'''
        text=text.replace("</main>",block+"</main>")
        path.write_text(text,encoding="utf-8")

def update_sitemap():
    path=Path("sitemap.xml")
    text=path.read_text(encoding="utf-8")
    urls=[BASE+"/cities/buenos-aires/gallery/"]+[BASE+f"/cities/buenos-aires/gallery/{p['slug']}/" for p in PHOTOS]
    additions=""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions+=f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    text=text.replace("</urlset>",additions+"</urlset>")
    path.write_text(text,encoding="utf-8")

def image_sitemap():
    rows=[]
    for p in PHOTOS:
        page=BASE+f"/cities/buenos-aires/gallery/{p['slug']}/"
        image=BASE+f"/assets/images/buenos-aires/{p['slug']}.jpg"
        rows.append(f"  <url><loc>{page}</loc><image:image><image:loc>{image}</image:loc></image:image></url>")
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+"\n".join(rows)+"\n</urlset>\n"
    Path("image-sitemap-buenos-aires.xml").write_text(xml,encoding="utf-8")
    robots=Path("robots.txt")
    content=robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    line=f"Sitemap: {BASE}/image-sitemap-buenos-aires.xml"
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
    print("DONE Buenos Aires gallery: 9 photographs")

if __name__=="__main__":
    main()
