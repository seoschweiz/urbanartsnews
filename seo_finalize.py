"""Apply a consistent technical SEO baseline to every generated HTML page."""

import json
import re
import subprocess
from datetime import date
from html import escape, unescape
from pathlib import Path
from urllib.parse import quote, urljoin


BASE_URL = "https://urbanartsnews.com"
DEFAULT_IMAGE = f"{BASE_URL}/assets/images/urban-art-gallery-news/group-exhibition-gallery-wall.jpg"
SITE_NAME = "Urban Arts News"
CONTRIBUTOR_NAME = "Rodriquez Ventura"
CONTRIBUTOR_URL = "https://www.facebook.com/street.art.galleries.barcelona/"
LANGUAGE_MENU = '''<details class="language-menu"><summary>Languages</summary><div class="language-menu-list"><a href="/sq/urban-art-news/" hreflang="sq">Shqip</a><a href="/de/urban-art-news/" hreflang="de">Deutsch</a><a href="/es/urban-art-news/" hreflang="es">Español</a><a href="/ca/urban-art-news/" hreflang="ca">Català</a><a href="/pt/urban-art-news/" hreflang="pt">Português</a><a href="/it/urban-art-news/" hreflang="it">Italiano</a><a href="/fr/urban-art-news/" hreflang="fr">Français</a><a href="/ja/urban-art-news/" hreflang="ja">日本語</a><a href="/ar/urban-art-news/" hreflang="ar">العربية</a><a href="/ru/urban-art-news/" hreflang="ru">Русский</a><a href="/sv/urban-art-news/" hreflang="sv">Svenska</a><a href="/ko/urban-art-news/" hreflang="ko">한국어</a><a href="/hi/urban-art-news/" hreflang="hi">हिन्दी</a><a href="/languages/">All Languages</a></div></details>'''
LANGUAGE_CSS = '''<style>.language-menu{display:inline-block;position:relative;margin-left:18px}.language-menu summary{cursor:pointer;font-size:14px;font-weight:800;text-transform:uppercase;list-style:none}.language-menu summary::-webkit-details-marker{display:none}.language-menu summary:after{content:" ▾"}.language-menu-list{display:none;position:absolute;right:0;top:100%;min-width:190px;background:#111;padding:10px;box-shadow:0 12px 30px #0006;z-index:100}.language-menu[open] .language-menu-list,.language-menu:hover .language-menu-list{display:block}.language-menu-list a{display:block!important;color:#fff!important;padding:9px 12px!important;margin:0!important;text-align:left;text-transform:none!important}.language-menu-list a:hover,.language-menu-list a:focus{color:#ff5b21!important}@media(max-width:750px){.language-menu{margin:12px 0 0}.language-menu-list{position:static;margin-top:8px}}</style>'''

ARTIST_GALLERY_LOCATIONS = {
    "art-is-trash": {
        "@type": "Place",
        "name": "Artevistas Gallery Born",
        "sameAs": "https://www.google.com/maps/search/?api=1&query=41.38510%2C2.18058",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Carrer de la Barra de Ferro, 8",
            "postalCode": "08003",
            "addressLocality": "Barcelona",
            "addressRegion": "Catalonia",
            "addressCountry": "ES",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 41.38510,
            "longitude": 2.18058,
        },
    },
    "ashwan": {
        "@type": "Place",
        "name": "BienCuadrado Art Gallery",
        "sameAs": "https://www.google.com/maps/search/?api=1&query=41.3809952%2C2.1790367",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Carrer d'Ataülf, 14",
            "postalCode": "08002",
            "addressLocality": "Barcelona",
            "addressRegion": "Catalonia",
            "addressCountry": "ES",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 41.3809952,
            "longitude": 2.1790367,
        },
    },
}


def artist_gallery_location(*values):
    haystack = " ".join(str(value or "").lower() for value in values)
    if "art-is-trash" in haystack or "francisco-de-pajaro" in haystack:
        return json.loads(json.dumps(ARTIST_GALLERY_LOCATIONS["art-is-trash"]))
    if "ashwan" in haystack:
        return json.loads(json.dumps(ARTIST_GALLERY_LOCATIONS["ashwan"]))
    return None


def first_match(pattern, text, flags=re.I | re.S):
    match = re.search(pattern, text, flags)
    return unescape(match.group(1).strip()) if match else ""


def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def page_url(path):
    relative = path.parent.as_posix()
    if relative == ".":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{relative.strip('/')}/"


def add_before_head(html, markup):
    return html.replace("</head>", markup + "\n</head>", 1)


def normalize_json_ld(html, canonical="", title="", description="", page_language="en"):
    pattern = re.compile(
        r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)',
        re.I | re.S,
    )

    def clean(match):
        try:
            data = json.loads(match.group(2), strict=False)
        except (TypeError, ValueError):
            return match.group(0)

        def synchronize(item):
            if isinstance(item, list):
                for child in item:
                    synchronize(child)
            elif isinstance(item, dict):
                item_type = item.get("@type")
                item_id = str(item.get("@id", ""))
                item_url = str(item.get("url", ""))
                if item_type == "ImageObject":
                    location = artist_gallery_location(
                        item.get("contentUrl"), item_url, item_id, canonical
                    )
                    if location:
                        item["contentLocation"] = location
                    item["contributor"] = {
                        "@type": "Person",
                        "name": CONTRIBUTOR_NAME,
                        "url": CONTRIBUTOR_URL,
                        "sameAs": [CONTRIBUTOR_URL],
                    }
                if canonical and isinstance(item_type, str) and item_type in {"WebPage", "CollectionPage", "ProfilePage"} and (
                    item_url == canonical or item_id.startswith(canonical + "#")
                ):
                    item["name"] = title
                    item["description"] = description
                    item["inLanguage"] = page_language
                for child in item.values():
                    synchronize(child)

        synchronize(data)
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return match.group(1) + payload + match.group(3)

    return pattern.sub(clean, html)


def uniquify_image_titles(pages):
    groups = {}
    for path in pages:
        if len(path.parts) != 3 or path.parts[0] != "images" or path.parts[-1] != "index.html":
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        title = plain_text(first_match(r"<title>(.*?)</title>", html))
        groups.setdefault(title, []).append(path)

    for title, paths in groups.items():
        if not title or len(paths) < 2:
            continue
        subject = title.split("|")[0].strip()
        for number, path in enumerate(sorted(paths), start=1):
            html = path.read_text(encoding="utf-8", errors="ignore")
            unique_title = f"{subject} – Selected Work {number} | Urban Arts News"
            html = re.sub(
                r"<title>.*?</title>",
                f"<title>{escape(unique_title)}</title>",
                html,
                count=1,
                flags=re.I | re.S,
            )
            description = first_match(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', html)
            if description and f"Selected work {number}" not in description:
                unique_description = f"Selected work {number}: {description[0].lower() + description[1:]}"
                html = replace_or_add_meta(html, "name", "description", unique_description)
            path.write_text(html, encoding="utf-8")


def absolute_image(html):
    image = first_match(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)', html)
    if not image:
        image = first_match(r'<img\b[^>]*\bsrc=["\']([^"\']+)', html)
    if not image or image.startswith("data:"):
        return DEFAULT_IMAGE
    return urljoin(f"{BASE_URL}/", image)


def replace_or_add_meta(html, attribute, key, content):
    pattern = rf'<meta\s+{attribute}=["\']{re.escape(key)}["\'][^>]*>'
    replacement = f'<meta {attribute}="{key}" content="{escape(content, quote=True)}">'
    if re.search(pattern, html, re.I):
        return re.sub(pattern, replacement, html, count=1, flags=re.I)
    return add_before_head(html, replacement)



def add_whatsapp_share(html, canonical, title):
    """Add one accessible WhatsApp share button using the current canonical URL."""
    html = re.sub(
        r'<!-- WhatsApp Share -->.*?<!-- /WhatsApp Share -->',
        '',
        html,
        flags=re.I | re.S,
    )
    share_url = "https://wa.me/?text=" + quote(f"{title} {canonical}")
    markup = f'''<!-- WhatsApp Share -->
<style id="whatsapp-share-style">
.whatsapp-share-button{{position:fixed;right:18px;bottom:18px;z-index:9999;display:inline-flex;align-items:center;gap:9px;padding:12px 17px;border-radius:999px;background:#25D366;color:#fff!important;font:700 15px/1 Arial,Helvetica,sans-serif;text-decoration:none!important;box-shadow:0 6px 22px rgba(0,0,0,.28);transition:transform .2s ease,box-shadow .2s ease}}
.whatsapp-share-button:hover,.whatsapp-share-button:focus{{transform:translateY(-2px);box-shadow:0 8px 26px rgba(0,0,0,.34)}}
.whatsapp-share-button svg{{width:22px;height:22px;fill:currentColor;flex:none}}
@media(max-width:600px){{.whatsapp-share-button{{right:12px;bottom:12px;padding:12px 15px;font-size:14px}}}}
</style>
<a class="whatsapp-share-button" href="{escape(share_url, quote=True)}" target="_blank" rel="nofollow noopener noreferrer" aria-label="Share this page on WhatsApp" title="Share on WhatsApp">
<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M19.11 17.21c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.15-.42-2.19-1.35-.81-.72-1.36-1.62-1.52-1.89-.16-.27-.02-.42.12-.55.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.01-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.72.34-.25.27-.95.93-.95 2.26s.97 2.62 1.11 2.8c.14.18 1.91 2.91 4.62 4.08.65.28 1.15.45 1.54.57.65.21 1.24.18 1.71.11.52-.08 1.6-.66 1.83-1.29.23-.63.23-1.18.16-1.29-.07-.11-.25-.18-.52-.32M16.03 27.06h-.01a11 11 0 0 1-5.61-1.54l-.4-.24-4.17 1.09 1.11-4.06-.26-.42a11.02 11.02 0 1 1 9.34 5.17m9.38-20.36A13.17 13.17 0 0 0 4.68 22.58L2.81 29.4l6.98-1.83a13.14 13.14 0 0 0 6.23 1.59h.01A13.17 13.17 0 0 0 25.41 6.7"/></svg>
<span>Share</span>
</a>
<!-- /WhatsApp Share -->'''
    if re.search(r"</body>", html, re.I):
        return re.sub(r"</body>", lambda match: markup + "\n" + match.group(0), html, count=1, flags=re.I)
    return html + "\n" + markup + "\n"

def enrich_artist_schema(path, html, canonical, title, description, page_language, image):
    is_english_profile = len(path.parts) == 3 and path.parts[0] == "artists" and path.parts[-1] == "index.html"
    is_localized_profile = len(path.parts) == 4 and path.parts[1] == "artists" and path.parts[-1] == "index.html"
    if not (is_english_profile or is_localized_profile) or '"ProfilePage"' in html:
        return html
    slug = path.parts[-2]
    heading = plain_text(first_match(r"<h1[^>]*>(.*?)</h1>", html)) or slug.replace("-", " ").title()
    instagram = first_match(r'<a[^>]+href=["\'](https://www\.instagram\.com/[^"\']+)', html)
    artist_id = f"{BASE_URL}/artists/{slug}/#artist"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{BASE_URL}/#organization", "name": SITE_NAME, "url": f"{BASE_URL}/"},
            {"@type": "WebSite", "@id": f"{BASE_URL}/#website", "name": SITE_NAME, "url": f"{BASE_URL}/", "publisher": {"@id": f"{BASE_URL}/#organization"}},
            {"@type": "ImageObject", "@id": f"{canonical}#primaryimage", "url": image, "contentUrl": image, "caption": heading},
            {"@type": "Person", "@id": artist_id, "name": heading, "url": f"{BASE_URL}/artists/{slug}/", **({"sameAs": [instagram]} if instagram else {})},
            {"@type": "ProfilePage", "@id": f"{canonical}#webpage", "url": canonical, "name": title, "description": description, "inLanguage": page_language, "isPartOf": {"@id": f"{BASE_URL}/#website"}, "mainEntity": {"@id": artist_id}, "primaryImageOfPage": {"@id": f"{canonical}#primaryimage"}},
            {"@type": "Article", "@id": f"{canonical}#article", "headline": title, "description": description, "url": canonical, "inLanguage": page_language, "author": {"@id": artist_id}, "publisher": {"@id": f"{BASE_URL}/#organization"}, "image": {"@id": f"{canonical}#primaryimage"}, "mainEntityOfPage": {"@id": f"{canonical}#webpage"}},
            {"@type": "BreadcrumbList", "@id": f"{canonical}#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": f"{BASE_URL}/"}, {"@type": "ListItem", "position": 2, "name": "Urban Artists", "item": f"{BASE_URL}/artists/"}, {"@type": "ListItem", "position": 3, "name": heading, "item": canonical}]},
        ],
    }
    markup = f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>'
    pattern = r'<script\s+type=["\']application/ld\+json["\']>.*?</script>'
    if re.search(pattern, html, re.I | re.S):
        return re.sub(pattern, lambda _: markup, html, count=1, flags=re.I | re.S)
    return add_before_head(html, markup)


def activate_known_tag_links(html):
    pattern = re.compile(r'<span\s+class=["\']tag["\']>(#[^<]+)</span>', re.I)

    def activate(match):
        label = match.group(1)
        normalized = re.sub(r"[^a-z0-9]+", "", label.lower())
        if "barcelona" in normalized and "streetart" in normalized:
            url = "/tags/barcelona-street-art/"
        elif "streetart" in normalized or "graffiti" in normalized or "mural" in normalized:
            url = "/tags/street-art/"
        elif "urbanart" in normalized:
            url = "/tags/urban-art/"
        else:
            return match.group(0)
        return f'<a class="tag" href="{url}">{label}</a>'

    return pattern.sub(activate, html)


def activate_artist_tag_labels(path, html):
    if len(path.parts) != 3 or path.parts[0] != "artists" or path.parts[-1] != "index.html":
        return html
    data_path = Path("data/artists.json")
    if not data_path.exists():
        return html
    try:
        artists = json.loads(data_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return html
    slug = path.parts[1]
    instagram = next((item.get("instagram", "") for item in artists if item.get("slug") == slug), "")
    if not instagram:
        return html
    return re.sub(
        r'<span\s+class=["\']tag["\']>(#[^<]+)</span>',
        lambda match: f'<a class="tag" href="{escape(instagram, quote=True)}" target="_blank" rel="nofollow noopener">{match.group(1)}</a>',
        html,
        flags=re.I,
    )


def finalize_page(path):
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = normalize_json_ld(html)
    html = activate_known_tag_links(html)
    html = activate_artist_tag_labels(path, html)
    html = html.replace(".tag:hover", ".tag[href]:hover")
    page_language = first_match(r'<html\s+[^>]*lang=["\']([^"\']+)', html) or "en"
    html = re.sub(
        r'<link\s+rel=["\']icon["\'][^>]*>',
        '<link rel="icon" href="/favicon.png" type="image/png" sizes="96x96">',
        html,
        count=1,
        flags=re.I,
    )
    if not re.search(r'<link\s+rel=["\']icon["\']', html, re.I):
        html = add_before_head(html, '<link rel="icon" href="/favicon.png" type="image/png" sizes="96x96">')
    if not re.search(r'<link\s+rel=["\']apple-touch-icon["\']', html, re.I):
        html = add_before_head(html, '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">')
    canonical = first_match(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', html)
    if not canonical:
        canonical = page_url(path)
        html = add_before_head(html, f'<link rel="canonical" href="{canonical}">')

    title = plain_text(first_match(r"<title>(.*?)</title>", html))
    if not title:
        h1 = plain_text(first_match(r"<h1[^>]*>(.*?)</h1>", html)) or SITE_NAME
        title = f"{h1} | {SITE_NAME}" if h1 != SITE_NAME else SITE_NAME
        html = add_before_head(html, f"<title>{escape(title)}</title>")

    description = first_match(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', html)
    if path == Path("images/index.html") or (
        len(path.parts) == 4 and path.parts[0] == "images" and path.parts[1] == "page"
    ):
        page_number = 1 if path == Path("images/index.html") else int(path.parts[2])
        description = (
            f"Explore page {page_number} of our mixed visual gallery featuring street art and "
            "urban artists from Barcelona, Badalona, Venice and cities around the world."
        )
        html = replace_or_add_meta(html, "name", "description", description)
    if not description:
        description = plain_text(first_match(r"<p[^>]*>(.*?)</p>", html))
        description = (description[:157].rstrip(" ,.;:") + "…") if len(description) > 160 else description
        description = description or "Explore street art, urban artists, galleries, murals and visual culture with Urban Arts News."
        html = add_before_head(html, f'<meta name="description" content="{escape(description, quote=True)}">')

    html = normalize_json_ld(html, canonical, title, description, page_language)

    robots = first_match(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)', html)
    if "noindex" not in robots.lower():
        html = replace_or_add_meta(
            html,
            "name",
            "robots",
            "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1",
        )

    image = absolute_image(html)
    if len(path.parts) == 3 and path.parts[0] == "artists" and path.parts[-1] == "index.html":
        artist_share_card = Path("assets/images/social/artists") / f"{path.parts[1]}.jpg"
        if artist_share_card.exists():
            image = f"{SITE_URL}/{artist_share_card.as_posix()}"
    social = (
        ("property", "og:title", title),
        ("property", "og:description", description),
        ("property", "og:type", "website"),
        ("property", "og:url", canonical),
        ("property", "og:site_name", SITE_NAME),
        ("property", "article:author", CONTRIBUTOR_URL),
        ("property", "og:see_also", CONTRIBUTOR_URL),
        ("name", "author", CONTRIBUTOR_NAME),
        ("property", "og:locale", {"ca": "ca_ES", "de": "de_DE", "es": "es_ES", "pt": "pt_PT", "it": "it_IT", "fr": "fr_FR", "sq": "sq_AL", "ja": "ja_JP", "ar": "ar_AR", "ru": "ru_RU", "sv": "sv_SE", "ko": "ko_KR", "hi": "hi_IN"}.get(page_language, "en_US")),
        ("property", "og:image", image),
        ("property", "og:image:secure_url", image),
        ("property", "og:image:type", "image/jpeg"),
        ("property", "og:image:width", "1200"),
        ("property", "og:image:height", "630"),
        ("property", "og:image:alt", f"{title} — artist profile preview"),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:title", title),
        ("name", "twitter:description", description),
        ("name", "twitter:image", image),
        ("name", "twitter:image:alt", f"{title} — artist profile preview"),
    )
    for attribute, key, value in social:
        html = replace_or_add_meta(html, attribute, key, value)

    html = enrich_artist_schema(path, html, canonical, title, description, page_language, image)

    if not re.search(r'<meta\s+name=["\']referrer["\']', html, re.I):
        html = add_before_head(html, '<meta name="referrer" content="strict-origin-when-cross-origin">')
    if path.parts and path.parts[0] == "urban-art-gallery-news":
        rss_url, rss_title = "/urban-art-gallery-news/feed.xml", "Urban Art Gallery News"
    elif len(path.parts) >= 4 and path.parts[1] == "artists":
        rss_url, rss_title = f"/{path.parts[0]}/feed.xml", f"Urban Artist Articles ({page_language})"
    elif len(path.parts) >= 3 and path.parts[0] == "artists":
        rss_url, rss_title = "/artists/feed.xml", "Urban Artist Articles"
    else:
        rss_url, rss_title = "/feed.xml", "Urban Arts News"
    rss_markup = f'<link rel="alternate" type="application/rss+xml" title="{rss_title}" href="{rss_url}">'
    rss_pattern = r'<link\s+rel=["\']alternate["\'][^>]*type=["\']application/rss\+xml["\'][^>]*>'
    if re.search(rss_pattern, html, re.I):
        html = re.sub(rss_pattern, rss_markup, html, count=1, flags=re.I)
    else:
        html = add_before_head(html, rss_markup)
    if path != Path("cities/barcelona/index.html") and re.search(r"<header\b", html, re.I):
        if "language-menu" in html:
            html = re.sub(r'<details\s+class=["\']language-menu["\']>.*?</details>', LANGUAGE_MENU, html, count=1, flags=re.I | re.S)
        else:
            if re.search(r"</nav>", html, re.I):
                html = re.sub(r"</nav>", LANGUAGE_MENU + "</nav>", html, count=1, flags=re.I)
            else:
                html = re.sub(r"</header>", LANGUAGE_MENU + "</header>", html, count=1, flags=re.I)
            html = add_before_head(html, LANGUAGE_CSS)
    if not re.search(r'<script\s+type=["\']application/ld\+json["\']', html, re.I):
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": canonical,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": f"{BASE_URL}/"},
            "inLanguage": page_language,
        }
        html = add_before_head(
            html,
            f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>',
        )

    html = add_whatsapp_share(html, canonical, title)
    path.write_text(html, encoding="utf-8")
    return canonical, "noindex" in robots.lower()


def enforce_url_migrations(pages):
    old_path = Path("cities/barcelona/index.html")
    new_url = f"{BASE_URL}/urban-art-city/barcelona/spain/"
    if old_path.exists():
        old_path.write_text(
            '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<meta name="robots" content="noindex,follow">\n'
            f'<link rel="canonical" href="{new_url}">\n'
            '<meta http-equiv="refresh" content="0; url=/urban-art-city/barcelona/spain/">\n'
            '<title>Barcelona Urban Art | Urban Arts News</title>\n'
            '<script>window.location.replace("/urban-art-city/barcelona/spain/");</script>\n'
            '</head><body><p>This page has moved to '
            '<a href="/urban-art-city/barcelona/spain/">Barcelona Urban Art</a>.</p></body></html>\n',
            encoding="utf-8",
        )
    for path in pages:
        if path == old_path:
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        updated = re.sub(
            r'href=(["\'])/cities/barcelona/\1',
            r'href=\1/urban-art-city/barcelona/spain/\1',
            html,
        )
        if updated != html:
            path.write_text(updated, encoding="utf-8")


def last_modified(path):
    try:
        dirty = subprocess.run(
            ["git", "diff", "--quiet", "--", str(path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode != 0
        untracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(path)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode != 0
        if dirty or untracked:
            return date.today().isoformat()
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
        value = result.stdout.strip()
        return value if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) else date.today().isoformat()
    except OSError:
        return date.today().isoformat()


def rebuild_sitemap(indexed_pages):
    rows = "\n".join(
        f"  <url>\n    <loc>{escape(url)}</loc>\n    <lastmod>{last_modified(path)}</lastmod>\n  </url>"
        for url, path in sorted(indexed_pages.items())
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{rows}\n"
        "</urlset>\n"
    )
    Path("sitemap.xml").write_text(xml, encoding="utf-8")


def ensure_ashwan_urban_art_gallery_link():
    """Keep the requested external gallery link after every site regeneration."""
    path = Path("artists/ashwan/index.html")
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8", errors="ignore")
    url = "https://share.google/xT8q0dObkLHEcJ0j3"
    if url in html:
        return
    link = f'<a class="profile-link" href="{url}" target="_blank" rel="noopener">Urban Art Gallery</a>'
    marker = '<nav class="profile-links" aria-label="Ashwan official links and art profiles">'
    start = html.find(marker)
    if start >= 0:
        end = html.find("</nav>", start)
        if end >= 0:
            html = html[:end] + "        " + link + "\n      " + html[end:]
    else:
        html = html.replace("</main>", f'<p>{link}</p></main>', 1)
    path.write_text(html, encoding="utf-8")


def ensure_artevistas_map_labels():
    """Keep the full Urban Art Gallery keyword in both Artevistas map buttons."""
    path = Path("street-art-galleries-barcelona/index.html")
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8", errors="ignore")
    html = html.replace("Artevistas Gallery Map I →", "Artevistas Urban Art Gallery Map I →")
    html = html.replace("Artevistas Gallery Map II →", "Artevistas Urban Art Gallery Map II →")
    path.write_text(html, encoding="utf-8")


def main():
    ensure_ashwan_urban_art_gallery_link()
    ensure_artevistas_map_labels()
    pages = sorted(path for path in Path(".").rglob("index.html") if ".git" not in path.parts)
    enforce_url_migrations(pages)
    uniquify_image_titles(pages)
    indexed_pages = {}
    for path in pages:
        canonical, noindex = finalize_page(path)
        if not noindex and canonical.startswith(f"{BASE_URL}/"):
            indexed_pages[canonical] = path
    rebuild_sitemap(indexed_pages)
    print(f"SEO finalized: {len(pages)} pages checked; {len(indexed_pages)} canonical URLs in sitemap")


if __name__ == "__main__":
    main()
