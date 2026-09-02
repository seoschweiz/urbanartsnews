from pathlib import Path
import base64
import html
import json
import re
import unicodedata
from PIL import Image, ImageFile

# Some source JPEGs contain a valid image with an incomplete final data block.
ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE = "https://urbanartsnews.com"
UPLOAD_DIR = Path("data/image_uploads")
ASSET_DIR = Path("assets/images/barcelona")
RESPONSIVE_DIR = ASSET_DIR / "responsive"
GALLERY_DIR = Path("cities/barcelona/gallery")
REDIRECTS = {
    "barcelona-waterfront-w-hotel": "barcelona-skyline-torre-glories",
    "barcelona-skyline-mediterranean": "sagrada-familia-barcelona-panorama",
}

LEGACY_PHOTOS = [
    {"n": 1, "slug": "park-guell-mosaic-view-barcelona", "title": "Park Güell Mosaic Terrace Overlooking Barcelona", "description": "Colourful mosaic architecture in Antoni Gaudí’s Park Güell frames a panoramic view across Barcelona, from the dense city blocks to the distant hills. The textured stone and broken-tile surfaces turn the viewpoint itself into a distinctive visual composition. Their expressive colour and handcrafted detail anticipate the way urban art transforms architecture into an experience shared in public space.", "meta_description": "Explore Gaudí’s colourful Park Güell mosaic terrace and its panoramic view across Barcelona in this Urban Arts News photograph.", "alt": "Colourful Park Güell mosaic terrace overlooking the Barcelona cityscape", "width": 1600, "height": 1066},
    {"n": 2, "slug": "barcelona-cathedral-gothic-quarter", "title": "Barcelona Cathedral and Gothic Quarter Square", "description": "The richly detailed façade of Barcelona Cathedral rises above the broad stone square in the historic Gothic Quarter. Visitors crossing the open space provide a human sense of scale beside the monumental architecture. Urban art enters similarly into conversation with historic streets, adding contemporary voices to places shaped by many cultural layers.", "meta_description": "View Barcelona Cathedral, its Gothic façade and the historic public square at the heart of the city’s Gothic Quarter.", "alt": "Barcelona Cathedral façade and visitors in the Gothic Quarter square", "width": 1600, "height": 1280},
    {"n": 3, "slug": "sagrada-familia-barcelona-park-view", "title": "Sagrada Família Across a Reflecting Pond in Barcelona", "description": "The towers of the Sagrada Família rise beyond trees and a calm reflecting pond in Barcelona. Framed by greenery and water, the basilica appears as part of a living urban landscape rather than an isolated monument. Its evolving forms show how ambitious visual ideas can reshape a skyline, while urban art brings the same creative energy to walls and public spaces at street level.", "meta_description": "See the Sagrada Família rising above trees and a reflecting pond in Barcelona in this atmospheric city photograph.", "alt": "Sagrada Família towers beyond trees and a reflecting pond in Barcelona", "width": 1600, "height": 1200},
    {"n": 4, "slug": "barcelona-waterfront-w-hotel", "title": "Barcelona Marina and W Hotel on the Waterfront", "description": "Sailing boats fill the marina while the curved W Hotel rises beside Barcelona’s Mediterranean waterfront. Water, modern architecture and port infrastructure create a layered portrait of the city’s coastal identity. Along such transitional urban zones, public art and creative interventions can reconnect functional spaces with the people who move through them.", "meta_description": "Explore Barcelona marina, sailing boats and the landmark W Hotel beside the city’s Mediterranean waterfront.", "alt": "Sailing boats in Barcelona marina with the W Hotel on the Mediterranean waterfront", "width": 1600, "height": 1067},
    {"n": 5, "slug": "barcelona-skyline-mediterranean", "title": "Barcelona Waterfront Skyline from the Mediterranean Sea", "description": "A wide view from the Mediterranean reveals Barcelona’s waterfront skyline, dense architecture and hills beneath an overcast sky. The distance makes the relationship between the coastline and the metropolitan landscape especially clear. Within that urban fabric, murals and other forms of urban art give individual neighbourhoods a visual identity that cannot be read from the skyline alone.", "meta_description": "View Barcelona’s waterfront skyline, city architecture and surrounding hills from across the Mediterranean Sea.", "alt": "Barcelona waterfront skyline and hills viewed across the Mediterranean Sea", "width": 1600, "height": 1066},
    {"n": 6, "slug": "barcelona-panoramic-city-view", "title": "Panoramic Barcelona Cityscape from a Green Overlook", "description": "Barcelona’s tightly packed cityscape stretches toward the surrounding hills from a green elevated viewpoint. Trees in the foreground contrast with the geometric grid, rooftops and distant urban landmarks. Seen from above, the city becomes a vast canvas, while urban art restores personal stories and local character to its individual streets.", "meta_description": "Discover a panoramic Barcelona cityscape, distant hills and dense urban architecture from a green elevated viewpoint.", "alt": "Panoramic Barcelona cityscape and distant hills viewed through green trees", "width": 1600, "height": 900},
    {"n": 7, "slug": "park-guell-barcelona-sunset", "title": "Park Güell Above Barcelona at a Colourful Sunset", "description": "Gaudí’s sculptural Park Güell architecture overlooks Barcelona beneath a sky filled with soft pink and purple sunset light. Mosaic surfaces and distinctive rooftop forms stand out against the Mediterranean horizon. The playful combination of colour, craft and architecture shares urban art’s ability to turn a public setting into a memorable visual landmark.", "meta_description": "See Gaudí’s Park Güell architecture above Barcelona beneath a colourful pink and purple Mediterranean sunset.", "alt": "Gaudí architecture in Park Güell overlooking Barcelona at a colourful sunset", "width": 1600, "height": 1059},
    {"n": 8, "slug": "gaudi-mosaic-window-barcelona-view", "title": "Gaudí Mosaic Architecture Framing a Barcelona Panorama", "description": "A sculptural stone opening decorated with colourful mosaic fragments frames a broad panorama across Barcelona. The composition connects Park Güell’s tactile architectural detail with the dense city beyond it. This fusion of surface, colour and public architecture remains deeply relevant to contemporary urban art and its transformation of everyday surroundings.", "meta_description": "Explore colourful Gaudí mosaic architecture framing a panoramic Barcelona city view from Park Güell.", "alt": "Gaudí mosaic stone opening framing a panoramic view across Barcelona", "width": 1600, "height": 1066},
    {"n": 9, "slug": "historic-central-barcelona-street", "title": "Historic Barcelona Avenue and Ornate City Architecture", "description": "Ornate stone façades line a busy central Barcelona avenue filled with pedestrians, cars and everyday city movement. Curved corners, balconies and decorative towers give the intersection a strong architectural rhythm. Urban art adds another layer to streets like these, allowing contemporary images and ideas to interact with the historic character of the city.", "meta_description": "Explore a busy central Barcelona avenue lined with ornate historic façades, balconies and distinctive city architecture.", "alt": "Busy central Barcelona avenue lined with ornate historic architecture", "width": 1600, "height": 1200},
]

PHOTOS = [
    {"n": 1, "slug": "barcelona-skyline-torre-glories", "title": "Barcelona Skyline with Torre Glòries and Mountain Views", "description": "Barcelona’s dense urban skyline extends toward the mountains, with the distinctive Torre Glòries rising above the surrounding rooftops. The elevated perspective reveals layers of residential blocks, landmarks and metropolitan infrastructure. Urban art gives this immense cityscape a human scale by bringing local stories, colour and identity to its streets.", "meta_description": "Explore Barcelona’s skyline, Torre Glòries, dense city architecture and distant mountains in this panoramic photograph.", "alt": "Barcelona skyline with Torre Glòries and mountains in the distance", "width": 2048, "height": 1536},
    {"n": 2, "slug": "sagrada-familia-barcelona-panorama", "title": "Sagrada Família Rising Across the Barcelona Cityscape", "description": "The Sagrada Família rises from the centre of Barcelona’s expansive cityscape beneath warm evening light. Dense rooftops and distant hills emphasise the basilica’s extraordinary vertical presence within the metropolitan grid. Like urban art, its evolving visual language challenges familiar ideas about architecture and reshapes the identity of public space.", "meta_description": "See the Sagrada Família rising above Barcelona’s dense rooftops and distant hills in this panoramic city photograph.", "alt": "Sagrada Família rising above the panoramic Barcelona cityscape", "width": 2048, "height": 1365},
    {"n": 3, "slug": "barcelona-cathedral-gothic-quarter", "title": "Barcelona Cathedral and Gothic Quarter Square", "description": "The richly detailed façade of Barcelona Cathedral rises above the broad stone square in the historic Gothic Quarter. Visitors crossing the open space provide a human sense of scale beside the monumental architecture. Urban art enters similarly into conversation with historic streets, adding contemporary voices to places shaped by many cultural layers.", "meta_description": "View Barcelona Cathedral, its Gothic façade and the historic public square at the heart of the city’s Gothic Quarter.", "alt": "Barcelona Cathedral façade and visitors in the Gothic Quarter square", "width": 2048, "height": 1638},
    {"n": 4, "slug": "sagrada-familia-barcelona-park-view", "title": "Sagrada Família Across a Reflecting Pond in Barcelona", "description": "The towers of the Sagrada Família rise beyond trees and a calm reflecting pond in Barcelona. Framed by greenery and water, the basilica appears as part of a living urban landscape rather than an isolated monument. Its evolving forms show how ambitious visual ideas can reshape a skyline, while urban art brings the same creative energy to walls and public spaces at street level.", "meta_description": "See the Sagrada Família rising above trees and a reflecting pond in Barcelona in this atmospheric city photograph.", "alt": "Sagrada Família towers beyond trees and a reflecting pond in Barcelona", "width": 2048, "height": 1536},
    {"n": 5, "slug": "park-guell-barcelona-sunset", "title": "Park Güell Above Barcelona at a Colourful Sunset", "description": "Gaudí’s sculptural Park Güell architecture overlooks Barcelona beneath a sky filled with soft pink and purple sunset light. Mosaic surfaces and distinctive rooftop forms stand out against the Mediterranean horizon. The playful combination of colour, craft and architecture shares urban art’s ability to turn a public setting into a memorable visual landmark.", "meta_description": "See Gaudí’s Park Güell architecture above Barcelona beneath a colourful pink and purple Mediterranean sunset.", "alt": "Gaudí architecture in Park Güell overlooking Barcelona at a colourful sunset", "width": 2048, "height": 1356},
    {"n": 6, "slug": "barcelona-panoramic-city-view", "title": "Panoramic Barcelona Cityscape and Tibidabo Hills", "description": "Barcelona spreads across the frame toward the dark silhouette of the Tibidabo hills and their illuminated landmarks. Soft evening light reveals the scale and density of the city without losing the contours of its natural setting. Across this urban fabric, street art and murals create closer, community-level perspectives that complement the distant panorama.", "meta_description": "Discover a panoramic Barcelona cityscape extending toward the Tibidabo hills and landmarks in soft evening light.", "alt": "Panoramic Barcelona cityscape with the Tibidabo hills in the distance", "width": 2048, "height": 1365},
    {"n": 7, "slug": "gaudi-mosaic-window-barcelona-view", "title": "Gaudí Mosaic Architecture Framing a Barcelona Panorama", "description": "A sculptural stone opening decorated with colourful mosaic fragments frames a broad panorama across Barcelona. The composition connects Park Güell’s tactile architectural detail with the dense city beyond it. This fusion of surface, colour and public architecture remains deeply relevant to contemporary urban art and its transformation of everyday surroundings.", "meta_description": "Explore colourful Gaudí mosaic architecture framing a panoramic Barcelona city view from Park Güell.", "alt": "Gaudí mosaic stone opening framing a panoramic view across Barcelona", "width": 2048, "height": 1365},
    {"n": 8, "slug": "historic-central-barcelona-street", "title": "Historic Barcelona Avenue and Ornate City Architecture", "description": "Ornate stone façades line a busy central Barcelona avenue filled with pedestrians, cars and everyday city movement. Curved corners, balconies and decorative towers give the intersection a strong architectural rhythm. Urban art adds another layer to streets like these, allowing contemporary images and ideas to interact with the historic character of the city.", "meta_description": "Explore a busy central Barcelona avenue lined with ornate historic façades, balconies and distinctive city architecture.", "alt": "Busy central Barcelona avenue lined with ornate historic architecture", "width": 2048, "height": 1536},
    {"n": 9, "slug": "park-guell-mosaic-view-barcelona", "title": "Park Güell Mosaic Terrace Overlooking Barcelona", "description": "Colourful mosaic architecture in Antoni Gaudí’s Park Güell frames a panoramic view across Barcelona, from the dense city blocks to the distant hills. The textured stone and broken-tile surfaces turn the viewpoint itself into a distinctive visual composition. Their expressive colour and handcrafted detail anticipate the way urban art transforms architecture into an experience shared in public space.", "meta_description": "Explore Gaudí’s colourful Park Güell mosaic terrace and its panoramic view across Barcelona in this Urban Arts News photograph.", "alt": "Colourful Park Güell mosaic terrace overlooking the Barcelona cityscape", "width": 2048, "height": 1365},
]

PAGE2_PHOTOS = [
    {"n": 10, "slug": "barcelona-sagrada-familia-aerial-culture", "title": "Sagrada Família and Barcelona from Above", "description": "An aerial view places the Sagrada Família at the centre of Barcelona’s dense street grid. The photograph shows how monumental architecture, neighbourhood life and the Mediterranean cityscape meet in one urban environment. Creative expression at this scale provides the setting in which Barcelona’s graffiti, street art and independent urban culture continue to evolve.", "meta_description": "See the Sagrada Família at the centre of Barcelona in this branded aerial city photograph from Urban Arts News.", "alt": "Aerial Barcelona cityscape with the Sagrada Família and Urban Arts News branding", "width": 1536, "height": 1024},
    {"n": 11, "slug": "park-guell-entrance-urban-culture", "title": "Park Güell Entrance and Barcelona Coast", "description": "Gaudí’s sculptural entrance buildings frame a broad view toward Barcelona and the Mediterranean. Their mosaic details, playful shapes and public setting connect architecture with the same accessible visual energy found in contemporary urban art. The scene presents Barcelona as a city where historic design and new creative voices continually share public space.", "meta_description": "Explore the Park Güell entrance and Barcelona coast in this branded Urban Arts News city photograph.", "alt": "Park Güell entrance buildings overlooking Barcelona with Urban Arts News branding", "width": 1448, "height": 1086},
    {"n": 12, "slug": "barcelona-coast-torre-glories-panorama", "title": "Barcelona Coast and Torre Glòries Panorama", "description": "The Torre Glòries rises from Barcelona’s metropolitan landscape while the Mediterranean defines the horizon. Seen from the hills, the city becomes a layered field of architecture, neighbourhoods and creative districts. Within that panorama, murals and street interventions give individual places a recognisable identity and bring urban culture closer to everyday life.", "meta_description": "View Barcelona’s coastline, Torre Glòries and metropolitan panorama in a branded Urban Arts News photograph.", "alt": "Barcelona coastline and Torre Glòries panorama with Urban Arts News branding", "width": 1536, "height": 1024},
    {"n": 13, "slug": "arc-de-triomf-public-culture", "title": "Arc de Triomf and Barcelona Public Culture", "description": "Barcelona’s red-brick Arc de Triomf anchors a wide pedestrian avenue used for encounters, performances and public events. The open urban setting demonstrates how architecture becomes meaningful through the communities moving around it. Street art and graffiti participate in the same living culture by adding contemporary images, messages and identities to the city.", "meta_description": "Discover Barcelona’s Arc de Triomf and public urban culture in this branded Urban Arts News photograph.", "alt": "Arc de Triomf in Barcelona with pedestrians, palms and Urban Arts News branding", "width": 1448, "height": 1086},
    {"n": 14, "slug": "barcelona-beaches-urban-coast", "title": "Barcelona Beaches and Mediterranean Urban Coast", "description": "Barcelona’s beaches curve alongside dense neighbourhoods, promenades and contemporary waterfront architecture. The view reveals how public leisure, city planning and Mediterranean identity overlap along the coast. Urban culture develops in these shared spaces through music, design, performance, graffiti and the many informal encounters that make a city visually distinctive.", "meta_description": "Explore Barcelona’s beaches and Mediterranean urban coast in this branded Urban Arts News city photograph.", "alt": "Barcelona beaches and Mediterranean coastline with Urban Arts News branding", "width": 1536, "height": 1024},
    {"n": 15, "slug": "park-guell-mosaic-public-art", "title": "Park Güell Mosaic Forms and Public Art", "description": "Colourful mosaic surfaces curve across Park Güell while Barcelona and the sea extend into the distance. The handcrafted fragments transform functional architecture into an immersive public artwork. Their accessibility, colour and relationship to place anticipate qualities that remain central to street art: visual invention experienced directly within everyday urban space.", "meta_description": "See Park Güell’s colourful mosaic forms and Barcelona panorama in a branded Urban Arts News photograph.", "alt": "Colourful Park Güell mosaic architecture with Barcelona and Urban Arts News branding", "width": 1448, "height": 1086},
    {"n": 16, "slug": "gran-via-barcelona-golden-hour", "title": "Gran Via Barcelona at Golden Hour", "description": "Ornate façades and broad avenues fill central Barcelona with strong architectural rhythm in the warm evening light. Historic buildings provide a dramatic backdrop for the movement of contemporary city life below. New murals, graphic interventions and urban artists add further layers to this inherited streetscape without erasing the identity already present.", "meta_description": "View central Barcelona and Gran Via architecture at golden hour in a branded Urban Arts News photograph.", "alt": "Gran Via and central Barcelona architecture at golden hour with Urban Arts News branding", "width": 1536, "height": 1024},
    {"n": 17, "slug": "tibidabo-sunset-urban-landscape", "title": "Tibidabo Sunset Above Barcelona", "description": "The Temple of the Sacred Heart stands above Barcelona as sunset colours spread across the mountains and Mediterranean coast. From Tibidabo, the city appears as a vast connected landscape shaped by architecture, mobility and creative communities. At street level, urban artists turn sections of that landscape into personal, political and shared visual narratives.", "meta_description": "Experience a vivid Tibidabo sunset above Barcelona in this branded Urban Arts News city photograph.", "alt": "Tibidabo church and Barcelona at sunset with Urban Arts News branding", "width": 1537, "height": 1023},
    {"n": 18, "slug": "gran-via-barcelona-night-culture", "title": "Gran Via Barcelona and Night Culture", "description": "Central Barcelona glows after sunset as traffic, illuminated façades and rooftop spaces activate the city. The transition from day to night changes how architecture and public space are experienced. Music, nightlife, design and visual art become part of a wider urban culture that connects local creators with visitors from around the world.", "meta_description": "Explore Gran Via and Barcelona night culture in this branded evening photograph from Urban Arts News.", "alt": "Illuminated Gran Via Barcelona at night with Urban Arts News branding", "width": 1536, "height": 1024},
]

ARTEVISTAS_IMAGES = [
    {"slug": "street-art-gallery-barcelona-artevistas-born-interior", "title": "Artevistas Born – Street Art Gallery Barcelona", "alt": "Panoramic interior of Artevistas Born, a contemporary and street art gallery in Barcelona", "caption": "Inside Artevistas Born, a Barcelona gallery presenting contemporary art, collectible street art and emerging artists near the Picasso Museum.", "description": "A panoramic view inside Artevistas Gallery Born showing its vaulted exhibition rooms and a selection of contemporary and urban artworks in Barcelona.", "width": 1600, "height": 738, "location": "born", "keywords": ["Street Art Gallery Barcelona", "Urban Art Gallery Barcelona", "Artevistas Born", "El Born Barcelona", "Gallery Interior Barcelona"]},
    {"slug": "street-art-gallery-barcelona-artevistas-exhibitions-events", "title": "Artevistas Exhibitions and Events in Barcelona", "alt": "Artevistas Gallery Barcelona exhibition and event programme featuring contemporary and urban artists", "caption": "Artevistas Gallery connects Barcelona audiences with changing exhibitions, openings and events involving contemporary and urban artists.", "description": "Screenshot documenting upcoming and past exhibitions at Artevistas Gallery Barcelona, including artist presentations and urban-art-related cultural events.", "width": 1600, "height": 725, "location": "both", "keywords": ["Street Art Gallery Barcelona", "Barcelona Art Events", "Barcelona Exhibitions", "Gallery Openings Barcelona"]},
    {"slug": "street-art-gallery-barcelona-artevistas-gotic", "title": "Artevistas Gòtic – Urban Art Gallery Barcelona", "alt": "Artevistas Gallery Gòtic in Barcelona with entrance and interior views of contemporary urban art", "caption": "Artevistas Gòtic presents original artworks and editions in Barcelona's historic centre at Passatge del Crèdit 4.", "description": "A visual overview of the Artevistas Gòtic location, combining its Barcelona entrance with interior views and displays of contemporary and urban art.", "width": 1600, "height": 733, "location": "gotic", "keywords": ["Urban Art Gallery Barcelona", "Artevistas Gòtic", "Gothic Quarter Barcelona", "Passatge del Crèdit"]},
    {"slug": "street-art-gallery-barcelona-artevistas-born-gallery-views", "title": "Artevistas Born Gallery Views – Barcelona", "alt": "Multiple interior views of Artevistas Born street art and contemporary art gallery in Barcelona", "caption": "A series of gallery views from Artevistas Born showing the scale, architecture and changing presentation of art in the Barcelona space.", "description": "A gallery grid documenting the Artevistas Born interior, its historic vaulted rooms and varied displays of street art and contemporary artworks.", "width": 1600, "height": 716, "location": "born", "keywords": ["Street Art Gallery Barcelona", "Artevistas Born Interior", "Barcelona Gallery Views", "Urban Art Exhibition Space"]},
]

ARTEVISTAS_LOCATIONS = {
    "born": {"name": "Artevistas Gallery Born", "address": "Carrer de la Barra de Ferro, 8, 08003 Barcelona, Spain", "latitude": 41.3849551, "longitude": 2.1804722, "maps": "https://www.google.com/maps/search/?api=1&query=Artevistas%20Gallery%20Born%2C%20Carrer%20de%20la%20Barra%20de%20Ferro%208%2C%20Barcelona"},
    "gotic": {"name": "Artevistas Gallery Gòtic", "address": "Passatge del Crèdit, 4, 08002 Barcelona, Spain", "latitude": 41.38185, "longitude": 2.17644, "maps": "https://www.google.com/maps/search/?api=1&query=Artevistas%20Gallery%20Gotic%2C%20Passatge%20del%20Credit%204%2C%20Barcelona"},
}

ALL_PHOTOS = PHOTOS + PAGE2_PHOTOS

def esc(value):
    return html.escape(str(value), quote=True)

def link_barcelona(value):
    """Escape gallery copy and link every visible Barcelona mention to the SEO city hub."""
    city_link = '<a href="/cities/barcelona/" title="Barcelona Urban Art"><strong>Barcelona</strong></a>'
    return esc(value).replace("Barcelona", city_link)

def seo_exif(photo):
    """Create embedded JPEG metadata that describes the photograph accurately."""
    exif = Image.Exif()
    keywords = "Barcelona; Urban Art; Barcelona Photography; Urban Arts News; Spain"
    full_description = f"{photo['title']}. {photo['description']}"
    ascii_description = unicodedata.normalize("NFKD", full_description).encode("ascii", "ignore").decode("ascii")
    exif[270] = ascii_description
    exif[315] = "Pexels contributor"
    exif[33432] = "Pexels License / respective contributor"
    exif[40091] = (photo["title"] + "\0").encode("utf-16le")
    exif[40092] = (full_description + "\0").encode("utf-16le")
    exif[40094] = (keywords + "\0").encode("utf-16le")
    return exif

def prepare_original(source, photo):
    """Optimise a licensed Pexels original and retain neutral source metadata."""
    with Image.open(source) as original:
        image = original.convert("RGB")
        image.save(source, "JPEG", quality=88, optimize=True, progressive=True, exif=seo_exif(photo))

def ensure_page2_metadata():
    """Embed descriptive metadata once without repeatedly recompressing images."""
    for photo in PAGE2_PHOTOS:
        source = ASSET_DIR / f"{photo['slug']}.jpg"
        if not source.exists():
            continue
        with Image.open(source) as image:
            has_description = bool(image.getexif().get(270))
        if not has_description:
            prepare_original(source, photo)

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
    for photo in ALL_PHOTOS:
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
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/cities/barcelona/">Barcelona</a><a href="/urban-art-cities/">Cities</a><a href="/artists/">Artists</a><a href="/subscribe/">Subscribe</a></nav></header>"""

def footer():
    return '<footer>© 2026 Urban Arts News · <a href="/cities/barcelona/" title="Barcelona Urban Art"><strong>Barcelona</strong></a> Urban Art · City Photography</footer></body></html>'

def generate_detail(photo):
    slug = photo["slug"]
    canonical = f"{BASE}/cities/barcelona/gallery/{slug}/"
    image = f"{BASE}/assets/images/barcelona/{slug}.jpg"
    description = photo["meta_description"]
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":photo["title"],"description":description,"primaryImageOfPage":{"@id":canonical+"#image"}},
        {"@type":"ImageObject","@id":canonical+"#image","name":photo["title"],"description":description,"caption":photo["description"],"contentUrl":image,"url":canonical,"encodingFormat":"image/jpeg","width":{"@type":"QuantitativeValue","value":photo["width"],"unitCode":"E37"},"height":{"@type":"QuantitativeValue","value":photo["height"],"unitCode":"E37"},"contentLocation":{"@type":"Place","name":"Barcelona, Catalonia, Spain"},"creditText":"Pexels contributor via Pexels","copyrightNotice":"Used under the Pexels License; rights remain with the respective contributor","representativeOfPage":True,"keywords":["Barcelona Urban Art News","Urban Art Barcelona","Barcelona City Photography","Urban Arts News"]},
        {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Barcelona","item":BASE+"/cities/barcelona/"},{"@type":"ListItem","position":3,"name":"Barcelona Gallery","item":BASE+"/cities/barcelona/gallery/"},{"@type":"ListItem","position":4,"name":photo["title"],"item":canonical}]}
    ]}
    markup = head(photo["title"]+" | Barcelona Urban Arts News", description, canonical, image, photo["width"], photo["height"], schema)
    markup += f"""<main class="container"><article class="photo">
<picture><source type="image/webp" media="(max-width:600px)" srcset="/assets/images/barcelona/responsive/{slug}-480.webp"><source type="image/webp" media="(max-width:1100px)" srcset="/assets/images/barcelona/responsive/{slug}-960.webp"><img src="/assets/images/barcelona/{slug}.jpg" alt="{esc(photo['alt'])}" width="{photo['width']}" height="{photo['height']}" loading="eager" fetchpriority="high" decoding="async"></picture>
<div class="caption"><h1>{esc(photo['title'])}</h1><p>{esc(photo['description'])}</p>
<p><strong><a href="https://urbanartsnews.com/cities/barcelona/">Barcelona Urban Art News</a></strong> presents this photograph as part of its visual documentation of <strong><a href="https://urbanartsnews.com/cities/barcelona/">Urban Art Barcelona</a></strong>, city culture and the changing metropolitan landscape.</p>
<p>Discover more urban photography, contemporary artists and city culture on <a href="https://urbanartsnews.com/"><strong>Urban Arts News</strong></a>.</p>
<p class="credit">Photo via <a href="https://www.pexels.com/"><strong>Pexels</strong></a>, used under the <a href="https://www.pexels.com/license/">Pexels License</a>. Rights remain with the respective contributor.</p>
<a class="button" href="/cities/barcelona/gallery/{'page/2/' if photo in PAGE2_PHOTOS else ''}">Barcelona Gallery</a><a class="button" href="/cities/barcelona/">Barcelona Urban Art</a>
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
        cards += f"""<article class="card"><a href="/cities/barcelona/gallery/{p['slug']}/"><picture><source type="image/webp" srcset="/assets/images/barcelona/responsive/{p['slug']}-480.webp 480w, /assets/images/barcelona/responsive/{p['slug']}-960.webp 960w" sizes="(max-width:800px) 92vw, 30vw"><img src="/assets/images/barcelona/{p['slug']}.jpg" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {attrs} decoding="async"></picture></a><div class="card-content"><h2>{link_barcelona(p['title'])}</h2><p>{link_barcelona(p['description'])}</p><a href="/cities/barcelona/gallery/{p['slug']}/">View photograph →</a></div></article>"""
    markup=head("Barcelona Urban Photography Gallery | Urban Arts News",description,canonical,image,hero["width"],hero["height"],schema)
    markup=markup.replace("</head>", '<link rel="next" href="https://urbanartsnews.com/cities/barcelona/gallery/page/2/"></head>')
    markup+=f"""<section class="hero"><small>Urban Arts News · {link_barcelona('Barcelona')} Gallery</small><h1>{link_barcelona('Barcelona')} <span class="accent">City Gallery</span></h1><p>{link_barcelona('Nine original photographs documenting Park Güell, the Gothic Quarter, Sagrada Família, the waterfront and the visual identity surrounding Urban Art Barcelona.')}</p></section><main class="container"><h2>{link_barcelona('Barcelona Urban Art News and City Photography')}</h2><p>{link_barcelona('This curated gallery connects Barcelona city photography with the wider Urban Arts News archive. Each photograph has its own indexable page, descriptive metadata and links to the Barcelona urban-art directory.')}</p><div class="grid">{cards}</div><p><a class="button" href="/cities/barcelona/gallery/page/2/">Barcelona Gallery · Page 2 →</a></p></main>"""+footer()
    (GALLERY_DIR/"index.html").write_text(markup,encoding="utf-8")

def generate_gallery_page2():
    page_dir = GALLERY_DIR / "page" / "2"
    page_dir.mkdir(parents=True, exist_ok=True)
    hero = ARTEVISTAS_IMAGES[0]
    canonical = BASE + "/cities/barcelona/gallery/page/2/"
    image = BASE + f"/assets/images/barcelona/{hero['slug']}.jpg"
    description = "Explore Barcelona urban culture and four documented views of Artevistas, a street art and contemporary art gallery with spaces in Born and the Gothic Quarter."
    item_list = [{"@type":"ListItem","position":i+1,"url":canonical+"#"+image_item["slug"],"name":image_item["title"]} for i,image_item in enumerate(ARTEVISTAS_IMAGES)]
    place_nodes = [{"@type":"ArtGallery","@id":canonical+"#"+key,"name":location["name"],"url":"https://www.artevistas.eu/","address":location["address"],"hasMap":location["maps"],"geo":{"@type":"GeoCoordinates","latitude":location["latitude"],"longitude":location["longitude"]}} for key,location in ARTEVISTAS_LOCATIONS.items()]
    image_nodes = []
    for image_item in ARTEVISTAS_IMAGES:
        location_ids = ["born", "gotic"] if image_item["location"] == "both" else [image_item["location"]]
        image_nodes.append({"@type":"ImageObject","@id":canonical+"#"+image_item["slug"],"name":image_item["title"],"description":image_item["description"],"caption":image_item["caption"],"contentUrl":BASE+"/assets/images/barcelona/"+image_item["slug"]+".webp","encodingFormat":"image/webp","width":image_item["width"],"height":image_item["height"],"contentLocation":[{"@id":canonical+"#"+location_id} for location_id in location_ids],"creditText":"Website screenshot courtesy of Artevistas Gallery. Editorial presentation by Urban Arts News.","copyrightNotice":"The website, logo, photographs and displayed artworks remain the property of their respective rights holders.","acquireLicensePage":"https://www.artevistas.eu/","creator":{"@type":"Organization","name":"Artevistas Gallery","url":"https://www.artevistas.eu/"},"publisher":{"@type":"Organization","name":"Urban Arts News","url":BASE+"/"},"keywords":image_item["keywords"],"representativeOfPage":False})
    schema={"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,"name":"Street Art Gallery Barcelona · Artevistas","description":description,"mainEntity":{"@type":"ItemList","numberOfItems":4,"itemListElement":item_list}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Barcelona","item":BASE+"/cities/barcelona/"},{"@type":"ListItem","position":3,"name":"Barcelona Gallery","item":BASE+"/cities/barcelona/gallery/"},{"@type":"ListItem","position":4,"name":"Page 2","item":canonical}]}] + place_nodes + image_nodes}
    artevistas_cards = ""
    for image_item in ARTEVISTAS_IMAGES:
        location_ids = ["born", "gotic"] if image_item["location"] == "both" else [image_item["location"]]
        map_links = " ".join(f'<a class="button" href="{esc(ARTEVISTAS_LOCATIONS[location_id]["maps"])}" rel="noopener" target="_blank">{esc(ARTEVISTAS_LOCATIONS[location_id]["name"])} Map →</a>' for location_id in location_ids)
        artevistas_cards += f"""<article class="card"><picture><source type="image/webp" srcset="/assets/images/barcelona/{image_item['slug']}.webp"><img src="/assets/images/barcelona/{image_item['slug']}.jpg" alt="{esc(image_item['alt'])}" width="{image_item['width']}" height="{image_item['height']}" loading="lazy" decoding="async"></picture><div class="card-content"><h2>{esc(image_item['title'])}</h2><p>{esc(image_item['caption'])}</p><p class="credit">Website screenshot courtesy of <a href="https://www.artevistas.eu/" rel="noopener" target="_blank"><strong>Artevistas Gallery</strong></a>. The website, photographs, logo and displayed artworks remain the property of their respective rights holders. Editorial presentation by <a href="https://urbanartsnews.com/"><strong>Urban Arts News</strong></a>.</p>{map_links}</div></article>"""
    markup=head("Street Art Gallery Barcelona · Artevistas | Urban Arts News",description,canonical,image,hero["width"],hero["height"],schema)
    markup=markup.replace("</head>", '<link rel="prev" href="https://urbanartsnews.com/cities/barcelona/gallery/"></head>')
    markup+=f"""<section class="hero"><small>Street Art Gallery Barcelona · ★★★★★</small><h1>Artevistas <span class="accent">Gallery Barcelona</span></h1><p>Four documented website views connect the Artevistas Born and Gòtic locations with contemporary art, collectible street art, exhibitions and Barcelona urban culture.</p></section><main class="container"><section><h2>Street Art Gallery Barcelona · Artevistas</h2><p>Urban Arts News presents four views of Artevistas Gallery in Barcelona, covering its gallery interiors, exhibitions and two central locations.</p><div class="grid">{artevistas_cards}</div></section><p><a class="button" href="/cities/barcelona/gallery/">← Barcelona Gallery · Page 1</a><a class="button" href="/subscribe/">Subscribe for Free →</a></p></main>"""+footer()
    (page_dir/"index.html").write_text(markup,encoding="utf-8")

def generate_redirects():
    """Preserve retired gallery URLs without serving the superseded photographs."""
    for old_slug, new_slug in REDIRECTS.items():
        target = f"/cities/barcelona/gallery/{new_slug}/"
        markup = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}{target}">
<meta http-equiv="refresh" content="0; url={target}"><title>Barcelona Gallery | Urban Arts News</title></head>
<body><p>This photograph has moved to <a href="{target}">the updated Barcelona gallery page</a>.</p></body></html>'''
        out = GALLERY_DIR / old_slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(markup, encoding="utf-8")

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
    for old_slug in REDIRECTS:
        old_url = BASE + f"/cities/barcelona/gallery/{old_slug}/"
        text = re.sub(r"\s*<url>\s*<loc>" + re.escape(old_url) + r"</loc>\s*</url>", "", text)
    urls=[BASE+"/cities/barcelona/gallery/", BASE+"/cities/barcelona/gallery/page/2/"]+[BASE+f"/cities/barcelona/gallery/{p['slug']}/" for p in ALL_PHOTOS]
    additions=""
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            additions+=f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    text=text.replace("</urlset>",additions+"</urlset>")
    path.write_text(text,encoding="utf-8")

def image_sitemap():
    rows=[]
    for p in ALL_PHOTOS:
        page=BASE+f"/cities/barcelona/gallery/{p['slug']}/"
        image=BASE+f"/assets/images/barcelona/{p['slug']}.jpg"
        rows.append(f"  <url><loc>{page}</loc><image:image><image:loc>{image}</image:loc></image:image></url>")
    page2=BASE+"/cities/barcelona/gallery/page/2/"
    for image_item in ARTEVISTAS_IMAGES:
        image=BASE+f"/assets/images/barcelona/{image_item['slug']}.webp"
        rows.append(f"  <url><loc>{page2}</loc><image:image><image:loc>{image}</image:loc><image:title>{esc(image_item['title'])}</image:title><image:caption>{esc(image_item['caption'])}</image:caption></image:image></url>")
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
    ensure_page2_metadata()
    responsive_images()
    for photo in ALL_PHOTOS: generate_detail(photo)
    generate_gallery()
    generate_gallery_page2()
    generate_redirects()
    patch_city_page()
    update_sitemap()
    image_sitemap()
    print("DONE Barcelona gallery: 18 photographs plus 4 Artevistas gallery images across 2 pages")

if __name__=="__main__":
    main()
