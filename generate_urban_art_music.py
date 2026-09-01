from pathlib import Path
import html
import json

BASE = "https://urbanartsnews.com"
OUT = Path("urban-art-music")

VIDEOS = [
    ("fJZd5IhTlsE", "DJ Key Song - Break in Tokyo 2012", "Breakdance Music"),
    ("VPh1w8ym1-s", "1City1Song (Official Videoclip)", "1City1Song"),
    ("UZzlMu7FStk", "The 45 King - 1, 2, 3 Hit It", "Real Hip Hop Lives!"),
    ("fwJp0Spgdno", "The 45 King - How U Doin'", "Real Hip Hop Lives!"),
    ("MzNj89E4BW8", "The 45 King - Hip Hop Music", "Real Hip Hop Lives!"),
    ("jrL_LzX5wv4", "House of Pain - Jump Around (Official 4K Music Video)", "HouseofPainVEVO"),
    ("kng_3yU5v-E", "Free Style Cutting", "Schoolly D"),
    ("ulBhSNEkMrM", "The Breaks", "Kurtis Blow"),
    ("nHFilDSZx6I", "Wild Style - Theme Rap 1", "Rare Groove Records"),
    ("SbYa7NBYyRc", "The Wanderer", "Dion"),
    ("Fm19n6L64hg", "King of the Surf Guitar", "Dick Dale"),
    ("MXB6T55oytE", "Miserlou", "Dick Dale"),
    ("VUosAGDM8Sg", "Die Fantastischen Vier - Die Da!?!", "Die Fantastischen Vier"),
    ("RGy5tp_CDU0", "Ice-T - New Jack Hustler", "UPROXX"),
    ("2Nn6bfYq8Ms", "Delinquent Habits - Return of the Tres", "Delinquent Habits"),
    ("bxN1xrLRvGU", "Spoonie Gee - Spoonin' Rap (1979)", "Official East Coast Rap"),
    ("HzjZQ4zRADQ", "Treacherous Three Fast Rap 1980", "jeffreywarley"),
    ("_uIWVrUcNs8", "Flightmode", "Alwa Alibi"),
    ("zKFqbyDR6M4", "Suprême NTM - That's My People", "NTMVEVO"),
    ("OEAjnqNF5n4", "Suprême NTM - Intro (Live in Paris 1998)", "NTMVEVO"),
    ("2tUYcInQ15k", "Suprême NTM - Check the Flow (Live in Paris 1998)", "NTMVEVO"),
    ("kgxKuRO21AU", "IAM - Planète Mars", "IAM Officiel"),
    ("Hc0Iy1nR-Q8", "Radio 200k - Im Huus", "agent007sui"),
    ("9OH7O9c-QeU", "Radio 200'000 - Hose", "reezer82"),
    ("n9FMvfvkBro", "Lou Monte - Che La Luna Mezzo Mare", "prendona"),
    ("_HEHD8UnF4E", "Electronic Music - Shuffle Dance", "Pixel Music"),
    ("1XS7OyZKLTc", "Suie Paparude - Pentru inimi", "Cat Music Gold"),
    ("PBsjggc5jHM", "Digital Underground - The Humpty Dance", "Tommy Boy"),
]

PAGES = [VIDEOS[:9], VIDEOS[9:18], VIDEOS[18:]]


def esc(value):
    return html.escape(str(value), quote=True)


def url_for(page_number):
    return f"{BASE}/urban-art-music/" if page_number == 1 else f"{BASE}/urban-art-music/page-{page_number}/"


def relative_url(page_number):
    return "/urban-art-music/" if page_number == 1 else f"/urban-art-music/page-{page_number}/"


def video_cards(videos, start_position):
    cards = []
    for offset, (video_id, title, author) in enumerate(videos):
        position = start_position + offset
        cards.append(f'''<article class="video-card">
<div class="player"><iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{esc(title)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
<div class="video-copy"><div class="number">Selection {position}</div><h2>{esc(title)}</h2><p>Featured on Urban Art Music · Video published by {esc(author)} on YouTube.</p><a href="https://www.youtube.com/watch?v={video_id}" rel="nofollow noopener" target="_blank">View on YouTube →</a></div>
</article>''')
    return "\n".join(cards)


def schema_for(page_number, videos):
    canonical = url_for(page_number)
    start = 1 if page_number == 1 else (page_number - 1) * 9 + 1
    items = []
    for offset, (video_id, title, author) in enumerate(videos):
        items.append({
            "@type": "ListItem",
            "position": start + offset,
            "item": {
                "@type": "VideoObject",
                "name": title,
                "description": f"{title}, featured in the Urban Art Music collection and published on YouTube by {author}.",
                "thumbnailUrl": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                "embedUrl": f"https://www.youtube-nocookie.com/embed/{video_id}",
                "contentUrl": f"https://www.youtube.com/watch?v={video_id}"
            }
        })
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": canonical + "#collection",
                "url": canonical,
                "name": "Urban Art Music" + (f" – Page {page_number}" if page_number > 1 else ""),
                "description": "An inspirational cross-genre music and video collection presented by Urban Arts News.",
                "mainEntity": {"@type": "ItemList", "numberOfItems": len(videos), "itemListElement": items},
                "inLanguage": "en"
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Urban Arts News", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Urban Art Music", "item": BASE + "/urban-art-music/"},
                    {"@type": "ListItem", "position": 3, "name": f"Page {page_number}", "item": canonical}
                ]
            }
        ]
    }


def navigation(page_number):
    links = []
    if page_number > 1:
        links.append(f'<a class="page-link" href="{relative_url(page_number - 1)}">← Previous</a>')
    for number in range(1, 4):
        cls = "page-link active" if number == page_number else "page-link"
        current = ' aria-current="page"' if number == page_number else ""
        links.append(f'<a class="{cls}" href="{relative_url(number)}"{current}>{number}</a>')
    if page_number < 3:
        links.append(f'<a class="page-link" href="{relative_url(page_number + 1)}">Next →</a>')
    return "".join(links)


def generate_page(page_number, videos):
    canonical = url_for(page_number)
    suffix = "" if page_number == 1 else f" – Page {page_number}"
    title = f"Urban Art Music{suffix} | Inspirational Music Videos"
    description = f"Explore page {page_number} of Urban Art Music: an inspirational cross-genre collection of music videos presented by Urban Arts News."
    first_video = videos[0][0]
    prev_link = f'<link rel="prev" href="{url_for(page_number - 1)}">' if page_number > 1 else ""
    next_link = f'<link rel="next" href="{url_for(page_number + 1)}">' if page_number < 3 else ""
    start = 1 if page_number == 1 else (page_number - 1) * 9 + 1
    end = start + len(videos) - 1
    schema = json.dumps(schema_for(page_number, videos), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    markup = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#090909">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canonical}">{prev_link}{next_link}
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Urban Arts News"><meta property="og:image" content="https://i.ytimg.com/vi/{first_video}/hqdefault.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="https://i.ytimg.com/vi/{first_video}/hqdefault.jpg">
<script type="application/ld+json">{schema}</script>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f3f3;color:#171717;font-family:Arial,Helvetica,sans-serif;line-height:1.6}}a{{color:inherit;text-decoration:none}}header{{background:#090909;color:#fff;padding:18px 5%;display:flex;justify-content:space-between;align-items:center}}.logo{{font-size:28px;font-weight:900;letter-spacing:-1px}}.logo span,.accent{{color:#ff5b21}}nav{{display:flex;gap:18px;align-items:center}}nav a{{font-size:13px;font-weight:800;text-transform:uppercase}}.hero{{background:#111;color:#fff;padding:80px 6%}}.eyebrow{{color:#ff5b21;font-size:13px;font-weight:900;letter-spacing:1.4px;text-transform:uppercase}}.hero h1{{max-width:1050px;font-size:clamp(44px,7vw,86px);line-height:.94;letter-spacing:-4px;text-transform:uppercase;margin:13px 0 22px}}.hero p{{max-width:880px;color:#ccc;font-size:20px}}.curator{{margin-top:22px;font-weight:800}}.curator a{{color:#ff5b21}}.container{{width:min(1300px,92%);margin:55px auto}}.intro{{max-width:900px;margin-bottom:38px}}.intro h2{{font-size:clamp(28px,4vw,44px);line-height:1.08;margin:0 0 12px}}.intro p{{font-size:18px;color:#555}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:25px}}.video-card{{background:#fff;box-shadow:0 7px 22px rgba(0,0,0,.09);overflow:hidden}}.player{{position:relative;aspect-ratio:16/9;background:#000}}.player iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}.video-copy{{padding:22px}}.number{{color:#ff5b21;font-size:12px;font-weight:900;text-transform:uppercase}}.video-copy h2{{font-size:21px;line-height:1.2;margin:7px 0 10px}}.video-copy p{{color:#666;font-size:14px}}.video-copy>a{{font-size:13px;font-weight:900;text-transform:uppercase;color:#ff5b21}}.pagination{{display:flex;justify-content:center;align-items:center;gap:9px;flex-wrap:wrap;margin:50px 0 10px}}.page-link{{background:#111;color:#fff;padding:11px 16px;font-weight:900}}.page-link.active{{background:#ff5b21}}.about{{background:#fff;border-left:5px solid #ff5b21;padding:32px;margin-top:50px}}.about h2{{margin:0 0 8px}}.about p{{margin:0;color:#555}}footer{{background:#090909;color:#888;text-align:center;padding:35px;margin-top:65px}}@media(max-width:950px){{.grid{{grid-template-columns:repeat(2,1fr)}}header{{display:block}}nav{{margin-top:12px;flex-wrap:wrap}}}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}.hero{{padding:58px 6%}}.hero h1{{letter-spacing:-2px}}}}
</style></head><body>
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/">Home</a><a href="/artists/">Artists</a><a href="/urban-art-cities/">Cities</a><a href="/urban-art-music/">Urban Art Music</a><a href="/subscribe/">Subscribe</a></nav></header>
<section class="hero"><div class="eyebrow">Inspirational listening · Page {page_number} of 3</div><h1>Urban Art <span class="accent">Music</span></h1><p>A cross-genre selection of music connected with creativity, movement, city culture and the energy behind urban art.</p></section>
<main class="container"><section class="intro"><h2>Urban Art Music Videos {start}–{end}</h2><p>Play every video directly on Urban Arts News or open the original publication on YouTube. Artist-curated collections will be introduced separately in the future.</p></section>
<section class="grid" aria-label="Urban Art Music video collection">{video_cards(videos, start)}</section>
<nav class="pagination" aria-label="Urban Art Music pages">{navigation(page_number)}</nav>
<section class="about"><h2>Urban Art Music on Urban Arts News</h2><p>This artist-curated music collection is part of <a href="{BASE}/"><strong>Urban Arts News</strong></a>, an international platform for street art, contemporary urban artists, city culture and creative discovery.</p></section></main>
<footer>© 2026 Urban Arts News · Urban Art Music · Inspirational Music Videos</footer></body></html>'''
    target = OUT if page_number == 1 else OUT / f"page-{page_number}"
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(markup, encoding="utf-8")


def update_sitemap():
    sitemap = Path("sitemap.xml")
    text = sitemap.read_text(encoding="utf-8")
    for page_number in range(1, 4):
        url = url_for(page_number)
        if f"<loc>{url}</loc>" not in text:
            text = text.replace("</urlset>", f"  <url>\n    <loc>{url}</loc>\n  </url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def main():
    for page_number, videos in enumerate(PAGES, start=1):
        generate_page(page_number, videos)
    update_sitemap()
    print(f"Generated 3 Urban Art Music pages with {len(VIDEOS)} videos")


if __name__ == "__main__":
    main()
