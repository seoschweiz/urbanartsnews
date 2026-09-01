"""Generate indexable language landing pages and a language directory."""

from html import escape
from pathlib import Path


BASE = "https://urbanartsnews.com"
LANGUAGES = {
    "sq": {
        "name": "Shqip", "title": "Lajme të artit urban, artistë dhe galeri",
        "description": "Zbuloni lajme të artit urban, street art, artistë, murale dhe galeri nga Barcelona dhe qytete të tjera.",
        "heading": "Lajme të artit urban",
        "intro": "Urban Arts News lidh lexuesit me artin e rrugës, grafitin, muralet, artistët bashkëkohorë dhe galeritë urbane.",
        "body": "Barcelona është fokusi ynë lokal, me profile artistësh, imazhe dhe udhëzues kulturorë. Arkivi përfshin gjithashtu krijues dhe qytete ndërkombëtare, duke treguar se si arti urban ndryshon hapësirat publike dhe krijon dialog. Vizitoni profilet e artistëve, eksploroni qytetet dhe ndiqni lajmet më të fundit nga galeritë.",
        "button": "Lexoni të gjithë faqen në shqip", "explore": "Eksploroni Urban Arts News",
    },
    "de": {
        "name": "Deutsch", "title": "Urban Art News, Künstler und Galerien",
        "description": "Entdecke Urban Art News, Street Art, Künstler, Murals und Galerien aus Barcelona und Städten weltweit.",
        "heading": "Urban Art News auf Deutsch",
        "intro": "Urban Arts News verbindet aktuelle urbane Kunst mit Street Art, Graffiti, Murals, Künstlerprofilen und unabhängigen Galerien.",
        "body": "Barcelona bildet unseren lokalen Schwerpunkt. Dazu kommen ausgewählte Künstler und visuelle Geschichten aus internationalen Städten. Die Plattform zeigt, wie Kunst im öffentlichen Raum entsteht, wie sie sich in Galerien weiterentwickelt und welche Menschen hinter den Werken stehen. Entdecke Künstlerprofile, Stadtarchive, Bilder und aktuelle Nachrichten aus der Urban-Art-Szene.",
        "button": "Gesamte Website auf Deutsch lesen", "explore": "Urban Arts News entdecken",
    },
    "es": {
        "name": "Español", "title": "Noticias de arte urbano, artistas y galerías",
        "description": "Descubre noticias de arte urbano, street art, artistas, murales y galerías de Barcelona y otras ciudades.",
        "heading": "Noticias de arte urbano",
        "intro": "Urban Arts News conecta el arte urbano contemporáneo con el street art, el graffiti, los murales, los artistas y las galerías independientes.",
        "body": "Barcelona es nuestro principal foco local, con perfiles de artistas, imágenes y guías culturales. El archivo también presenta creadores y ciudades internacionales para mostrar cómo el arte urbano transforma el espacio público y genera nuevas conversaciones. Explora artistas, ciudades, galerías y las últimas noticias de la escena urbana.",
        "button": "Leer todo el sitio en español", "explore": "Explorar Urban Arts News",
    },
    "ca": {
        "name": "Català", "title": "Notícies d’art urbà, artistes i galeries",
        "description": "Descobreix Urban Arts News en català: art urbà, street art, artistes, murals, galeries, exposicions i cultura visual de Barcelona i del món.",
        "heading": "Notícies d’art urbà",
        "intro": "Urban Arts News és una plataforma independent dedicada a l’art urbà, l’street art, el grafiti, els murals, els artistes i les galeries que transformen la cultura visual de les ciutats.",
        "body": "Barcelona és el nostre principal focus local, però la mirada s’estén a artistes, espais i ciutats de tot el món.",
        "button": "Llegir tot el web en català", "explore": "Explora Urban Arts News",
        "sections": [
            ("Una mirada independent a l’art urbà", "Urban Arts News neix amb la voluntat de documentar i compartir formes d’expressió que sovint apareixen lluny dels circuits culturals tradicionals. L’art urbà pot començar en una paret, en un objecte abandonat, en una persiana metàl·lica o en una intervenció efímera al carrer. També pot continuar en un estudi, una galeria, un museu o una col·lecció privada. La nostra feina és connectar aquests espais i explicar les històries que hi ha darrere de les obres, sense perdre l’energia directa que caracteritza la cultura urbana."),
            ("Barcelona, ciutat d’art i experimentació", "Barcelona ocupa un lloc central dins del projecte. Els seus barris combinen arquitectura, vida quotidiana, turisme, conflictes urbans i una escena creativa internacional. A Urban Arts News presentem artistes vinculats amb Barcelona, obres seleccionades, fotografies de la ciutat i informació sobre espais culturals. El nostre directori permet descobrir creadors locals i internacionals que treballen amb pintura, grafiti, collage, instal·lació, materials reciclats, tipografia, escultura i altres llenguatges contemporanis."),
            ("Artistes i obres amb identitat pròpia", "Cada perfil d’artista ofereix una entrada clara a la seva pràctica. No volem presentar l’art urbà com una categoria uniforme: cada creador desenvolupa una relació diferent amb el carrer, els materials i el públic. Alguns artistes intervenen directament en l’espai públic; d’altres traslladen l’experiència urbana a la pintura, a l’escultura o a formats digitals. Les pàgines individuals connecten biografia, ciutat, imatges i publicacions originals perquè el lector pugui entendre millor el context de cada obra."),
            ("Galeries, exposicions i museus", "Les galeries d’art urbà tenen una funció important. Ofereixen als artistes espais per experimentar, presentar noves sèries i entrar en contacte amb col·leccionistes i públics diversos. També organitzen inauguracions, converses, tallers i esdeveniments que reforcen la comunitat cultural. La nostra guia de galeries de Barcelona inclou espais com Artevistas, BienCuadrado i BAS Barcelona Art Street Museum. A més, el registre Urban Art Gallery News segueix exposicions i notícies relacionades amb la vida de les galeries."),
            ("Ciutats, imatges i cultura visual", "L’art urbà sempre està relacionat amb el lloc on apareix. Per això organitzem una part important del contingut per ciutats. Les pàgines urbanes connecten artistes, notícies, imatges i galeries amb el seu context geogràfic. Barcelona és el punt de partida, però l’arxiu també incorpora Badalona, Los Angeles, Buenos Aires, Venècia, Ontario i altres localitzacions. Les galeries fotogràfiques ajuden a entendre l’arquitectura, els carrers i els paisatges que envolten les pràctiques artístiques."),
            ("Una plataforma oberta a nous descobriments", "Urban Arts News continuarà creixent amb nous artistes, ciutats, imatges, vídeos, exposicions i històries. L’objectiu no és acumular pàgines sense context, sinó construir un arxiu navegable que sigui útil per a persones interessades en l’art, viatgers, creadors, galeries i col·leccionistes. Cada secció està connectada amb altres continguts perquè sigui fàcil passar d’un artista a la seva ciutat, d’una imatge a una galeria o d’una notícia a una exposició."),
            ("Per a lectors, artistes i espais culturals", "La plataforma està pensada tant per a qui descobreix l’art urbà per primera vegada com per a persones que ja coneixen l’escena. Els lectors poden trobar idees per visitar una ciutat, seguir un artista o descobrir una exposició. Els creadors disposen d’un context on la seva obra pot connectar amb altres pràctiques sense quedar reduïda a una simple imatge. Les galeries i els espais culturals poden arribar a un públic interessat en propostes independents. Aquesta combinació converteix Urban Arts News en un punt de trobada entre carrer, estudi, galeria, museu i comunitat."),
        ],
        "newsletter_title": "Rep Urban Arts News gratuïtament",
        "newsletter_text": "Subscriu-te per rebre una selecció personal de notícies, artistes, galeries i oportunitats relacionades amb l’art urbà.",
        "email_label": "La teva adreça electrònica",
        "consent": "Accepto rebre Urban Arts News i ofertes seleccionades per correu electrònic. Em puc donar de baixa en qualsevol moment.",
        "subscribe": "Subscriu-m’hi gratuïtament",
    },
    "pt": {
        "name": "Português", "title": "Notícias de arte urbana, artistas e galerias",
        "description": "Descubra notícias de arte urbana, street art, artistas, murais e galerias de Barcelona e outras cidades.",
        "heading": "Notícias de arte urbana",
        "intro": "Urban Arts News conecta arte urbana contemporânea, street art, graffiti, murais, artistas e galerias independentes.",
        "body": "Barcelona é o nosso principal foco local, com perfis de artistas, imagens e guias culturais. O arquivo também apresenta criadores e cidades internacionais, mostrando como a arte urbana transforma o espaço público e cria novas conversas. Explore artistas, cidades, galerias e as notícias mais recentes da cena urbana.",
        "button": "Ler todo o site em português", "explore": "Explorar Urban Arts News",
    },
    "it": {
        "name": "Italiano", "title": "Notizie di arte urbana, artisti e gallerie",
        "description": "Scopri notizie di arte urbana, street art, artisti, murales e gallerie di Barcellona e altre città.",
        "heading": "Notizie di arte urbana",
        "intro": "Urban Arts News collega l’arte urbana contemporanea con street art, graffiti, murales, artisti e gallerie indipendenti.",
        "body": "Barcellona è il nostro principale centro locale, con profili di artisti, immagini e guide culturali. L’archivio presenta anche creatori e città internazionali per mostrare come l’arte urbana trasformi lo spazio pubblico e generi nuove conversazioni. Esplora artisti, città, gallerie e le ultime notizie della scena urbana.",
        "button": "Leggi tutto il sito in italiano", "explore": "Esplora Urban Arts News",
    },
    "fr": {
        "name": "Français", "title": "Actualités de l’art urbain, artistes et galeries",
        "description": "Découvrez l’actualité de l’art urbain, du street art, des artistes, des fresques et des galeries à Barcelone et ailleurs.",
        "heading": "Actualités de l’art urbain",
        "intro": "Urban Arts News relie l’art urbain contemporain au street art, au graffiti, aux fresques, aux artistes et aux galeries indépendantes.",
        "body": "Barcelone constitue notre principal ancrage local, avec des portraits d’artistes, des images et des guides culturels. Les archives présentent également des créateurs et des villes du monde entier afin de montrer comment l’art urbain transforme l’espace public. Découvrez les artistes, les villes, les galeries et les dernières nouvelles de la scène urbaine.",
        "button": "Lire tout le site en français", "explore": "Explorer Urban Arts News",
    },
    "ja": {
        "name": "日本語", "title": "アーバンアートニュース、アーティスト、ギャラリー",
        "description": "バルセロナと世界の都市から、アーバンアート、ストリートアート、アーティスト、壁画、ギャラリーのニュースを紹介します。",
        "heading": "アーバンアートニュース",
        "intro": "Urban Arts Newsは、現代のアーバンアート、ストリートアート、グラフィティ、壁画、アーティスト、独立系ギャラリーを紹介するプラットフォームです。",
        "body": "バルセロナを主な拠点として、アーティストのプロフィール、作品画像、文化ガイドを掲載しています。さらに世界各地のアーティストや都市を取り上げ、アーバンアートが公共空間をどのように変え、新しい対話を生み出すかを伝えます。アーティスト、都市、ギャラリー、最新ニュースをご覧ください。",
        "button": "サイト全体を日本語で読む", "explore": "Urban Arts Newsを見る",
    },
    "ar": {
        "name": "العربية", "title": "أخبار الفن الحضري والفنانين والمعارض",
        "description": "اكتشف أخبار الفن الحضري وفن الشارع والفنانين والجداريات والمعارض من برشلونة ومدن أخرى حول العالم.",
        "heading": "أخبار الفن الحضري",
        "intro": "تربط Urban Arts News بين الفن الحضري المعاصر وفن الشارع والغرافيتي والجداريات والفنانين والمعارض المستقلة.",
        "body": "برشلونة هي محورنا المحلي الرئيسي، مع ملفات للفنانين وصور وأدلة ثقافية. ويعرض الأرشيف أيضاً مبدعين ومدناً من أنحاء العالم ليوضح كيف يغير الفن الحضري الفضاء العام ويخلق حوارات جديدة. استكشف الفنانين والمدن والمعارض وآخر أخبار المشهد الفني الحضري.",
        "button": "اقرأ الموقع كاملاً بالعربية", "explore": "استكشف Urban Arts News",
    },
}

CSS = """*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f4f2;color:#171717;line-height:1.7}a{color:inherit}.top{background:#090909;color:#fff;padding:20px 6%}.logo{text-decoration:none;font-size:28px;font-weight:900}.logo span,.accent{color:#ff5b21}.hero{background:#111;color:#fff;padding:80px 6%}.hero h1{font-size:clamp(42px,7vw,82px);line-height:1;margin:0 0 22px;max-width:1000px}.hero p{font-size:20px;color:#ccc;max-width:850px}.wrap{width:min(1050px,90%);margin:55px auto}.copy{background:#fff;padding:clamp(28px,5vw,55px);box-shadow:0 10px 35px #00000012}.copy h2{font-size:clamp(25px,4vw,36px);line-height:1.15;margin:40px 0 12px}.copy h2:first-child{margin-top:0}.copy p{font-size:18px}.links{display:flex;flex-wrap:wrap;gap:12px;margin:30px 0}.button{display:inline-block;border:0;background:#ff5b21;color:#fff;text-decoration:none;font-weight:800;padding:13px 18px;cursor:pointer}.button.secondary{background:#111}.newsletter{margin-top:45px;padding:clamp(25px,5vw,42px);background:#111;color:#fff}.newsletter h2{margin-top:0}.newsletter p{color:#ccc}.field{display:block;font-size:13px;font-weight:800;text-transform:uppercase;margin:18px 0 7px}.email{width:100%;padding:15px;border:2px solid #ddd;font-size:17px}.consent{display:flex;gap:10px;align-items:flex-start;margin:16px 0;font-size:13px;color:#ccc}.consent input{margin-top:5px}.languages{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.languages a{background:#fff;padding:18px;text-decoration:none;font-weight:800;border-left:4px solid #ff5b21}footer{background:#090909;color:#aaa;text-align:center;padding:35px;margin-top:60px}@media(max-width:700px){.languages{grid-template-columns:1fr}.hero{padding:55px 5%}}"""


def alternates():
    links = ['<link rel="alternate" hreflang="x-default" href="https://urbanartsnews.com/languages/">']
    links += [f'<link rel="alternate" hreflang="{code}" href="{BASE}/{code}/urban-art-news/">' for code in LANGUAGES]
    links += [f'<link rel="alternate" hreflang="en" href="{BASE}/">']
    return "\n".join(links)


def page(code, item):
    canonical = f"{BASE}/{code}/urban-art-news/"
    direction = ' dir="rtl"' if code == "ar" else ""
    translator = f"https://urbanartsnews-com.translate.goog/?_x_tr_sl=en&_x_tr_tl={code}&_x_tr_hl={code}&_x_tr_pto=sc"
    sections = "".join(f"<section><h2>{escape(title)}</h2><p>{escape(text)}</p></section>" for title, text in item.get("sections", []))
    newsletter = ""
    if item.get("newsletter_title"):
        newsletter = f'''<section class="newsletter"><h2>{escape(item['newsletter_title'])}</h2><p>{escape(item['newsletter_text'])}</p><form action="https://formspree.io/f/mnpqpdld" method="POST"><label class="field" for="email-{code}">{escape(item['email_label'])}</label><input class="email" id="email-{code}" type="email" name="email" autocomplete="email" required><input type="hidden" name="language" value="{code}"><input type="hidden" name="_subject" value="New UrbanArtsNews {code} subscriber"><input type="hidden" name="_next" value="https://urbanartsnews.com/subscribe/thank-you/"><label class="consent"><input type="checkbox" name="consent" value="yes" required><span>{escape(item['consent'])}</span></label><button class="button" type="submit">{escape(item['subscribe'])} →</button></form></section>'''
    return f'''<!DOCTYPE html><html lang="{code}"{direction}><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(item['title'])} | Urban Arts News</title><meta name="description" content="{escape(item['description'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">
{alternates()}<style>{CSS}</style></head><body><header class="top"><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a></header>
<section class="hero"><h1>{escape(item['heading'])}</h1><p>{escape(item['intro'])}</p></section><main class="wrap"><article class="copy"><h2>{escape(item['explore'])}</h2><p>{escape(item['body'])}</p>{sections}<div class="links"><a class="button" href="/artists/">Artistes</a><a class="button" href="/urban-art-cities/">Ciutats</a><a class="button" href="/urban-art-gallery-news/">Notícies de galeries</a><a class="button" href="/street-art-galleries-barcelona/">Galeries de Barcelona</a></div><a class="button secondary" href="{translator}" rel="nofollow noopener">{escape(item['button'])} →</a>{newsletter}</article></main><footer><a href="/languages/">All Languages</a> · <a href="/">Urban Arts News</a></footer></body></html>'''


def directory():
    cards = "".join(f'<a href="/{code}/urban-art-news/" hreflang="{code}">{escape(item["name"])}</a>' for code, item in LANGUAGES.items())
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Urban Art News in Different Languages</title><meta name="description" content="Read Urban Arts News introductions in Albanian, German, Spanish, Catalan, Portuguese, Italian, French, Japanese and Arabic."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}/languages/">{alternates()}<style>{CSS}</style></head><body><header class="top"><a class="logo" href="/">URBAN <span>ARTS</span> NEWS</a></header><section class="hero"><h1>Urban Art News <span class="accent">Languages</span></h1><p>Choose a language to discover street art, artists, cities, galleries and urban culture.</p></section><main class="wrap"><div class="languages">{cards}</div></main><footer><a href="/">Urban Arts News</a></footer></body></html>'''


def main():
    for code, item in LANGUAGES.items():
        output = Path(code) / "urban-art-news" / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page(code, item), encoding="utf-8")
    output = Path("languages/index.html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(directory(), encoding="utf-8")
    print(f"Language pages generated: {len(LANGUAGES)} plus directory")


if __name__ == "__main__":
    main()
