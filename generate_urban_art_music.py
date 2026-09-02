from pathlib import Path
import html
import json
import re

BASE = "https://urbanartsnews.com"
OUT = Path("urban-art-music")
GENERATOR_VERSION = "2026-09-02-multilingual-video-pages.2"

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
]

PAGES = [VIDEOS[:9], VIDEOS[9:18], VIDEOS[18:]]

LANGUAGES = {
    "en": {"name": "English", "dir": "ltr", "watch": "View on YouTube", "back": "Back to Urban Art Music", "languages": "Explore this video in 14 languages", "label": "Urban Art Music Selection", "about": "Why urban music matters", "meta": "Urban music can inspire street art, graffiti and urban artists in cities around the world."},
    "ca": {"name": "Català", "dir": "ltr", "watch": "Veure a YouTube", "back": "Tornar a Urban Art Music", "languages": "Explora aquest vídeo en 14 idiomes", "label": "Selecció d'Urban Art Music", "about": "Per què importa la música urbana", "meta": "La música urbana pot inspirar l'art de carrer, el grafiti i els artistes urbans de ciutats de tot el món."},
    "es": {"name": "Español", "dir": "ltr", "watch": "Ver en YouTube", "back": "Volver a Urban Art Music", "languages": "Explora este vídeo en 14 idiomas", "label": "Selección de Urban Art Music", "about": "Por qué importa la música urbana", "meta": "La música urbana puede inspirar el arte callejero, el grafiti y a artistas urbanos de ciudades de todo el mundo."},
    "de": {"name": "Deutsch", "dir": "ltr", "watch": "Auf YouTube ansehen", "back": "Zurück zu Urban Art Music", "languages": "Dieses Video in 14 Sprachen entdecken", "label": "Urban Art Music Auswahl", "about": "Warum urbane Musik wichtig ist", "meta": "Urbane Musik kann Street Art, Graffiti und urbane Künstler in Städten auf der ganzen Welt inspirieren."},
    "fr": {"name": "Français", "dir": "ltr", "watch": "Voir sur YouTube", "back": "Retour à Urban Art Music", "languages": "Découvrir cette vidéo en 14 langues", "label": "Sélection Urban Art Music", "about": "Pourquoi la musique urbaine compte", "meta": "La musique urbaine peut inspirer le street art, le graffiti et les artistes urbains dans les villes du monde entier."},
    "it": {"name": "Italiano", "dir": "ltr", "watch": "Guarda su YouTube", "back": "Torna a Urban Art Music", "languages": "Scopri questo video in 14 lingue", "label": "Selezione Urban Art Music", "about": "Perché la musica urbana è importante", "meta": "La musica urbana può ispirare street art, graffiti e artisti urbani nelle città di tutto il mondo."},
    "pt": {"name": "Português", "dir": "ltr", "watch": "Ver no YouTube", "back": "Voltar a Urban Art Music", "languages": "Explore este vídeo em 14 idiomas", "label": "Seleção Urban Art Music", "about": "Porque a música urbana importa", "meta": "A música urbana pode inspirar street art, graffiti e artistas urbanos em cidades de todo o mundo."},
    "sq": {"name": "Shqip", "dir": "ltr", "watch": "Shiko në YouTube", "back": "Kthehu te Urban Art Music", "languages": "Eksploro këtë video në 14 gjuhë", "label": "Përzgjedhje Urban Art Music", "about": "Pse ka rëndësi muzika urbane", "meta": "Muzika urbane mund të frymëzojë artin e rrugës, grafitin dhe artistët urbanë në qytete në mbarë botën."},
    "ja": {"name": "日本語", "dir": "ltr", "watch": "YouTubeで見る", "back": "Urban Art Musicへ戻る", "languages": "この動画を14言語で見る", "label": "Urban Art Music セレクション", "about": "アーバンミュージックの価値", "meta": "アーバンミュージックは、世界中の都市でストリートアート、グラフィティ、アーバンアーティストを刺激します。"},
    "ar": {"name": "العربية", "dir": "rtl", "watch": "المشاهدة على يوتيوب", "back": "العودة إلى Urban Art Music", "languages": "استكشف هذا الفيديو بـ14 لغة", "label": "مختارات Urban Art Music", "about": "لماذا تهم الموسيقى الحضرية", "meta": "يمكن للموسيقى الحضرية أن تلهم فن الشارع والغرافيتي والفنانين الحضريين في مدن العالم."},
    "ru": {"name": "Русский", "dir": "ltr", "watch": "Смотреть на YouTube", "back": "Назад к Urban Art Music", "languages": "Смотреть это видео на 14 языках", "label": "Подборка Urban Art Music", "about": "Почему важна городская музыка", "meta": "Городская музыка вдохновляет стрит-арт, граффити и городских художников в городах по всему миру."},
    "sv": {"name": "Svenska", "dir": "ltr", "watch": "Visa på YouTube", "back": "Tillbaka till Urban Art Music", "languages": "Utforska videon på 14 språk", "label": "Urban Art Music-utval", "about": "Varför urban musik är viktig", "meta": "Urban musik kan inspirera gatukonst, graffiti och urbana konstnärer i städer över hela världen."},
    "ko": {"name": "한국어", "dir": "ltr", "watch": "YouTube에서 보기", "back": "Urban Art Music으로 돌아가기", "languages": "이 동영상을 14개 언어로 보기", "label": "Urban Art Music 셀렉션", "about": "도시 음악의 가치", "meta": "도시 음악은 전 세계 도시의 스트리트 아트, 그래피티와 도시 예술가들에게 영감을 줄 수 있습니다."},
    "hi": {"name": "हिन्दी", "dir": "ltr", "watch": "YouTube पर देखें", "back": "Urban Art Music पर वापस जाएँ", "languages": "इस वीडियो को 14 भाषाओं में देखें", "label": "Urban Art Music चयन", "about": "शहरी संगीत क्यों महत्वपूर्ण है", "meta": "शहरी संगीत दुनिया भर के शहरों में स्ट्रीट आर्ट, ग्रैफिटी और शहरी कलाकारों को प्रेरित कर सकता है।"},
}

SUBSCRIBE_LABELS = {
    code: "Subscribe 4 Urban News" for code in LANGUAGES
}

MOTIVATION_TEXTS = [
    "Urban music turns rhythm into creative momentum, giving street artists and graffiti writers fresh energy for ideas that can travel far beyond one city.",
    "A powerful beat can open a space for experimentation, helping urban artists translate movement, memory and city life into visual expression.",
    "Music and street art share an instinct for freedom: both can transform everyday public space into a place of surprise, identity and imagination.",
    "Motivating urban music supports the creative flow behind murals, lettering and independent art, connecting artists from Barcelona to cities worldwide.",
    "Rhythm can become a creative companion during long painting sessions, encouraging focus, courage and the confidence to try something new.",
    "Urban sound carries the voices of neighbourhoods and helps visual artists turn local experience into work that can speak across borders.",
    "When music creates momentum, a blank wall, recycled surface or overlooked corner can begin to feel like an invitation to create.",
    "Hip-hop culture has long connected sound, movement, graffiti and community, showing how different art forms can strengthen one another.",
    "An inspiring track can shift the mood of a creative process and help an artist discover unexpected colours, forms, letters and gestures.",
    "Urban music links personal expression with collective energy, reminding creators that street art can belong to a worldwide cultural conversation.",
    "The pulse of music can encourage spontaneous decisions, giving graffiti and mural work the movement and immediacy of a live performance.",
    "Creative music offers more than background sound: it can shape atmosphere, sustain attention and help visual ideas grow into finished urban artworks.",
    "From Badalona and Barcelona to Buenos Aires and beyond, music helps artists feel connected to a larger network of independent creativity.",
    "Strong rhythms can support resilience and motivation, especially when urban artists are developing demanding work in changing public environments.",
    "Music can turn solitude into connection, accompanying an individual artist while linking the work to audiences and creative communities worldwide.",
    "The exchange between sound and image encourages new perspectives, allowing graffiti, street art and music to continually reinvent urban culture.",
    "A memorable song can become part of an artwork's creative history, preserving the mood, energy and ideas present while the piece was made.",
    "Urban music invites movement, and that sense of movement can appear in flowing letters, dynamic characters and expansive mural compositions.",
    "Independent music and independent street art share a valuable spirit: each can create visibility for voices outside traditional cultural spaces.",
    "Listening across genres can widen an artist's visual vocabulary and inspire combinations that would not emerge from a single cultural influence.",
    "Music gives creative work an emotional tempo, helping artists move between reflection, experimentation and decisive action.",
    "The energy of urban music can make public-space creativity feel possible, immediate and connected to everyday life rather than distant institutions.",
    "Sound can activate memory and place, helping artists express how a neighbourhood feels as well as how it looks.",
    "A motivating soundtrack can support creative risk, encouraging urban artists to explore unfamiliar materials, scales and visual languages.",
    "Urban art and music both build bridges between generations, carrying cultural knowledge forward while leaving room for new interpretations.",
    "The right rhythm can bring clarity to a complex idea and help an artist organise colour, composition and movement with greater confidence.",
    "Across continents and languages, urban music can unite people who value graffiti, street art and the creative transformation of shared spaces.",
]


def esc(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "urban-art-music-video"


def video_slug(video):
    video_id, title, _author = video
    return f"{slugify(title)}-{video_id.lower()}"


def detail_relative_url(language, video):
    prefix = "" if language == "en" else f"/{language}"
    return f"{prefix}/urban-art-music/{video_slug(video)}/"


def detail_url(language, video):
    return BASE + detail_relative_url(language, video)


def hreflang_links(video):
    links = []
    for code in LANGUAGES:
        links.append(f'<link rel="alternate" hreflang="{code}" href="{esc(detail_url(code, video))}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{esc(detail_url("en", video))}">')
    return "".join(links)


def language_buttons(video, current_language):
    links = []
    for code, config in LANGUAGES.items():
        current = ' aria-current="page"' if code == current_language else ""
        links.append(
            f'<a class="language-button" lang="{code}" href="{esc(detail_relative_url(code, video))}"{current}>{esc(config["name"])}</a>'
        )
    return "".join(links)


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
<div class="video-copy"><div class="number">Selection {position}</div><h2><a href="{esc(detail_relative_url('en', (video_id, title, author)))}">{esc(title)}</a></h2><p>{esc(MOTIVATION_TEXTS[position - 1])}</p><div class="video-actions"><a href="{esc(detail_relative_url('en', (video_id, title, author)))}">Explore New Urban Music Video →</a><a class="subscribe-action" href="/subscribe/">Subscribe 4 Urban News →</a></div></div>
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
*{{box-sizing:border-box}}body{{margin:0;background:#f3f3f3;color:#171717;font-family:Arial,Helvetica,sans-serif;line-height:1.6}}a{{color:inherit;text-decoration:none}}header{{background:#090909;color:#fff;padding:18px 5%;display:flex;justify-content:space-between;align-items:center}}.logo{{font-size:28px;font-weight:900;letter-spacing:-1px}}.logo span,.accent{{color:#ff5b21}}nav{{display:flex;gap:18px;align-items:center}}nav a{{font-size:13px;font-weight:800;text-transform:uppercase}}.hero{{background:#111;color:#fff;padding:80px 6%}}.eyebrow{{color:#ff5b21;font-size:13px;font-weight:900;letter-spacing:1.4px;text-transform:uppercase}}.hero h1{{max-width:1050px;font-size:clamp(44px,7vw,86px);line-height:.94;letter-spacing:-4px;text-transform:uppercase;margin:13px 0 22px}}.hero p{{max-width:880px;color:#ccc;font-size:20px}}.curator{{margin-top:22px;font-weight:800}}.curator a{{color:#ff5b21}}.container{{width:min(1300px,92%);margin:55px auto}}.intro{{max-width:900px;margin-bottom:38px}}.intro h2{{font-size:clamp(28px,4vw,44px);line-height:1.08;margin:0 0 12px}}.intro p{{font-size:18px;color:#555}}.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:25px}}.video-card{{background:#fff;box-shadow:0 7px 22px rgba(0,0,0,.09);overflow:hidden}}.player{{position:relative;aspect-ratio:16/9;background:#000}}.player iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}.video-copy{{padding:22px}}.number{{color:#ff5b21;font-size:12px;font-weight:900;text-transform:uppercase}}.video-copy h2{{font-size:21px;line-height:1.2;margin:7px 0 10px}}.video-copy p{{color:#666;font-size:14px}}.video-actions{{display:flex;gap:9px;flex-wrap:wrap;margin-top:15px}}.video-actions a{{font-size:12px;font-weight:900;text-transform:uppercase;color:#fff;background:#111;padding:10px 12px}}.video-actions .subscribe-action{{background:#ff5b21}}.pagination{{display:flex;justify-content:center;align-items:center;gap:9px;flex-wrap:wrap;margin:50px 0 10px}}.page-link{{background:#111;color:#fff;padding:11px 16px;font-weight:900}}.page-link.active{{background:#ff5b21}}.about{{background:#fff;border-left:5px solid #ff5b21;padding:32px;margin-top:50px}}.about h2{{margin:0 0 8px}}.about p{{margin:0;color:#555}}footer{{background:#090909;color:#888;text-align:center;padding:35px;margin-top:65px}}@media(max-width:950px){{.grid{{grid-template-columns:repeat(2,1fr)}}header{{display:block}}nav{{margin-top:12px;flex-wrap:wrap}}}}@media(max-width:650px){{.grid{{grid-template-columns:1fr}}.hero{{padding:58px 6%}}.hero h1{{letter-spacing:-2px}}}}
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


def generate_video_page(video, position, language):
    video_id, title, author = video
    config = LANGUAGES[language]
    canonical = detail_url(language, video)
    paragraph = MOTIVATION_TEXTS[position - 1] if language == "en" else config["meta"]
    meta_description = f'{title}. {config["meta"]}'
    page_title = f"{title} | Urban Art Music | Urban Arts News"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "VideoObject",
                "@id": canonical + "#video",
                "name": title,
                "description": meta_description,
                "thumbnailUrl": [f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"],
                "embedUrl": f"https://www.youtube-nocookie.com/embed/{video_id}",
                "contentUrl": f"https://www.youtube.com/watch?v={video_id}",
                "url": canonical,
                "inLanguage": language,
                "isPartOf": {"@type": "CollectionPage", "name": "Urban Art Music", "url": BASE + "/urban-art-music/"},
                "publisher": {"@type": "Organization", "name": "Urban Arts News", "url": BASE + "/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Urban Arts News", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Urban Art Music", "item": BASE + "/urban-art-music/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
        ],
    }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    markup = f'''<!DOCTYPE html>
<html lang="{language}" dir="{config['dir']}"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#090909">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(meta_description)}"><meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<link rel="canonical" href="{esc(canonical)}">{hreflang_links(video)}
<meta property="og:type" content="video.other"><meta property="og:title" content="{esc(page_title)}"><meta property="og:description" content="{esc(meta_description)}"><meta property="og:url" content="{esc(canonical)}"><meta property="og:site_name" content="Urban Arts News"><meta property="og:image" content="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"><meta property="og:video" content="https://www.youtube-nocookie.com/embed/{video_id}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(page_title)}"><meta name="twitter:description" content="{esc(meta_description)}"><meta name="twitter:image" content="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg">
<script type="application/ld+json">{schema_json}</script>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f3f3f3;color:#171717;font-family:Arial,Helvetica,sans-serif;line-height:1.65}}a{{color:inherit;text-decoration:none}}header{{background:#090909;color:#fff;padding:18px 5%;display:flex;justify-content:space-between;align-items:center}}.logo{{font-size:28px;font-weight:900;letter-spacing:-1px}}.logo span,.accent{{color:#ff5b21}}nav{{display:flex;gap:18px;align-items:center}}nav a{{font-size:13px;font-weight:800;text-transform:uppercase}}.hero{{background:#111;color:#fff;padding:64px 6% 52px}}.eyebrow{{color:#ff5b21;font-size:13px;font-weight:900;letter-spacing:1.4px;text-transform:uppercase}}h1{{max-width:1050px;font-size:clamp(36px,6vw,72px);line-height:1;letter-spacing:-2px;margin:12px 0 16px}}.hero p{{color:#bbb;font-size:17px}}main{{width:min(1050px,92%);margin:48px auto}}.video-panel,.copy-panel,.language-panel{{background:#fff;box-shadow:0 7px 22px rgba(0,0,0,.08);margin-bottom:28px}}.player{{position:relative;aspect-ratio:16/9;background:#000}}.player iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}.video-meta{{padding:20px 24px;display:flex;gap:10px;flex-wrap:wrap}}.video-meta a{{display:inline-block;background:#111;color:#fff;padding:11px 15px;font-weight:900;text-transform:uppercase;font-size:13px}}.video-meta .subscribe-button{{background:#ff5b21}}.back{{color:#ff5b21;font-weight:900}}.copy-panel,.language-panel{{padding:30px}}.copy-panel h2,.language-panel h2{{margin-top:0}}.copy-panel p{{font-size:18px;color:#555}}.language-buttons{{display:flex;flex-wrap:wrap;gap:9px}}.language-button{{background:#111;color:#fff;padding:10px 13px;font-weight:800}}.language-button[aria-current="page"]{{background:#ff5b21}}.back{{display:inline-block;margin-top:10px}}footer{{background:#090909;color:#888;text-align:center;padding:35px;margin-top:60px}}@media(max-width:760px){{header{{display:block}}nav{{margin-top:12px;flex-wrap:wrap}}}}
</style></head><body>
<header><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a><nav><a href="/">Home</a><a href="/artists/">Artists</a><a href="/urban-art-cities/">Cities</a><a href="/urban-art-music/">Urban Art Music</a><a href="/subscribe/">Subscribe</a></nav></header>
<section class="hero"><div class="eyebrow">{esc(config['label'])} {position:02d}</div><h1>{esc(title)}</h1><p>{esc(author)} · YouTube · Urban Arts News</p></section>
<main>
<article class="video-panel"><div class="player"><iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{esc(title)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><div class="video-meta"><a href="https://www.youtube.com/watch?v={video_id}" rel="nofollow noopener" target="_blank">{esc(config['watch'])} →</a><a class="subscribe-button" href="/subscribe/">{esc(SUBSCRIBE_LABELS[language])} →</a></div></article>
<section class="copy-panel"><h2>{esc(config['about'])}</h2><p>{esc(paragraph)}</p><p><a href="{BASE}/"><strong>Urban Arts News</strong></a> connects music, graffiti, street art and independent urban creativity from Barcelona, Badalona and Buenos Aires to cities worldwide.</p></section>
<section class="language-panel"><h2>{esc(config['languages'])}</h2><div class="language-buttons">{language_buttons(video, language)}</div></section>
<a class="back" href="/urban-art-music/">← {esc(config['back'])}</a>
</main><footer>© 2026 Urban Arts News · Urban Art Music · {esc(title)}</footer></body></html>'''
    target = OUT / video_slug(video) if language == "en" else Path(language) / OUT / video_slug(video)
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(markup, encoding="utf-8")


def update_sitemap():
    sitemap = Path("sitemap.xml")
    text = sitemap.read_text(encoding="utf-8")
    for page_number in range(1, 4):
        url = url_for(page_number)
        if f"<loc>{url}</loc>" not in text:
            text = text.replace("</urlset>", f"  <url>\n    <loc>{url}</loc>\n  </url>\n</urlset>")
    for video in VIDEOS:
        for language in LANGUAGES:
            url = detail_url(language, video)
            if f"<loc>{url}</loc>" not in text:
                text = text.replace("</urlset>", f"  <url>\n    <loc>{url}</loc>\n  </url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def main():
    for page_number, videos in enumerate(PAGES, start=1):
        generate_page(page_number, videos)
    for position, video in enumerate(VIDEOS, start=1):
        for language in LANGUAGES:
            generate_video_page(video, position, language)
    update_sitemap()
    print(f"Generated 3 Urban Art Music pages and {len(VIDEOS) * len(LANGUAGES)} localized video pages for {len(VIDEOS)} videos")


if __name__ == "__main__":
    main()
