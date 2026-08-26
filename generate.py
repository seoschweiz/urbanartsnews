from pathlib import Path

content = r'''import json
import re
from html import escape
from pathlib import Path

BASE_URL = "https://urbanartsnews.com"
DATA_FILE = Path("data/artists.json")

ARTISTS_DIR = Path("artists")
CITIES_DIR = Path("cities")

# These artist pages were manually designed and should remain untouched.
MANUAL_ARTIST_PAGES = {
    "art-is-trash",
    "ashwan",
    "si-beriana",
}


# =========================================================
# HELPERS
# =========================================================

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


def hashtags_from_tags(tags):
    output = []
    for tag in tags:
        clean = re.sub(r"[^A-Za-z0-9]+", "", tag)
        if clean:
            output.append("#" + clean)
    return output


# =========================================================
# COMMON PAGE PARTS
# =========================================================

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
    line-height:1.65;
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
    font-size:clamp(50px,8vw,94px);
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
    width:min(1300px,92%);
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
    padding:24px;
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
    margin-top:15px;
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
    margin-top:14px;
}}

.button:hover {{
    background:#111;
}}

.related {{
    margin-top:50px;
    background:white;
    padding:30px;
    box-shadow:0 5px 18px rgba(0,0,0,.06);
}}

.related h2 {{
    text-transform:uppercase;
    margin-bottom:15px;
}}

footer {{
    margin-top:70px;
    background:#090909;
    color:#888;
    text-align:center;
    padding:40px;
    font-size:13px;
}}

@media(max-width:1000px) {{
    .profile-layout {{
        grid-template-columns:1fr;
    }}

    .grid {{
        grid-template-columns:repeat(2,1fr);
    }}
}}

@media(max-width:700px) {{
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

    .grid {{
        grid-template-columns:1fr;
    }}

    .instagram-frame {{
        height:620px;
    }}

    .profile-copy {{
        padding:25px;
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


# =========================================================
# ARTIST PAGE
# =========================================================

def generate_artist_page(artist):
    name = artist["name"]
    slug = artist["slug"]
    city = artist["city"]
    country = artist["country"]
    instagram = artist["instagram"]
    posts = artist.get("posts", [])
    headline = artist.get(
        "headline",
        f"{name} – Urban Art from {city}"
    )
    bio = artist.get(
        "bio",
        f"{name} is an urban artist connected with {city}, {country}."
    )
    tags = artist.get("tags", ["Urban Art", city])

    artist_dir = ARTISTS_DIR / slug
    ensure_directory(artist_dir)
    output_file = artist_dir / "index.html"

    # Preserve the three hand-built Barcelona pages.
    if slug in MANUAL_ARTIST_PAGES and output_file.exists():
        print(f"KEEP manual artist page: {output_file}")
        return

    canonical = f"{BASE_URL}/artists/{slug}/"
    city_slug = slugify(city)

    title = f"{name} | {city} Urban Artist | Urban Arts News"
    description = (
        f"Discover {name}, {headline}. Explore selected Instagram posts "
        f"and urban art connected with {city}, {country}."
    )

    tag_html = ""
    for tag in tags:
        hashtag = re.sub(r"[^A-Za-z0-9]+", "", tag)
        if hashtag:
            tag_html += f'<span class="tag">#{escape(hashtag)}</span>\n'

    post_html = ""

    for index, post in enumerate(posts, start=1):
        embed = instagram_embed_url(post)

        post_html += f"""
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

<h3>
{escape(name)} · Selected Work {index}
</h3>

<p>
Selected Instagram work by {escape(name)}, featured in the
Urban Arts News archive for {escape(city)}, {escape(country)}.
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

<div class="hero-label">
Urban Arts News · {escape(city)} Featured Artist
</div>

<h1>
<span>{escape(name)}</span>
</h1>

<p>
{escape(headline)}
</p>

</section>


<main class="container">

<section class="profile-layout">

<div class="profile-copy">

<h2>
About <span>{escape(name)}</span>
</h2>

<p>
{escape(bio)}
</p>

<p>
Urban Arts News presents {escape(name)} as a featured artist connected
with {escape(city)}, combining selected Instagram works with an
independent editorial profile and city-based discovery.
</p>

<h3 style="margin-top:28px;">
Artist Tags
</h3>

<div class="tags">
{tag_html}
</div>

</div>


<aside class="info-box">

<h3>
Artist Information
</h3>

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

<div class="meta">
<strong>Urban Arts News</strong>
Featured Artist
</div>

<a class="button"
href="{escape(instagram)}"
target="_blank"
rel="noopener">
View Instagram
</a>

</aside>

</section>


<h2 class="section-title">
Selected <span>{escape(name)} Posts</span>
</h2>

<div class="grid">

{post_html}

</div>


<section class="related">

<h2>
Explore {escape(city)}
</h2>

<p>
Discover more urban artists and street-art culture connected with
{escape(city)} on Urban Arts News.
</p>

<a class="button"
href="/cities/{city_slug}/">
Explore {escape(city)} →
</a>

<a class="button"
href="/artists/">
All Artists →
</a>

</section>

</main>
"""

    html += page_footer()

    output_file.write_text(html, encoding="utf-8")
    print(f"UPDATE artist page: {output_file}")


# =========================================================
# ARTIST DIRECTORY
# =========================================================

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

<div class="category">
Artist {number:02d} · {escape(city)}
</div>

<h2>
{escape(name)}
</h2>

<p>
{escape(headline)}
</p>

<div class="tags">
<a class="tag" href="/cities/{slugify(city)}/">#{escape(city.replace(" ", ""))}</a>
<span class="tag">#{escape(country.replace(" ", ""))}</span>
<span class="tag">#UrbanArt</span>
</div>

<a class="button"
href="/artists/{slug}/">
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

<h2 class="section-title">
Featured <span>Artists</span>
</h2>

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


# =========================================================
# CITY PAGES
# =========================================================

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

<div class="category">
Urban Arts News · City
</div>

<h2>
{escape(city)}
</h2>

<p>
Explore {len(city_artists)} featured urban artist{plural}
connected with {escape(city)}.
</p>

<a class="button"
href="/cities/{city_slug}/">
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

<div class="category">
{escape(city)} Featured Artist
</div>

<h2>
{escape(artist_name)}
</h2>

<p>
{escape(headline)}
</p>

<a class="button"
href="/artists/{artist_slug}/">
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

<div class="hero-label">
Urban Arts News · City
</div>

<h1>
<span>{escape(city)}</span>
</h1>

<p>
Discover selected street artists, urban creators and contemporary
visual culture connected with {escape(city)}.
</p>

</section>

<main class="container">

<h2 class="section-title">
Artists in <span>{escape(city)}</span>
</h2>

<div class="grid">
{artist_cards}
</div>

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

<div class="hero-label">
Urban Arts News · City Directory
</div>

<h1>
Urban Art <span>Cities</span>
</h1>

<p>
Explore curated artists and contemporary urban culture city by city.
Barcelona is our deeper local focus, while international cities begin
with one selected featured artist.
</p>

</section>

<main class="container">

<h2 class="section-title">
Explore <span>Cities</span>
</h2>

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


# =========================================================
# SITEMAP
# =========================================================

def generate_sitemap(artists):
    urls = {
        f"{BASE_URL}/",
        f"{BASE_URL}/artists/",
        f"{BASE_URL}/cities/",
        f"{BASE_URL}/tags/street-art/",
        f"{BASE_URL}/tags/urban-art/",
        f"{BASE_URL}/tags/barcelona-street-art/",
    }

    for artist in artists:
        urls.add(f"{BASE_URL}/artists/{artist['slug']}/")
        urls.add(f"{BASE_URL}/cities/{slugify(artist['city'])}/")

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for url in sorted(urls):
        sitemap += f"""  <url>
    <loc>{url}</loc>
  </url>
"""

    sitemap += "</urlset>\n"

    Path("sitemap.xml").write_text(
        sitemap,
        encoding="utf-8"
    )

    print("UPDATE sitemap.xml")


# =========================================================
# MAIN
# =========================================================

def main():
    print("======================================")
    print("URBAN ARTS NEWS GENERATOR")
    print("======================================")

    artists = load_artists()

    print(f"Artists loaded: {len(artists)}")

    for artist in artists:
        generate_artist_page(artist)

    generate_artist_directory(artists)
    generate_city_pages(artists)
    generate_sitemap(artists)

    print("")
    print("DONE")
    print("======================================")


if __name__ == "__main__":
    main()
'''

path = Path("/mnt/data/generate_perfect_artist.py")
path.write_text(content, encoding="utf-8")

compile(content, str(path), "exec")
print("Created and syntax-checked:", path)
