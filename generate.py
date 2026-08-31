# Generates artists, cities, mixed galleries, RSS news and sitemap.
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

BASE_URL = "https://urbanartsnews.com"
DATA_FILE = Path("data/artists.json")
POST_STATUS_FILE = Path("data/post_status.json")
POST_STATUS = {}

ARTISTS_DIR = Path("artists")
CITIES_DIR = Path("cities")
IMAGES_DIR = Path("images")

MANUAL_ARTIST_PAGES = {
    "art-is-trash",
    "ashwan",
    "si-beriana",
}


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def instagram_embed_url(url):
    clean = url.split("?")[0].rstrip("/")
    return clean + "/embed/"


def ensure_directory(path):
    path.mkdir(parents=True, exist_ok=True)


def load_artists():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)



def normalize_instagram_post(url):
    return url.split("?")[0].rstrip("/") + "/"


def check_instagram_post(url):
    """Return True for reachable, False only for definite removal, None for temporary uncertainty."""
    embed_url = instagram_embed_url(url)
    request = urllib.request.Request(
        embed_url,
        headers={
            "User-Agent": "Mozilla/5.0 UrbanArtsNews-LinkChecker/1.0",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            content = response.read(600000).decode("utf-8", errors="ignore").lower()
            if response.status in (404, 410):
                return False
            if response.status != 200:
                return None
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 410):
            return False
        return None
    except Exception:
        return None

    definite_missing = (
        "post isn't available",
        "post is not available",
        "page isn't available",
        "page is not available",
        "sorry, this page isn't available",
        "the link you followed may be broken",
        "content unavailable",
    )
    if any(marker in content for marker in definite_missing):
        return False
    return True


def refresh_post_status(artists):
    global POST_STATUS
    if POST_STATUS_FILE.exists():
        try:
            loaded = json.loads(POST_STATUS_FILE.read_text(encoding="utf-8"))
            POST_STATUS = loaded if isinstance(loaded, dict) else {}
        except Exception:
            POST_STATUS = {}
    else:
        POST_STATUS = {}

    urls = []
    seen = set()
    for artist in artists:
        for post in artist.get("posts", []):
            url = normalize_instagram_post(post)
            if url not in seen:
                seen.add(url)
                urls.append(url)

    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(check_instagram_post, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                results[url] = future.result()
            except Exception:
                results[url] = None

    for url in urls:
        previous = POST_STATUS.get(url, {})
        failures = int(previous.get("consecutive_failures", 0))
        result = results.get(url)
        if result is True:
            failures = 0
            state = "available"
        elif result is False:
            failures = min(2, failures + 1)
            state = "hidden" if failures >= 2 else "warning"
        else:
            state = previous.get("state", "unknown")
        POST_STATUS[url] = {
            "consecutive_failures": failures,
            "state": state,
        }

    # Remove status records for links no longer present in artists.json.
    POST_STATUS = {url: POST_STATUS[url] for url in urls}
    POST_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    POST_STATUS_FILE.write_text(
        json.dumps(POST_STATUS, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    hidden = sum(1 for value in POST_STATUS.values() if value.get("consecutive_failures", 0) >= 2)
    warnings = sum(1 for value in POST_STATUS.values() if value.get("consecutive_failures", 0) == 1)
    print(f"Instagram link check: {len(urls)} checked, {warnings} warning, {hidden} hidden")


def get_active_posts(artist):
    active = []
    for post in artist.get("posts", []):
        url = normalize_instagram_post(post)
        status = POST_STATUS.get(url, {})
        if int(status.get("consecutive_failures", 0)) < 2:
            active.append(url)
    return active

def page_head(title, description, canonical):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">

<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">

<style>
* {{
  box-sizing:border-box;
  margin:0;
  padding:0;
}}

body {{
  font-family:Arial,Helvetica,sans-serif;
  background:#f5f5f5;
  color:#161616;
  line-height:1.6;
}}

a {{
  color:inherit;
  text-decoration:none;
}}

header {{
  background:#090909;
  color:white;
  padding:18px 5%;
  display:flex;
  justify-content:space-between;
  align-items:center;
  position:sticky;
  top:0;
  z-index:20;
}}

.logo {{
  font-size:28px;
  font-weight:900;
  letter-spacing:-1px;
}}

.logo span {{
  color:#ff5b21;
}}

nav a {{
  margin-left:22px;
  font-size:14px;
  font-weight:700;
  text-transform:uppercase;
}}

nav a:hover {{
  color:#ff5b21;
}}

.hero {{
  background:#111;
  color:white;
  padding:95px 6%;
}}

.hero-label {{
  color:#ff5b21;
  font-size:13px;
  font-weight:800;
  text-transform:uppercase;
  margin-bottom:12px;
}}

.hero h1 {{
  font-size:clamp(48px,8vw,92px);
  line-height:.95;
  text-transform:uppercase;
  letter-spacing:-3px;
  margin-bottom:20px;
}}

.hero h1 span {{
  color:#ff5b21;
}}

.hero p {{
  max-width:850px;
  font-size:19px;
  color:#ccc;
}}

.container {{
  width:min(1400px,92%);
  margin:55px auto;
}}

.section-title {{
  font-size:32px;
  text-transform:uppercase;
  margin-bottom:30px;
}}

.section-title span {{
  color:#ff5b21;
}}

.grid {{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:25px;
}}

.card {{
  background:white;
  overflow:hidden;
  box-shadow:0 5px 18px rgba(0,0,0,.08);
  transition:.2s;
}}

.card:hover {{
  transform:translateY(-4px);
  box-shadow:0 12px 28px rgba(0,0,0,.13);
}}

.card-content {{
  padding:22px;
}}

.card h2,
.card h3 {{
  margin-bottom:10px;
}}

.card p {{
  color:#666;
  margin-bottom:16px;
}}

.instagram-frame {{
  width:100%;
  height:520px;
  border:0;
  display:block;
  background:white;
}}

.category {{
  color:#ff5b21;
  font-size:12px;
  font-weight:800;
  text-transform:uppercase;
  margin-bottom:7px;
}}

.tags {{
  display:flex;
  flex-wrap:wrap;
  gap:7px;
  margin-top:12px;
}}

.tag {{
  background:#eee;
  padding:6px 9px;
  font-size:11px;
  font-weight:700;
}}

.tag:hover {{
  background:#ff5b21;
  color:white;
}}

.button {{
  display:inline-block;
  background:#ff5b21;
  color:white;
  padding:13px 18px;
  font-size:13px;
  font-weight:800;
  text-transform:uppercase;
  margin-top:12px;
}}

.button:hover {{
  background:#111;
}}

.home-layout {{
  display:grid;
  grid-template-columns:minmax(0,3fr) minmax(260px,1fr);
  gap:38px;
}}

.sidebar-box {{
  background:white;
  padding:24px;
  margin-bottom:25px;
  box-shadow:0 5px 18px rgba(0,0,0,.06);
}}

.sidebar-box h3 {{
  text-transform:uppercase;
  font-size:18px;
  margin-bottom:15px;
  border-bottom:3px solid #ff5b21;
  padding-bottom:8px;
}}

.sidebar-box a {{
  display:block;
  padding:9px 0;
  border-bottom:1px solid #eee;
  font-weight:700;
}}

.sidebar-box a:hover {{
  color:#ff5b21;
}}

.profile-layout {{
  display:grid;
  grid-template-columns:minmax(0,2fr) minmax(260px,1fr);
  gap:40px;
  margin-bottom:60px;
}}

.profile-copy {{
  background:white;
  padding:38px;
  box-shadow:0 5px 18px rgba(0,0,0,.06);
}}

.profile-copy h2 {{
  font-size:33px;
  text-transform:uppercase;
  margin-bottom:20px;
}}

.profile-copy h2 span {{
  color:#ff5b21;
}}

.profile-copy p {{
  color:#505050;
  font-size:16px;
  margin-bottom:18px;
}}

.info-box {{
  background:#111;
  color:white;
  padding:30px;
  height:fit-content;
}}

.info-box h3 {{
  color:#ff5b21;
  text-transform:uppercase;
  margin-bottom:18px;
}}

.meta {{
  padding:11px 0;
  border-bottom:1px solid #333;
}}

.meta strong {{
  display:block;
  color:#999;
  font-size:11px;
  text-transform:uppercase;
  margin-bottom:2px;
}}

.artist-grid {{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:22px;
}}

.artist-tile {{
  background:#111;
  color:white;
  padding:28px;
}}

.artist-tile .category {{
  margin-bottom:8px;
}}

.artist-tile h2 {{
  font-size:28px;
  text-transform:uppercase;
  margin-bottom:10px;
}}

.artist-tile p {{
  color:#bbb;
  margin-bottom:16px;
}}

.related {{
  margin-top:50px;
  background:white;
  padding:30px;
  box-shadow:0 5px 18px rgba(0,0,0,.06);
}}

footer {{
  margin-top:70px;
  background:#090909;
  color:#888;
  text-align:center;
  padding:40px;
  font-size:13px;
}}

@media(max-width:1100px) {{
  .home-layout {{
    grid-template-columns:1fr;
  }}

  .grid {{
    grid-template-columns:repeat(2,1fr);
  }}

  .artist-grid {{
    grid-template-columns:repeat(2,1fr);
  }}
}}

@media(max-width:750px) {{
  header {{
    display:block;
  }}

  nav {{
    margin-top:12px;
  }}

  nav a {{
    margin-left:0;
    margin-right:12px;
  }}

  .grid,
  .artist-grid {{
    grid-template-columns:1fr;
  }}

  .profile-layout {{
    grid-template-columns:1fr;
  }}

  .instagram-frame {{
    height:620px;
  }}
}}
</style>
</head>

<body>

<header>
<a href="/" class="logo">URBAN <span>ARTS</span> NEWS</a>

<nav>
<a href="/">Home</a>
<a href="/tags/street-art/">Street Art</a>
<a href="/tags/urban-art/">Urban Art</a>
<a href="/cities/">Cities</a>
<a href="/artists/">Artists</a>
<a href="/images/">Images</a>
</nav>
</header>
"""


def page_footer():
    return """
<footer>
© 2026 Urban Arts News · Street Art · Urban Artists · Urban Culture
</footer>
</body>
</html>
"""


def make_tag_html(tags):
    html = ""
    for tag in tags:
        clean = re.sub(r"[^A-Za-z0-9]+", "", tag)
        if clean:
            html += f'<span class="tag">#{escape(clean)}</span>\n'
    return html


def generate_artist_page(artist):
    name = artist["name"]
    slug = artist["slug"]
    city = artist["city"]
    country = artist["country"]
    instagram = artist["instagram"]
    posts = get_active_posts(artist)
    headline = artist.get("headline", f"{name} – Urban Art from {city}")
    bio = artist.get("bio", f"{name} is an urban artist connected with {city}, {country}.")
    seo_text = artist.get("seo_text", "")
    tags = artist.get("tags", ["Urban Art", city])

    artist_dir = ARTISTS_DIR / slug
    ensure_directory(artist_dir)
    output_file = artist_dir / "index.html"

    if slug in MANUAL_ARTIST_PAGES and output_file.exists() and len(posts) == len(artist.get("posts", [])):
        print(f"KEEP manual artist page: {output_file}")
        return

    canonical = f"{BASE_URL}/artists/{slug}/"
    city_slug = slugify(city)

    title = f"{name} | {city} Urban Artist | Urban Arts News"
    description = f"Discover {name}, {headline}. Explore selected Instagram posts and urban art connected with {city}, {country}."

    post_html = ""

    for index, post in enumerate(posts, start=1):
        embed = instagram_embed_url(post)

        post_html += f"""
<article class="card">
<iframe class="instagram-frame" src="{embed}" loading="lazy"></iframe>

<div class="card-content">
<div class="category">{escape(name)} · {escape(city)}</div>

<h3>{escape(name)} · Selected Work {index}</h3>

<p>
Selected Instagram work by {escape(name)}, featured in the Urban Arts News
archive for {escape(city)}, {escape(country)}.
</p>

<div class="tags">
<a class="tag" href="/tags/street-art/">#StreetArt</a>
<a class="tag" href="/tags/urban-art/">#UrbanArt</a>
<a class="tag" href="/cities/{city_slug}/">#{escape(city.replace(" ", ""))}</a>
</div>
</div>
</article>
"""

    html = page_head(title, description, canonical)

    html += f"""
<section class="hero">
<div class="hero-label">Urban Arts News · {escape(city)} Featured Artist</div>
<h1><span>{escape(name)}</span></h1>
<p>{escape(headline)}</p>
</section>

<main class="container">

<section class="profile-layout">

<div class="profile-copy">
<h2>About <span>{escape(name)}</span></h2>

<p>{escape(bio)}</p>

<p>
Urban Arts News presents {escape(name)} as a featured artist connected
with {escape(city)}, combining selected Instagram works with an
independent editorial profile and city-based discovery.
</p>

<h3>Artist Tags</h3>
<div class="tags">
{make_tag_html(tags)}
</div>
</div>

<aside class="info-box">
<h3>Artist Information</h3>

<div class="meta">
<strong>Artist</strong>
{escape(name)}
</div>

<div class="meta">
<strong>City</strong>
<a href="/cities/{city_slug}/">{escape(city)}</a>
</div>

<div class="meta">
<strong>Country</strong>
{escape(country)}
</div>

<a class="button"
href="{escape(instagram)}"
target="_blank"
rel="noopener">
View Instagram
</a>
</aside>

</section>

<h2 class="section-title">Selected <span>{escape(name)} Posts</span></h2>

<div class="grid">
{post_html}
</div>

<section class="related">
<h2>About {escape(name)} and Urban Art in {escape(city)}</h2>
<p>{escape(seo_text)}</p>
</section>

<section class="related">
<h2>Explore {escape(city)}</h2>

<p>
Discover more urban artists and street-art culture connected with
{escape(city)} on Urban Arts News.
</p>

<a class="button" href="/cities/{city_slug}/">
Explore {escape(city)} →
</a>

<a class="button" href="/artists/">
All Artists →
</a>
</section>

</main>
"""

    html += page_footer()
    output_file.write_text(html, encoding="utf-8")
    print(f"UPDATE artist page: {output_file}")


def generate_artist_directory(artists):
    ensure_directory(ARTISTS_DIR)

    cards = ""

    for number, artist in enumerate(artists, start=1):
        name = artist["name"]
        slug = artist["slug"]
        city = artist["city"]
        country = artist["country"]
        headline = artist.get("headline", f"{name} – Urban Art")

        cards += f"""
<article class="card">
<div class="card-content">

<div class="category">Artist {number:02d} · {escape(city)}</div>
<h2>{escape(name)}</h2>
<p>{escape(headline)}</p>

<div class="tags">
<a class="tag" href="/cities/{slugify(city)}/">#{escape(city.replace(" ", ""))}</a>
<span class="tag">#{escape(country.replace(" ", ""))}</span>
<span class="tag">#UrbanArt</span>
</div>

<a class="button" href="/artists/{slug}/">
Explore {escape(name)} →
</a>

</div>
</article>
"""

    html = page_head(
        "Urban Artists | Urban Arts News",
        "Discover featured street artists and contemporary urban artists by city on Urban Arts News.",
        f"{BASE_URL}/artists/"
    )

    html += """
<section class="hero">
<div class="hero-label">Urban Arts News · Artist Directory</div>
<h1>Urban <span>Artists</span></h1>
<p>
Discover curated artists city by city, from Barcelona to Venice
and the world's most important urban-art scenes.
</p>
</section>

<main class="container">
<h2 class="section-title">Featured <span>Artists</span></h2>
<div class="grid">
"""
    html += cards
    html += """
</div>
</main>
"""
    html += page_footer()

    output_file = ARTISTS_DIR / "index.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"UPDATE artist directory: {output_file}")



def city_news_rss_url(city):
    query = urllib.parse.quote_plus(f"urban art {city}")
    return f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


def fetch_city_news(city, limit=6):
    rss_url = city_news_rss_url(city)
    request = urllib.request.Request(
        rss_url,
        headers={"User-Agent": "Mozilla/5.0 UrbanArtsNews/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            root = ET.fromstring(response.read())
        items = []
        for item in root.findall("./channel/item")[:limit]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            date = (item.findtext("pubDate") or "").strip()
            source_node = item.find("source")
            source = (source_node.text or "").strip() if source_node is not None else ""
            if title and link:
                items.append({"title": title, "link": link, "date": date, "source": source})
        return items
    except Exception as exc:
        print(f"WARNING city news unavailable for {city}: {exc}")
        return []


def render_city_news(city):
    items = fetch_city_news(city)
    rss_url = city_news_rss_url(city)
    cards = ""
    for item in items:
        source_line = item["source"] or "English news source"
        cards += f"""
<article class="card">
<div class="card-content">
<div class="category">{escape(city)} · Urban Art News</div>
<h3><a href="{escape(item['link'])}" target="_blank" rel="noopener noreferrer">{escape(item['title'])}</a></h3>
<p>{escape(source_line)}</p>
<a class="button" href="{escape(item['link'])}" target="_blank" rel="noopener noreferrer">Read News →</a>
</div>
</article>
"""
    if not cards:
        cards = f"""
<article class="card">
<div class="card-content">
<h3>Urban Art {escape(city)} News</h3>
<p>The live English news feed is temporarily unavailable. Open the RSS source directly for the latest results.</p>
</div>
</article>
"""
    return f"""
<section style="margin-top:70px;" aria-labelledby="city-news-title">
<h2 class="section-title" id="city-news-title">Urban Art <span>{escape(city)} News</span></h2>
<p style="margin-bottom:25px;">Latest English-language news results for urban art, street art, murals and visual culture connected with {escape(city)}.</p>
<div class="grid">
{cards}
</div>
<a class="button" href="{escape(rss_url)}" target="_blank" rel="noopener noreferrer" type="application/rss+xml">English RSS Feed →</a>
</section>
"""

def generate_city_pages(artists):
    ensure_directory(CITIES_DIR)

    cities = {}
    for artist in artists:
        cities.setdefault(artist["city"], []).append(artist)

    city_directory_cards = ""

    for city in sorted(cities):
        city_slug = slugify(city)
        city_artists = cities[city]
        plural = "s" if len(city_artists) != 1 else ""

        city_directory_cards += f"""
<article class="card">
<div class="card-content">

<div class="category">Urban Arts News · City</div>
<h2>{escape(city)}</h2>

<p>
Explore {len(city_artists)} featured urban artist{plural}
connected with {escape(city)}.
</p>

<a class="button" href="/cities/{city_slug}/">
Explore {escape(city)} →
</a>

</div>
</article>
"""

        artist_cards = ""

        for artist in city_artists:
            artist_name = artist["name"]
            artist_slug = artist["slug"]
            headline = artist.get("headline", f"{artist_name} – Urban Art")

            artist_cards += f"""
<article class="card">
<div class="card-content">

<div class="category">{escape(city)} Featured Artist</div>
<h2>{escape(artist_name)}</h2>
<p>{escape(headline)}</p>

<a class="button" href="/artists/{artist_slug}/">
Explore Artist →
</a>

</div>
</article>
"""

        city_dir = CITIES_DIR / city_slug
        ensure_directory(city_dir)

        city_html = page_head(
            f"{city} Urban Art & Street Artists | Urban Arts News",
            f"Discover featured urban artists, street art and contemporary urban culture from {city}.",
            f"{BASE_URL}/cities/{city_slug}/"
        )

        city_html += f"""
<section class="hero">
<div class="hero-label">Urban Arts News · City</div>
<h1><span>{escape(city)}</span></h1>

<p>
Discover selected street artists, urban creators and contemporary
visual culture connected with {escape(city)}.
</p>
</section>

<main class="container">

<h2 class="section-title">Artists in <span>{escape(city)}</span></h2>

<div class="grid">
{artist_cards}
</div>

{render_city_news(city)}

</main>
"""

        city_html += page_footer()

        city_output = city_dir / "index.html"
        city_output.write_text(city_html, encoding="utf-8")
        print(f"UPDATE city page: {city_output}")

    cities_html = page_head(
        "Urban Art Cities | Urban Arts News",
        "Explore featured street artists and contemporary urban art city by city.",
        f"{BASE_URL}/cities/"
    )

    cities_html += """
<section class="hero">
<div class="hero-label">Urban Arts News · City Directory</div>
<h1>Urban Art <span>Cities</span></h1>

<p>
Explore curated artists and contemporary urban culture city by city.
Barcelona is our deeper local focus, while international cities begin
with one selected featured artist.
</p>
</section>

<main class="container">

<h2 class="section-title">Explore <span>Cities</span></h2>

<div class="grid">
"""
    cities_html += city_directory_cards
    cities_html += """
</div>
</main>
"""
    cities_html += page_footer()

    cities_output = CITIES_DIR / "index.html"
    cities_output.write_text(cities_html, encoding="utf-8")
    print(f"UPDATE city directory: {cities_output}")


def generate_homepage(artists):
    cities = sorted({artist["city"] for artist in artists})

    # Build all Instagram posts from all artists.
    posts_html = ""

    for artist in artists:
        name = artist["name"]
        slug = artist["slug"]
        city = artist["city"]
        city_slug = slugify(city)
        posts = get_active_posts(artist)

        for index, post in enumerate(posts, start=1):
            embed = instagram_embed_url(post)

            posts_html += f"""
<article class="card">

<iframe
class="instagram-frame"
src="{embed}"
loading="lazy">
</iframe>

<div class="card-content">

<div class="category">
{escape(name)} · {escape(city)}
</div>

<h2>
<a href="/artists/{slug}/">
{escape(name)} · Urban Art
</a>
</h2>

<p>
Selected work by {escape(name)} from {escape(city)}.
</p>

<div class="tags">
<a class="tag" href="/artists/{slug}/">#{escape(name.replace(" ", ""))}</a>
<a class="tag" href="/cities/{city_slug}/">#{escape(city.replace(" ", ""))}</a>
<a class="tag" href="/tags/urban-art/">#UrbanArt</a>
</div>

</div>
</article>
"""

    artist_tiles = ""

    for artist in artists:
        name = artist["name"]
        slug = artist["slug"]
        city = artist["city"]
        headline = artist.get("headline", f"{name} – Urban Art")

        artist_tiles += f"""
<article class="artist-tile">

<div class="category">
{escape(city)} Featured Artist
</div>

<h2>
{escape(name)}
</h2>

<p>
{escape(headline)}
</p>

<a class="button"
href="/artists/{slug}/">
Explore Artist →
</a>

</article>
"""

    city_links = ""
    for city in cities:
        city_links += f'<a href="/cities/{slugify(city)}/">{escape(city)}</a>\n'

    artist_links = ""
    for artist in artists:
        artist_links += f'<a href="/artists/{artist["slug"]}/">{escape(artist["name"])}</a>\n'

    html = page_head(
        "Urban Arts News | Street Art, Graffiti & Urban Artists",
        "Discover street art, graffiti, murals and contemporary urban artists from Barcelona, Venice and cities around the world.",
        f"{BASE_URL}/"
    )

    html += """
<section class="hero">

<div class="hero-label">
Street Art · Graffiti · Murals · Urban Culture
</div>

<h1>
Urban <span>Arts</span> News
</h1>

<p>
A curated discovery platform for street art and contemporary urban artists.
Barcelona is our local focus, while selected international artists connect
Urban Arts News with cities around the world.
</p>

</section>


<main class="container">

<h2 class="section-title">
Latest <span>Instagram Posts</span>
</h2>

<div class="home-layout">

<div>

<div class="grid">
"""
    html += posts_html
    html += """
</div>

</div>

<aside>

<section class="sidebar-box">

<h3>
Cities
</h3>
"""
    html += city_links
    html += """
<a href="/cities/">View All Cities →</a>

</section>


<section class="sidebar-box">

<h3>
Artists
</h3>
"""
    html += artist_links
    html += """
<a href="/artists/">View All Artists →</a>

</section>


<section class="sidebar-box">

<h3>
Topics
</h3>

<a href="/tags/street-art/">Street Art</a>
<a href="/tags/urban-art/">Urban Art</a>
<a href="/tags/barcelona-street-art/">Barcelona Street Art</a>

</section>

</aside>

</div>


<section style="margin-top:70px;">

<h2 class="section-title">
Featured <span>Artists</span>
</h2>

<div class="artist-grid">
"""
    html += artist_tiles
    html += """
</div>

</section>

</main>
"""

    html += page_footer()

    Path("index.html").write_text(html, encoding="utf-8")
    print("UPDATE homepage: index.html")



def build_mixed_works(artists):
    """Round-robin works so cities and artists remain mixed."""
    works = []
    max_posts = max((len(get_active_posts(a)) for a in artists), default=0)
    for post_index in range(max_posts):
        for artist in artists:
            posts = get_active_posts(artist)
            if post_index < len(posts):
                post_url = posts[post_index].split("?")[0].rstrip("/")
                post_id = post_url.rsplit("/", 1)[-1]
                works.append({
                    "artist": artist,
                    "post_url": post_url,
                    "post_id": post_id,
                    "number": post_index + 1,
                    "slug": f"{artist['slug']}-{slugify(post_id)}",
                })
    return works


def generate_image_gallery(artists):
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR)
    ensure_directory(IMAGES_DIR)
    works = build_mixed_works(artists)
    per_page = 9
    pages = [works[i:i + per_page] for i in range(0, len(works), per_page)] or [[]]

    for work in works:
        artist = work["artist"]
        name = artist["name"]
        city = artist["city"]
        city_slug = slugify(city)
        detail_dir = IMAGES_DIR / work["slug"]
        ensure_directory(detail_dir)
        canonical = f"{BASE_URL}/images/{work['slug']}/"
        title = f"{name} Urban Art in {city} | Urban Arts News Image"
        description = (
            f"View selected urban art by {name}, connected with {city}. "
            f"Explore the artist, city and original Instagram publication."
        )
        detail = page_head(title, description, canonical)
        detail += f"""
<section class="hero">
<div class="hero-label">Urban Arts News · Selected Work · {escape(city)}</div>
<h1><span>{escape(name)}</span></h1>
<p>Selected urban-art work connected with {escape(city)}, {escape(artist['country'])}.</p>
</section>
<main class="container">
<article class="card">
<iframe class="instagram-frame" src="{instagram_embed_url(work['post_url'])}" loading="lazy"
title="{escape(name)} urban art in {escape(city)}"></iframe>
<div class="card-content">
<div class="category">{escape(name)} · {escape(city)}</div>
<h2>{escape(name)} Urban Art in {escape(city)}</h2>
<p>This selected public Instagram work forms part of the mixed Urban Arts News visual archive.</p>
<div class="tags">
<a class="tag" href="/artists/{artist['slug']}/">#{escape(name.replace(' ', ''))}</a>
<a class="tag" href="/cities/{city_slug}/">#{escape(city.replace(' ', ''))}</a>
<a class="tag" href="/tags/urban-art/">#UrbanArt</a>
</div>
<a class="button" href="{escape(work['post_url'])}" target="_blank" rel="noopener">View Original Post</a>
</div>
</article>
<section class="related">
<h2>Explore the Artist and City</h2>
<p>Continue to the complete artist profile or discover more urban art connected with {escape(city)}.</p>
<a class="button" href="/artists/{artist['slug']}/">Explore {escape(name)} →</a>
<a class="button" href="/cities/{city_slug}/">Explore {escape(city)} →</a>
<a class="button" href="/images/">All Images →</a>
</section>
</main>
"""
        detail += page_footer()
        (detail_dir / "index.html").write_text(detail, encoding="utf-8")

    total_pages = len(pages)
    for page_number, page_works in enumerate(pages, start=1):
        page_dir = IMAGES_DIR if page_number == 1 else IMAGES_DIR / "page" / str(page_number)
        ensure_directory(page_dir)
        canonical = f"{BASE_URL}/images/" if page_number == 1 else f"{BASE_URL}/images/page/{page_number}/"
        title = "Urban Art Images from Around the World | Urban Arts News"
        if page_number > 1:
            title = f"Urban Art Images – Page {page_number} | Urban Arts News"
        description = (
            "Explore a mixed visual gallery of street art and urban artists from Barcelona, "
            "Badalona, Venice and cities around the world."
        )
        cards = ""
        for work in page_works:
            artist = work["artist"]
            name = artist["name"]
            city = artist["city"]
            cards += f"""
<article class="card">
<iframe class="instagram-frame" src="{instagram_embed_url(work['post_url'])}" loading="lazy"
title="{escape(name)} urban art in {escape(city)}"></iframe>
<div class="card-content">
<div class="category">{escape(city)} · {escape(name)}</div>
<h2>{escape(name)} Urban Art in {escape(city)}</h2>
<p>Selected work from the international Urban Arts News visual archive.</p>
<a class="button" href="/images/{work['slug']}/">View Work →</a>
<a class="button" href="/artists/{artist['slug']}/">Artist →</a>
</div>
</article>
"""
        pagination = '<div class="related"><h2>Explore More Images</h2>'
        if page_number > 1:
            prev = "/images/" if page_number == 2 else f"/images/page/{page_number - 1}/"
            pagination += f'<a class="button" href="{prev}">← Previous</a> '
        if page_number < total_pages:
            pagination += f'<a class="button" href="/images/page/{page_number + 1}/">Next →</a>'
        pagination += "</div>"

        gallery = page_head(title, description, canonical)
        gallery += f"""
<section class="hero">
<div class="hero-label">Urban Arts News · Mixed International Gallery</div>
<h1>Urban Art <span>Images</span></h1>
<p>Discover artists and selected works from all featured cities, mixed across pages with a maximum of nine works per page.</p>
</section>
<main class="container">
<h2 class="section-title">Visual Archive <span>Page {page_number}</span></h2>
<div class="grid">{cards}</div>
{pagination}
</main>
"""
        gallery += page_footer()
        (page_dir / "index.html").write_text(gallery, encoding="utf-8")

    print(f"UPDATE image gallery: {len(works)} works across {len(pages)} pages")

def generate_sitemap(artists):
    urls = {
        f"{BASE_URL}/",
        f"{BASE_URL}/artists/",
        f"{BASE_URL}/cities/",
        f"{BASE_URL}/tags/street-art/",
        f"{BASE_URL}/tags/urban-art/",
        f"{BASE_URL}/tags/barcelona-street-art/",
        f"{BASE_URL}/images/",
    }

    for artist in artists:
        urls.add(f"{BASE_URL}/artists/{artist['slug']}/")
        urls.add(f"{BASE_URL}/cities/{slugify(artist['city'])}/")

    works = build_mixed_works(artists)
    total_gallery_pages = max(1, (len(works) + 8) // 9)
    for page_number in range(2, total_gallery_pages + 1):
        urls.add(f"{BASE_URL}/images/page/{page_number}/")
    for work in works:
        urls.add(f"{BASE_URL}/images/{work['slug']}/")

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for url in sorted(urls):
        sitemap += f"""  <url>
    <loc>{url}</loc>
  </url>
"""

    sitemap += "</urlset>\n"

    Path("sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("UPDATE sitemap.xml")


def main():
    print("======================================")
    print("URBAN ARTS NEWS GENERATOR")
    print("======================================")

    artists = load_artists()
    print(f"Artists loaded: {len(artists)}")
    refresh_post_status(artists)

    for artist in artists:
        generate_artist_page(artist)

    generate_artist_directory(artists)
    generate_city_pages(artists)
    generate_homepage(artists)
    generate_image_gallery(artists)
    generate_sitemap(artists)

    print("")
    print("DONE")
    print("======================================")


if __name__ == "__main__":
    main()