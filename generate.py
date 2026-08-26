import json
import re
from html import escape
from pathlib import Path


# =========================================================
# URBAN ARTS NEWS GENERATOR
# =========================================================

BASE_URL = "https://urbanartsnews.com"
DATA_FILE = Path("data/artists.json")

ARTISTS_DIR = Path("artists")
CITIES_DIR = Path("cities")


# =========================================================
# HELPERS
# =========================================================

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def instagram_embed_url(url):
    """
    Converts:
    https://www.instagram.com/p/ABC123/
    into:
    https://www.instagram.com/p/ABC123/embed/
    """
    clean = url.split("?")[0].rstrip("/")
    return clean + "/embed/"


def ensure_directory(path):
    path.mkdir(parents=True, exist_ok=True)


def load_artists():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


# =========================================================
# COMMON HTML
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
    padding:90px 6%;
}}

.hero-label {{
    color:#ff5b21;
    font-size:13px;
    font-weight:800;
    text-transform:uppercase;
    margin-bottom:12px;
}}

.hero h1 {{
    font-size:clamp(48px,8vw,90px);
    line-height:.95;
    text-transform:uppercase;
    letter-spacing:-3px;
    margin-bottom:20px;
}}

.hero h1 span {{
    color:#ff5b21;
}}

.hero p {{
    max-width:820px;
    font-size:18px;
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
}}

.tag {{
    background:#eee;
    padding:6px 9px;
    font-size:11px;
    font-weight:700;
}}

.button {{
    display:inline-block;
    background:#ff5b21;
    color:white;
    padding:13px 18px;
    font-size:13px;
    font-weight:800;
    text-transform:uppercase;
    margin-top:10px;
}}

.button:hover {{
    background:#111;
}}

.info-box {{
    background:#111;
    color:white;
    padding:30px;
    margin-bottom:40px;
}}

.info-box strong {{
    color:#ff5b21;
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
}}
</style>
</head>

<body>

<header>
<a href="/" class="logo">
URBAN <span>ARTS</span> NEWS
</a>

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

    artist_dir = ARTISTS_DIR / slug
    ensure_directory(artist_dir)

    output_file = artist_dir / "index.html"

    # Do not overwrite manually created artist pages.
    if output_file.exists():
        print(f"KEEP existing artist page: {output_file}")
        return

    canonical = f"{BASE_URL}/artists/{slug}/"

    title = f"{name} | {city} Urban Artist | Urban Arts News"

    description = (
        f"Discover {name}, an urban artist connected with {city}, "
        f"{country}. Explore selected Instagram posts, street art "
        f"and contemporary urban culture on Urban Arts News."
    )

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
{escape(name)} Urban Art · Post {index}
</h3>

<p>
Selected work by {escape(name)} from the contemporary urban-art scene
connected with {escape(city)}, {escape(country)}.
</p>

<div class="tags">

<a class="tag" href="/tags/street-art/">
#StreetArt
</a>

<a class="tag" href="/tags/urban-art/">
#UrbanArt
</a>

<a class="tag" href="/cities/{slugify(city)}/">
#{escape(city.replace(" ", ""))}
</a>

</div>

</div>

</article>
"""

    html = page_head(title, description, canonical)

    html += f"""
<section class="hero">

<div class="hero-label">
Urban Arts News · Artist Profile
</div>

<h1>
<span>{escape(name)}</span>
</h1>

<p>
Discover {escape(name)}, urban art and selected Instagram works
connected with {escape(city)}, {escape(country)}.
</p>

</section>


<main class="container">

<div class="info-box">

<p>
<strong>Artist:</strong> {escape(name)}
</p>

<p>
<strong>City:</strong> {escape(city)}
</p>

<p>
<strong>Country:</strong> {escape(country)}
</p>

<p>
<strong>Instagram:</strong>
<a href="{instagram}" target="_blank" rel="noopener">
{escape(instagram)}
</a>
</p>

</div>


<h2 class="section-title">
Selected <span>{escape(name)} Posts</span>
</h2>

<div class="grid">

{post_html}

</div>


<p style="margin-top:40px;">

<a class="button" href="/artists/">
← All Artists
</a>

<a class="button" href="/cities/{slugify(city)}/">
Explore {escape(city)}
</a>

</p>

</main>
"""

    html += page_footer()

    output_file.write_text(html, encoding="utf-8")

    print(f"CREATE artist page: {output_file}")


# =========================================================
# ARTISTS DIRECTORY
# =========================================================

def generate_artist_directory(artists):
    ensure_directory(ARTISTS_DIR)

    cards = ""

    for number, artist in enumerate(artists, start=1):
        name = artist["name"]
        slug = artist["slug"]
        city = artist["city"]
        country = artist["country"]

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
Urban artist featured by Urban Arts News.
Explore selected works and Instagram posts from
{escape(city)}, {escape(country)}.
</p>

<div class="tags">

<a class="tag" href="/cities/{slugify(city)}/">
{escape(city)}
</a>

<span class="tag">
{escape(country)}
</span>

<span class="tag">
Urban Art
</span>

</div>

<a class="button"
href="/artists/{slug}/">
Explore {escape(name)} →
</a>

</div>

</article>
"""

    title = "Urban Artists | Urban Arts News"

    description = (
        "Discover street artists, mural artists and contemporary urban "
        "artists from Barcelona, Italy and cities around the world."
    )

    html = page_head(
        title,
        description,
        f"{BASE_URL}/artists/"
    )

    html += """
<section class="hero">

<div class="hero-label">
Urban Arts News · Artist Directory
</div>

<h1>
Urban <span>Artists</span>
</h1>

<p>
Discover artists working between street art, graffiti,
murals, contemporary art and urban culture.
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
        city = artist["city"]

        if city not in cities:
            cities[city] = []

        cities[city].append(artist)

    city_directory_cards = ""

    for city in sorted(cities.keys()):
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

        city_dir = CITIES_DIR / city_slug
        ensure_directory(city_dir)

        artist_cards = ""

        for artist in city_artists:
            artist_name = artist["name"]
            artist_slug = artist["slug"]

            artist_cards += f"""
<article class="card">

<div class="card-content">

<div class="category">
{escape(city)} Urban Artist
</div>

<h2>
{escape(artist_name)}
</h2>

<p>
Explore selected works and Instagram posts by
{escape(artist_name)}.
</p>

<a class="button"
href="/artists/{artist_slug}/">
Explore Artist →
</a>

</div>

</article>
"""

        city_title = f"{city} Urban Art & Street Artists | Urban Arts News"

        city_description = (
            f"Discover urban artists, street art and contemporary "
            f"urban culture from {city} on Urban Arts News."
        )

        city_html = page_head(
            city_title,
            city_description,
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
Discover street artists, urban creators and contemporary
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

    # Main cities directory
    cities_html = page_head(
        "Urban Art Cities | Urban Arts News",
        "Explore street art and urban artists by city on Urban Arts News.",
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
Explore artists and contemporary urban culture city by city.
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
        urls.add(
            f"{BASE_URL}/artists/{artist['slug']}/"
        )

        urls.add(
            f"{BASE_URL}/cities/{slugify(artist['city'])}/"
        )

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

    for url in sorted(urls):
        sitemap += f"""
  <url>
    <loc>{url}</loc>
  </url>
"""

    sitemap += """
</urlset>
"""

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

    # Existing manually-created artist pages stay untouched.
    # New artist pages are generated automatically.
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
