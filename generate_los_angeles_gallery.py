from pathlib import Path
import base64
import html
import json
from PIL import Image

BASE = "https://urbanartsnews.com"
UPLOAD_DIR = Path("data/image_uploads")
ASSET_DIR = Path("assets/images/los-angeles")
RESPONSIVE_DIR = ASSET_DIR / "responsive"
GALLERY_DIR = Path("cities/los-angeles/gallery")

PHOTOS = [
    {"n": 1, "slug": "hollywood-sign-sunset-los-angeles", "title": "Hollywood Sign and Communications Tower at Sunset", "description": "The Hollywood Sign and neighbouring communications tower form a dramatic silhouette above the Los Angeles hills as the evening sky turns amber and gold. The image connects one of California’s best-known landmarks with the broadcasting infrastructure that shares its ridgeline.", "meta_description": "Explore the Hollywood Sign and communications tower silhouetted above the Los Angeles hills at sunset in this Urban Arts News photograph.", "alt": "Hollywood Sign and communications tower silhouetted against an amber Los Angeles sunset", "width": 1800, "height": 1079},
    {"n": 2, "slug": "hollywood-sign-hills-los-angeles", "title": "Hollywood Sign Framed by Greenery in the Los Angeles Hills", "description": "The white Hollywood letters emerge between layers of green foliage on a clear Los Angeles day. Framing the distant landmark with trees gives this familiar view of the Hollywood Hills a quieter, more natural perspective.", "meta_description": "View the Hollywood Sign framed by green trees in the Los Angeles hills in this detailed daytime photograph from Urban Arts News.", "alt": "Hollywood Sign emerging between green trees in the Los Angeles hills", "width": 1800, "height": 1178},
    {"n": 3, "slug": "downtown-los-angeles-night-skyline", "title": "Downtown Los Angeles Skyline Across the City at Night", "description": "Downtown Los Angeles glows in the distance while countless street and building lights spread across the metropolitan landscape. The elevated night view reveals the immense scale of the city and the concentrated vertical profile of its illuminated centre.", "meta_description": "See the illuminated Downtown Los Angeles skyline rising beyond a vast field of city lights in this panoramic night photograph.", "alt": "Downtown Los Angeles skyline glowing beyond an expansive field of city lights at night", "width": 1800, "height": 1201},
    {"n": 4, "slug": "los-angeles-skyline-sunset-view", "title": "Panoramic Los Angeles Skyline Beneath a Pastel Sunset", "description": "A broad panorama stretches from the rugged foreground hills across the Los Angeles basin to the distant Downtown skyline. Soft pink clouds and warm evening light give the dense urban landscape an atmospheric, almost dreamlike appearance.", "meta_description": "Explore a panoramic Los Angeles cityscape with the Downtown skyline, foreground hills and a soft pastel sunset sky.", "alt": "Panoramic Los Angeles cityscape and Downtown skyline beneath a pastel sunset", "width": 1800, "height": 1200},
    {"n": 5, "slug": "hollywood-sign-radio-towers", "title": "Hollywood Sign and Radio Towers Under a Clear Blue Sky", "description": "The Hollywood Sign stretches across the dry hillside beneath a bright blue Southern California sky. Radio and communications towers rise above the ridge, revealing the working infrastructure surrounding one of Los Angeles’ most recognisable cultural symbols.", "meta_description": "Discover the Hollywood Sign, dry hillside and radio towers beneath a clear blue Los Angeles sky in this city photograph.", "alt": "Hollywood Sign and radio towers on a dry hillside beneath a clear blue Los Angeles sky", "width": 1800, "height": 1195},
    {"n": 6, "slug": "downtown-los-angeles-night-reflections", "title": "Downtown Los Angeles Lights Reflected Across the Water", "description": "Illuminated towers, palm trees and city lights create colourful reflections across the dark water in Los Angeles. The calm foreground transforms the Downtown skyline into a layered night scene of architecture, colour and mirrored light.", "meta_description": "View Downtown Los Angeles towers, palm trees and colourful city lights reflected across the water after dark.", "alt": "Downtown Los Angeles towers and palm trees reflected in calm water at night", "width": 1800, "height": 1122},
    {"n": 7, "slug": "downtown-los-angeles-freeway-cityscape", "title": "Downtown Los Angeles Rising Above a Busy Freeway", "description": "Streams of daytime traffic move through a wide multilane freeway while the Downtown Los Angeles skyline rises beyond the concrete corridor. The photograph captures the close relationship between movement, infrastructure and vertical urban growth in the city.", "meta_description": "See Downtown Los Angeles rising behind a busy multilane freeway in this daytime cityscape and urban-infrastructure photograph.", "alt": "Downtown Los Angeles skyline rising behind traffic on a wide multilane freeway", "width": 1800, "height": 1439},
    {"n": 8, "slug": "los-angeles-freeway-night-traffic", "title": "Night Freeway Traffic Leading Toward Downtown Los Angeles", "description": "Red taillights form continuous streams along a Los Angeles freeway as traffic moves toward the illuminated Downtown skyline. Dark hills, overhead signs and distant towers combine in a distinctly nocturnal portrait of the city in motion.", "meta_description": "Follow streams of night traffic along a Los Angeles freeway toward the illuminated Downtown skyline and city towers.", "alt": "Red freeway traffic lights leading toward the illuminated Downtown Los Angeles skyline at night", "width": 1800, "height": 1270},
    {"n": 9, "slug": "downtown-los-angeles-overlook", "title": "Downtown Los Angeles Skyline Viewed from a Scenic Overlook", "description": "A solitary visitor stands in the foreground and looks across the vast urban fabric toward the distant Downtown Los Angeles skyline. The soft focus of the observer creates a personal sense of scale, distance and discovery within the metropolitan panorama.", "meta_description": "A visitor looks across the Los Angeles cityscape toward the distant Downtown skyline from a high scenic viewpoint.", "alt": "Visitor overlooking the expansive Los Angeles cityscape and distant Downtown skyline", "width": 1800, "height": 1200},
]

URBAN_ART_CONTEXT = [
    "Like urban art, the monumental lettering shows how a bold visual statement can transform a landscape and become part of a city’s identity.",
    "This dialogue between a human-made symbol and its surroundings also reflects how urban art responds to the character of a specific place.",
    "Within this vast urban fabric, urban art—from murals to installations and street interventions—gives neighbourhoods a distinct visual voice by day and night.",
    "Seen at this scale, Los Angeles becomes a vast canvas in which urban art connects architecture, communities and public space.",
    "Urban art similarly uses highly visible signs, symbols and public surfaces to communicate ideas and shape shared cultural memory.",
    "Its saturated colours and overlapping forms echo the visual energy found in murals and contemporary urban art across the city.",
    "Concrete corridors and overlooked structures are also important urban-art spaces, where creative interventions can give anonymous infrastructure a human voice.",
    "The rhythm of lights, signs and movement forms a living visual language that continually inspires urban artists.",
    "Urban art invites a similar way of looking: beyond individual works to the neighbourhoods, architecture and public spaces that give them meaning.",
]

for photo, urban_art_sentence in zip(PHOTOS, URBAN_ART_CONTEXT, strict=True):
    photo["description"] = f'{photo["description"]} {urban_art_sentence}'

def esc(value):
    return html.escape(str(value), quote=True)

def link_los_angeles(value):
    """Escape visible copy and link every Los Angeles mention to the city hub."""
    city_link = '<a href="/cities/los-angeles/" title="Los Angeles Urban Art"><strong>Los Angeles</strong></a>'
    return esc(value).replace("Los Angeles", city_link)

def decode_staged_images():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for photo in PHOTOS:
        staged = UPLOAD_DIR / f"los-angeles-{photo['n']}.jpg.b64"
        target = ASSET_DIR / f"{photo['slug']}.jpg"
        if staged.exists():
            target.write_bytes(base64.b64decode(staged.read_text(encoding="utf-8")))
            staged.unlink()
            print(f"IMPORT Los Angeles image: {target}")

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
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/cities/los-angeles/">Los Angeles</a><a href="/urban-art-cities/">Cities</a><a href="/artists/">Artists</a><a href="/subscribe/">Subscribe</a></nav></header>"""

def footer():
    return '<footer>© 2026 Urban Arts News · <a href="/cities/los-angeles/" title="Los Angeles Urban Art"><strong>Los Angeles</strong></a> Urban Art · City Photography</footer></body></html>'

def generate_detail(photo):
    slug = photo["slug"]
    canonical = f"{BASE}/cities/los-angeles/gallery/{slug}/"
    image = f"{BASE}/assets/images/los-angeles/{slug}.jpg"
    description = photo["meta_description"]
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":photo["title"],"description":description,"primaryImageOfPage":{"@id":canonical+"#image"}},
        {"@type":"ImageObject","@id":canonical+"#image","name":photo["title"],"description":description,"caption":photo["description"],"contentUrl":image,"url":canonical,"encodingFormat":"image/jpeg","width":{"@type":"QuantitativeValue","value":photo["width"],"unitCode":"E37"},"height":{"@type":"QuantitativeValue","value":photo["height"],"unitCode":"E37"},"contentLocation":{"@type":"Place","name":"Los Angeles, California, United States"},"creditText":"Urban Arts News Los Angeles Gallery","copyrightNotice":"All rights reserved by the respective copyright holder","representativeOfPage":True,"keywords":["Los Angeles Urban Art News","Urban Art Los Angeles","Los Angeles City Photography","Urban Arts News"]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Los Angeles","item":BASE+"/cities/los-angeles/"},{"@type":"ListItem","position":3,"name":"Los Angeles Gallery","item":BASE+"/cities/los-angeles/gallery/"},{"@type":"ListItem","position":4,"name":photo["title"],"item":canonical}]}
    ]}
    markup = head(photo["title"]+" | Los Angeles Urban Arts News", description, canonical, image, photo["width"], photo["height"], schema)
    markup += f"""<main class="container"><article class="photo">
<picture><source type="image/webp" media="(max-width:600px)" srcset="/assets/images/los-angeles/responsive/{slug}-480.webp"><source type="image/webp" media="(max-width:1100px)" srcset="/assets/images/los-angeles/responsive/{slug}-960.webp"><img src="/assets/images/los-angeles/{slug}.jpg" alt="{esc(photo['alt'])}" width="{photo['width']}" height="{photo['height']}" loading="eager" fetchpriority="high" decoding="async"></picture>
<div class="caption"><h1>{esc(photo['title'])}</h1><p>{esc(photo['description'])}</p>
<p><strong><a href="https://urbanartsnews.com/cities/los-angeles/">Los Angeles Urban Art News</a></strong> presents this photograph as part of its visual documentation of <strong><a href="https://urbanartsnews.com/cities/los-angeles/">Urban Art Los Angeles</a></strong>, city culture and the changing metropolitan landscape.</p>
<p>Discover more urban photography, contemporary artists and city culture on <a href="https://urbanartsnews.com/"><strong>Urban Arts News</strong></a>.</p>
<p class="credit">Photograph supplied for publication to Urban Arts News. Rights remain with the respective copyright holder.</p>
<a class="button" href="/cities/los-angeles/gallery/">Los Angeles Gallery</a><a class="button" href="/cities/los-angeles/">Los Angeles Urban Art</a>
</div></article></main>""" + footer()
    out = GALLERY_DIR / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(markup, encoding="utf-8")

def generate_gallery():
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    hero = PHOTOS[3]
    canonical = BASE + "/cities/los-angeles/gallery/"
    image = BASE + f"/assets/images/los-angeles/{hero['slug']}.jpg"
    description = "Explore nine original Los Angeles photographs featuring the Hollywood Sign, Downtown skyline, freeways and city views on Urban Arts News."
    item_list = [{"@type":"ListItem","position":i+1,"url":BASE+f"/cities/los-angeles/gallery/{p['slug']}/","name":p["title"]} for i,p in enumerate(PHOTOS)]
    schema={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,"name":"Los Angeles Urban Photography Gallery","description":description,"mainEntity":{"@type":"ItemList","numberOfItems":9,"itemListElement":item_list}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Los Angeles","item":BASE+"/cities/los-angeles/"},{"@type":"ListItem","position":3,"name":"Los Angeles Gallery","item":canonical}]}]}
    cards=""
    for i,p in enumerate(PHOTOS):
        attrs='loading="eager" fetchpriority="high"' if i==0 else 'loading="lazy"'
        cards += f"""<article class="card"><a href="/cities/los-angeles/gallery/{p['slug']}/"><picture><source type="image/webp" srcset="/assets/images/los-angeles/responsive/{p['slug']}-480.webp 480w, /assets/images/los-angeles/responsive/{p['slug']}-960.webp 960w" sizes="(max-width:800px) 92vw, 30vw"><img src="/assets/images/los-angeles/{p['slug']}.jpg" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {attrs} decoding="async"></picture></a><div class="card-content"><h2>{link_los_angeles(p['title'])}</h2><p>{link_los_angeles(p['description'])}</p><a href="/cities/los-angeles/gallery/{p['slug']}/">View photograph →</a></div></article>"""
    markup=head("Los Angeles Urban Photography Gallery | Urban Arts News",description,canonical,image,hero["width"],hero["height"],schema)
    markup+=f"""<section class="hero"><small>Urban Arts News · {link_los_angeles('Los Angeles')} Gallery</small><h1>{link_los_angeles('Los Angeles')} <span class="accent">City Gallery</span></h1><p>{link_los_angeles('Nine original photographs documenting the Hollywood Sign, Downtown Los Angeles, freeways, night views and the visual identity surrounding Urban Art Los Angeles.')}</p></section><main class="container"><h2>{link_los_angeles('Los Angeles Urban Art News and City Photography')}</h2><p>{link_los_angeles('This curated gallery connects Los Angeles city photography with the wider Urban Arts News archive. Each photograph has its own indexable page, descriptive metadata and links to the Los Angeles urban-art directory.')}</p><div class="grid">{cards}</div></main>"""+footer()
    (GALLERY_DIR/"index.html").write_text(markup,encoding="utf-8")

def patch_city_page():
    path=Path("cities/los-angeles/index.html")
    if not path.exists(): return
    text=path.read_text(encoding="utf-8")
    marker="/cities/los-angeles/gallery/"
    if marker not in text:
        block='''<section class="related"><h2>Los Angeles City Photography Gallery</h2><p>Explore nine original photographs of the Hollywood Sign, Downtown skyline, freeways and Los Angeles city views.</p><a class="button" href="/cities/los-angeles/gallery/">Explore Los Angeles Gallery →</a></section>'''
        text=text.replace("</main>",block+"</main>")
        path.write_text(text,encoding="utf-8")

def update_sitemap():
    path=Path("sitemap.xml")
    text=path.read_text(encoding="utf-8")
    urls=[BASE+"/cities/los-angeles/gallery/"]+[BASE+f"/cities/los-angeles/gallery/{p['slug']}/" for p in PHOTOS]
    additions=""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions+=f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    text=text.replace("</urlset>",additions+"</urlset>")
    path.write_text(text,encoding="utf-8")

def image_sitemap():
    rows=[]
    for p in PHOTOS:
        page=BASE+f"/cities/los-angeles/gallery/{p['slug']}/"
        image=BASE+f"/assets/images/los-angeles/{p['slug']}.jpg"
        rows.append(f"  <url><loc>{page}</loc><image:image><image:loc>{image}</image:loc></image:image></url>")
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+"\n".join(rows)+"\n</urlset>\n"
    Path("image-sitemap-los-angeles.xml").write_text(xml,encoding="utf-8")
    robots=Path("robots.txt")
    content=robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    line=f"Sitemap: {BASE}/image-sitemap-los-angeles.xml"
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
    print("DONE Los Angeles gallery: 9 photographs")

if __name__=="__main__":
    main()
