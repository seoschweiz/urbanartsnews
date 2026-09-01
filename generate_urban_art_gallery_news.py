from pathlib import Path
from urllib.parse import quote_plus
import html, json, unicodedata
from PIL import Image

BASE="https://urbanartsnews.com"
ROOT=Path("urban-art-gallery-news")
ASSETS=Path("assets/images/urban-art-gallery-news")
RESPONSIVE=ASSETS/"responsive"

PHOTOS=[
 {"n":1,"slug":"group-exhibition-gallery-wall","title":"Urban Art Gallery News: Group Exhibition Wall","description":"A spacious gallery presents a carefully arranged wall of framed works for visitors to explore together. Urban art galleries give group exhibitions a professional setting where different artists, techniques and perspectives can enter into dialogue. They also create opportunities for openings, guided visits and community events that make contemporary culture more accessible.","meta":"Urban Art Gallery News featuring a group exhibition wall and the positive role of galleries in events and public access.","alt":"Group exhibition wall inside a spacious urban art gallery"},
 {"n":2,"slug":"visitors-contemporary-blue-art-exhibition","title":"Urban Art Gallery News: Visitors at a Contemporary Exhibition","description":"Visitors engage with a sequence of bold blue artworks in a bright contemporary gallery. Urban art galleries turn exhibitions into shared experiences through curatorial interpretation, guided tours and direct conversations about artistic ideas. Artist talks and opening events can connect creators with new audiences while encouraging informed cultural exchange.","meta":"Urban Art Gallery News with visitors viewing contemporary blue artworks during a public gallery exhibition.","alt":"Visitors viewing blue contemporary artworks in an urban art gallery"},
 {"n":3,"slug":"colourful-art-editions-gallery-display","title":"Urban Art Gallery News: Colourful Art Editions and Displays","description":"Colourful illustrations and art editions create an energetic display beside a larger exhibition space. Urban art galleries can support emerging artists by presenting accessible works, limited editions and experimental formats to new collectors. Pop-up events and curated sales also strengthen the independent creative economy without separating art from public engagement.","meta":"Urban Art Gallery News featuring colourful editions and displays that support emerging artists and collectors.","alt":"Colourful art editions displayed inside a contemporary urban gallery"},
 {"n":4,"slug":"independent-contemporary-gallery-exhibition","title":"Urban Art Gallery News: Independent Contemporary Exhibition","description":"An independent white-walled gallery brings together paintings and sculptural works in an open exhibition. Urban art galleries provide flexible platforms for solo shows, group projects and site-responsive installations that may not fit conventional institutions. Their openings, workshops and neighbourhood events help artists build lasting relationships with local audiences.","meta":"Urban Art Gallery News exploring an independent contemporary exhibition with paintings and installations.","alt":"Independent contemporary urban art gallery with visitors and paintings"},
 {"n":5,"slug":"visitor-reflective-black-white-gallery","title":"Urban Art Gallery News: A Reflective Gallery Encounter","description":"A moving visitor becomes part of a quiet black-and-white gallery scene surrounded by framed artworks. Urban art galleries offer time and space for focused encounters that contrast with the speed of everyday visual culture. Thoughtful exhibitions, educational programs and slow-looking events can deepen attention, empathy and personal interpretation.","meta":"Urban Art Gallery News showing a reflective visitor experience among framed black-and-white artworks.","alt":"Visitor moving through a black-and-white urban art gallery exhibition"},
 {"n":6,"slug":"modern-gallery-mixed-art-exhibition","title":"Urban Art Gallery News: Modern Mixed-Art Exhibition Space","description":"A luminous modern gallery displays paintings, sculpture and installation across a generous open floor. Urban art galleries can bring multiple media and generations of artists into one coherent curatorial program. Exhibition openings, performances and public discussions turn these spaces into active cultural meeting points rather than static display rooms.","meta":"Urban Art Gallery News featuring a modern exhibition space with paintings, sculpture and installation art.","alt":"Modern urban art gallery displaying paintings sculpture and installation"},
 {"n":7,"slug":"industrial-space-urban-art-gallery","title":"Urban Art Gallery News: Exhibition in an Industrial Space","description":"A converted industrial interior provides an atmospheric setting for photography, illustration and contemporary artworks. Urban art galleries often give former commercial buildings a new civic purpose through adaptive reuse and cultural programming. Exhibitions, creative workshops and evening events can reactivate neighbourhoods while preserving their architectural character.","meta":"Urban Art Gallery News inside a converted industrial exhibition space supporting culture and neighbourhood renewal.","alt":"Urban art gallery exhibition inside a converted industrial building"},
 {"n":8,"slug":"curated-painting-exhibition-evening","title":"Urban Art Gallery News: Curated Painting Exhibition","description":"A visitor studies expressive paintings in a warmly lit gallery exhibition. Urban art galleries use thoughtful curation to connect individual works with wider social, historical and visual themes. Vernissages, collector previews and artist conversations help audiences understand the work while creating sustainable opportunities for artists.","meta":"Urban Art Gallery News with a visitor exploring a curated painting exhibition in a warmly lit space.","alt":"Visitor viewing expressive paintings in a curated urban art gallery"},
 {"n":9,"slug":"intimate-gallery-art-viewing","title":"Urban Art Gallery News: Intimate Art Viewing Space","description":"A visitor pauses before a small group of framed works in an intimate gallery room. Smaller urban art galleries encourage close attention and meaningful encounters between artworks, artists and audiences. Their focused exhibitions and personal events can introduce overlooked practices while building trust within a creative community.","meta":"Urban Art Gallery News showing an intimate viewing space for focused exhibitions and community connections.","alt":"Visitor viewing framed works in an intimate urban art gallery"},
]

REGIONAL_FEEDS=[
 ("Urban Art Gallery News Spain","urban art gallery Spain","ES"),
 ("Urban Art Gallery News Barcelona","urban art gallery Barcelona","ES"),
 ("Urban Art Gallery News Los Angeles","urban art gallery Los Angeles","US"),
 ("Urban Art Gallery News California","urban art gallery California","US"),
 ("Urban Art Gallery News Argentina","urban art gallery Argentina","AR"),
 ("Urban Art Gallery News Buenos Aires","urban art gallery Buenos Aires","AR"),
]

def esc(v): return html.escape(str(v),quote=True)
def feed_url(query,country): return f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en&gl={country}&ceid={country}:en"

def seo_exif(photo):
 exif=Image.Exif(); full=f"{photo['title']}. {photo['description']}"
 exif[270]=unicodedata.normalize("NFKD",full).encode("ascii","ignore").decode("ascii")
 exif[315]="Licensed stock contributor"; exif[33432]="Rights remain with the contributor; licensed for editorial website use"
 exif[40091]=(photo["title"]+"\0").encode("utf-16le"); exif[40092]=(full+"\0").encode("utf-16le")
 exif[40094]=("Urban Art Gallery News; Urban Art Exhibitions; Gallery Events; Contemporary Art\0").encode("utf-16le")
 return exif

def prepare_images():
 RESPONSIVE.mkdir(parents=True,exist_ok=True)
 for p in PHOTOS:
  src=ASSETS/f"{p['slug']}.jpg"
  with Image.open(src) as original:
   image=original.convert("RGB"); p["width"],p["height"]=image.size
   image.save(src,"JPEG",quality=90,optimize=True,progressive=True,exif=seo_exif(p))
   for width in (480,960):
    height=round(image.height*width/image.width)
    image.resize((width,height),Image.Resampling.LANCZOS).save(RESPONSIVE/f"{p['slug']}-{width}.webp","WEBP",quality=82,method=6)

def schema(photo=None):
 canonical=BASE+"/urban-art-gallery-news/"+(f"{photo['slug']}/" if photo else "")
 if photo:
  image=BASE+f"/assets/images/urban-art-gallery-news/{photo['slug']}.jpg"
  return {"@context":"https://schema.org","@graph":[{"@type":"WebPage","@id":canonical+"#page","url":canonical,"name":photo["title"],"description":photo["meta"],"primaryImageOfPage":{"@id":canonical+"#image"}},{"@type":"ImageObject","@id":canonical+"#image","name":photo["title"],"caption":photo["description"],"description":photo["meta"],"contentUrl":image,"encodingFormat":"image/jpeg","width":photo["width"],"height":photo["height"],"creditText":"Licensed stock contributor","copyrightNotice":"Rights remain with the respective contributor; no ownership is claimed by Urban Arts News"},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Urban Arts News","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Urban Art Gallery News","item":BASE+"/urban-art-gallery-news/"},{"@type":"ListItem","position":3,"name":photo["title"],"item":canonical}]}]}
 items=[{"@type":"ListItem","position":i+1,"url":BASE+f"/urban-art-gallery-news/{p['slug']}/","name":p["title"]} for i,p in enumerate(PHOTOS)]
 return {"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","@id":canonical+"#collection","url":canonical,"name":"Urban Art Gallery News Register","description":"Urban Art Gallery News register for exhibitions, events, galleries and contemporary visual culture.","mainEntity":{"@type":"ItemList","numberOfItems":9,"itemListElement":items}},{"@type":"Organization","name":"Urban Arts News","url":BASE+"/","logo":BASE+"/favicon.svg"}]}

CSS="""*{box-sizing:border-box}body{margin:0;background:#f3f3f1;color:#171717;font-family:Arial,sans-serif;line-height:1.65}a{color:inherit}header{background:#080808;color:#fff;padding:18px 5%;display:flex;justify-content:space-between;align-items:center}.logo{text-decoration:none;font-size:27px;font-weight:900}.logo span,.accent{color:#ff5b21}nav a{margin-left:17px;font-size:13px;font-weight:800;text-transform:uppercase}.hero{background:#111;color:#fff;padding:72px 6%}.hero h1{font-size:clamp(40px,7vw,78px);line-height:.98;letter-spacing:-3px;margin:8px 0 20px;text-transform:uppercase}.hero p{max-width:900px;color:#ccc;font-size:19px}.container{width:min(1320px,92%);margin:48px auto}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.card,.photo,.feeds article{background:#fff;box-shadow:0 6px 22px #00000012}.card img{display:block;width:100%;height:310px;object-fit:cover}.copy,.caption{padding:22px}.copy h2{font-size:20px;line-height:1.25;margin:0 0 9px}.photo{padding:clamp(14px,4vw,42px)}.photo img{display:block;width:100%;height:auto}.caption{max-width:960px;margin:auto}.caption h1{font-size:clamp(30px,5vw,52px);line-height:1.08}.button{display:inline-block;background:#ff5b21;color:#fff;text-decoration:none;padding:12px 17px;font-weight:900;text-transform:uppercase}.feeds{border-top:5px solid #ff5b21;padding-top:30px}.feed-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.feeds article{padding:18px}.feeds a{font-weight:900}.credit{font-size:13px;color:#777;border-top:1px solid #ddd;padding-top:14px}footer{background:#080808;color:#999;text-align:center;padding:34px;margin-top:55px}@media(max-width:800px){header{display:block}nav{margin-top:12px}nav a{margin:0 12px 0 0}.grid,.feed-grid{grid-template-columns:1fr}.card img{height:auto}}"""

def head(title,description,canonical,image,schema_data):
 return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="keywords" content="Urban Art Gallery News, urban art galleries, art exhibitions, gallery events, contemporary art news">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="googlebot" content="index,follow,max-image-preview:large"><meta name="bingbot" content="index,follow"><meta name="yandex" content="index,follow"><meta name="news_keywords" content="Urban Art Gallery News, exhibitions, events, contemporary art">
<link rel="canonical" href="{canonical}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" title="Urban Art Gallery News RSS" href="/urban-art-gallery-news/feed.xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="Urban Arts News"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:secure_url" content="{image}"><meta property="og:image:type" content="image/jpeg"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{image}">
<script type="application/ld+json">{json.dumps(schema_data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')}</script><style>{CSS}</style></head><body><header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/urban-art-gallery-news/">Gallery News</a><a href="/urban-art-cities/">Cities</a><a href="/artists/">Artists</a></nav></header>'''

def footer(): return '<footer>© 2026 Urban Arts News · Urban Art Gallery News · Exhibitions and Events</footer></body></html>'

def generate():
 ROOT.mkdir(parents=True,exist_ok=True); hero=PHOTOS[1]; cards=""
 for i,p in enumerate(PHOTOS):
  image=f"/assets/images/urban-art-gallery-news/{p['slug']}.jpg"; url=f"/urban-art-gallery-news/{p['slug']}/"; attrs='loading="eager" fetchpriority="high"' if i==0 else 'loading="lazy"'
  cards+=f'''<article class="card"><a href="{url}"><picture><source type="image/webp" srcset="/assets/images/urban-art-gallery-news/responsive/{p['slug']}-480.webp 480w, /assets/images/urban-art-gallery-news/responsive/{p['slug']}-960.webp 960w"><img src="{image}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {attrs}></picture></a><div class="copy"><h2><a href="{url}">{esc(p['title'])}</a></h2><p>{esc(p['description'])}</p><a class="button" href="{url}">View gallery story</a></div></article>'''
  canonical=BASE+url; full_image=BASE+image; markup=head(p["title"]+" | Urban Arts News",p["meta"],canonical,full_image,schema(p))
  markup+=f'''<main class="container"><article class="photo"><picture><source type="image/webp" media="(max-width:600px)" srcset="/assets/images/urban-art-gallery-news/responsive/{p['slug']}-480.webp"><source type="image/webp" media="(max-width:1100px)" srcset="/assets/images/urban-art-gallery-news/responsive/{p['slug']}-960.webp"><img src="{image}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" loading="eager" fetchpriority="high"></picture><div class="caption"><h1>{esc(p['title'])}</h1><p>{esc(p['description'])}</p><p>Urban art galleries create positive opportunities for exhibitions, events, artist development and meaningful public participation in contemporary culture.</p><p class="credit">Licensed stock photograph. Rights remain with the respective contributor; Urban Arts News does not claim ownership.</p><a class="button" href="/urban-art-gallery-news/">Urban Art Gallery News Register</a></div></article></main>'''+footer()
  out=ROOT/p["slug"];out.mkdir(parents=True,exist_ok=True);(out/"index.html").write_text(markup,encoding="utf-8")
 feed_cards=''.join(f'<article><h3>{esc(label)}</h3><p>English Google News RSS search covering exhibitions, galleries and events in this region.</p><a href="{esc(feed_url(query,country))}" rel="nofollow external">Open RSS feed →</a></article>' for label,query,country in REGIONAL_FEEDS)
 canonical=BASE+"/urban-art-gallery-news/"; image=BASE+f"/assets/images/urban-art-gallery-news/{hero['slug']}.jpg"; desc="Urban Art Gallery News register covering exhibitions, events, gallery culture and the positive role of contemporary art spaces."
 markup=head("Urban Art Gallery News Register | Exhibitions and Events",desc,canonical,image,schema())
 markup+=f'''<section class="hero"><small class="accent">Exhibitions · Events · Contemporary Culture</small><h1>Urban Art <span class="accent">Gallery News</span></h1><p>An international visual register exploring how urban art galleries support exhibitions, artist talks, openings, workshops, cultural participation and creative communities.</p></section><main class="container"><h2>Urban Art Gallery News, Exhibitions and Events</h2><p>Discover gallery environments and the positive role they play in presenting artists, connecting audiences and building sustainable cultural networks.</p><div class="grid">{cards}</div><section class="feeds"><h2>Urban Art Gallery News: English Regional RSS Feeds</h2><p>Live Google News RSS searches for regional gallery exhibitions, openings, events and contemporary art coverage.</p><div class="feed-grid">{feed_cards}</div></section></main>'''+footer();(ROOT/"index.html").write_text(markup,encoding="utf-8")

def data_files():
 data={"name":"Urban Art Gallery News Register","url":BASE+"/urban-art-gallery-news/","language":"en","updated":"2026-09-01","items":[{"position":i+1,"title":p["title"],"description":p["description"],"url":BASE+f"/urban-art-gallery-news/{p['slug']}/","image":BASE+f"/assets/images/urban-art-gallery-news/{p['slug']}.jpg","alt":p["alt"]} for i,p in enumerate(PHOTOS)],"regional_google_news_rss":[{"title":l,"url":feed_url(q,c)} for l,q,c in REGIONAL_FEEDS]}
 (ROOT/"urban-art-gallery-news.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 items=''.join(f'<item><title>{esc(p["title"])}</title><link>{BASE}/urban-art-gallery-news/{p["slug"]}/</link><guid>{BASE}/urban-art-gallery-news/{p["slug"]}/</guid><description>{esc(p["meta"])}</description></item>' for p in PHOTOS)
 (ROOT/"feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Urban Art Gallery News</title><link>{BASE}/urban-art-gallery-news/</link><description>Exhibitions, events and contemporary gallery culture.</description><language>en</language>{items}</channel></rss>\n',encoding="utf-8")
 rows=''.join(f'<url><loc>{BASE}/urban-art-gallery-news/{p["slug"]}/</loc><image:image><image:loc>{BASE}/assets/images/urban-art-gallery-news/{p["slug"]}.jpg</image:loc><image:title>{esc(p["title"])}</image:title><image:caption>{esc(p["meta"])}</image:caption></image:image></url>' for p in PHOTOS)
 Path("image-sitemap-urban-art-gallery-news.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{rows}</urlset>\n',encoding="utf-8")

def update_site():
 sitemap=Path("sitemap.xml"); text=sitemap.read_text(); urls=[BASE+"/urban-art-gallery-news/"]+[BASE+f"/urban-art-gallery-news/{p['slug']}/" for p in PHOTOS]
 additions=''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls if f'<loc>{u}</loc>' not in text); sitemap.write_text(text.replace('</urlset>',additions+'</urlset>'))
 robots=Path("robots.txt");text=robots.read_text();line=f"Sitemap: {BASE}/image-sitemap-urban-art-gallery-news.xml"; robots.write_text(text.rstrip()+("\n"+line if line not in text else "")+"\n")

if __name__=="__main__":
 prepare_images();generate();data_files();update_site();print("DONE Urban Art Gallery News register")
