"""Create complete static translations of the Barcelona gallery master page.

The source of truth is street-art-galleries-barcelona/index.html. Brand names,
artist names, addresses, coordinates and URLs are protected from translation.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

BASE = "https://urbanartsnews.com"
SOURCE = Path("street-art-galleries-barcelona/index.html")

LANGUAGES = {
    "ca": ("ca", "galeries-art-urba-barcelona"),
    "es": ("es", "galerias-arte-urbano-barcelona"),
    "de": ("de", "street-art-galerien-barcelona"),
    "fr": ("fr", "galeries-art-urbain-barcelone"),
    "it": ("it", "gallerie-arte-urbana-barcellona"),
    "pt": ("pt", "galerias-arte-urbana-barcelona"),
    "nl": ("nl", "street-art-galeries-barcelona"),
    "sv": ("sv", "gatukonstgallerier-barcelona"),
    "ja": ("ja", "baruserona-urban-art-gallery"),
    "ar": ("ar", "معارض-الفن-الحضري-برشلونة"),
    "el": ("el", "gkaleri-astikis-technis-varkeloni"),
    "ko": ("ko", "bareusellona-dosi-misul-gaelleori"),
    "pl": ("pl", "galerie-sztuki-miejskiej-barcelona"),
    "tr": ("tr", "barselona-kentsel-sanat-galerileri"),
    "zh-hans": ("zh-CN", "巴塞罗那城市艺术画廊"),
    "ru": ("ru", "galerei-gorodskogo-iskusstva-barselona"),
    "da": ("da", "gadekunstgallerier-barcelona"),
    "no": ("no", "gatekunstgallerier-barcelona"),
}

PROTECTED = [
    "Urban Arts News", "Artevistas", "BienCuadrado", "BAS Barcelona Art Street Museum",
    "BAS Museum", "MARK ROX", "Mark Rox", "@pop.art.pov", "Instagram", "Google Maps",
    "Okuda San Miguel", "Aryz", "Escif", "Dulk", "Mina Hamada", "Kenor",
    "Felipe Pantone", "Juanjo Surace", "PichiAvo", "Seth", "Ledania", "Charles Leval",
    "Dran", "Mike Swaney", "Vhils", "Bordalo II", "Sixe Paredes", "Os Gêmeos",
    "Camil Escruela", "GR170", "Javier Mariscal", "Nami", "Rubén Martín",
    "Sebas Velasco", "Fátima de Juan", "Bezt Etam", "Tim Marsh", "Segi Muñoz",
    "Kiara Cortez", "Akore", "Juan Manuel Pajares", "Martí Roca Balcells",
    "Andrzej Farfulowski", "Ashwan", "Matt Duffin", "Rithika Merchant", "Dai",
    "Aidan McGovern", "Richard Ashcroft", "Barcelona", "Ciutat Vella", "El Born", "Gòtic",
]

TRANSLATABLE_JSON_KEYS = {
    "name", "description", "caption", "creditText", "copyrightNotice", "keywords"
}


def page_url(code: str) -> str:
    return f"{BASE}/{code}/{LANGUAGES[code][1]}/"


def protect(text: str):
    replacements = {}
    for index, value in enumerate(sorted(PROTECTED, key=len, reverse=True)):
        token = f"ZXQ{index:03d}QXZ"
        if value in text:
            text = text.replace(value, token)
            replacements[token] = value
    return text, replacements


def restore(text: str, replacements: dict[str, str]) -> str:
    for token, value in replacements.items():
        text = re.sub(re.escape(token), value, text, flags=re.I)
    return text


def translate_values(values: list[str], target: str) -> list[str]:
    translator = GoogleTranslator(source="en", target=target)
    output = [""] * len(values)
    batch, batch_indices, size = [], [], 0

    def request(value: str, depth: int = 0) -> str:
        last_error = None
        for attempt in range(3):
            try:
                # A fresh translator instance avoids stale throttled sessions.
                result = GoogleTranslator(source="en", target=target).translate(value)
                if result:
                    return result
            except Exception as exc:
                last_error = exc
                time.sleep(1.5 * (attempt + 1))
        # Google legitimately returns the source unchanged for technical tokens
        # such as "html". Longer rejected passages are recursively reduced so
        # one difficult request never prevents the complete page translation.
        words = value.split()
        if len(words) <= 3 or depth >= 4:
            return value
        midpoint = len(words) // 2
        return request(" ".join(words[:midpoint]), depth + 1) + " " + request(
            " ".join(words[midpoint:]), depth + 1
        )

    def flush():
        nonlocal batch, batch_indices, size
        if not batch:
            return
        marker = "\nZXSEPZX\n"
        protected, maps = [], []
        for value in batch:
            item, mapping = protect(value)
            protected.append(item)
            maps.append(mapping)
        joined = marker.join(protected)
        try:
            translated = request(joined)
            parts = re.split(r"\s*ZXSEPZX\s*", translated, flags=re.I)
        except Exception:
            parts = []
        if len(parts) != len(batch):
            # Some targets reject large joined requests or alter separators.
            # Translating each item is slower, but preserves complete output.
            parts = [request(item) for item in protected]
        for idx, part, mapping in zip(batch_indices, parts, maps):
            output[idx] = restore(part, mapping)
        batch, batch_indices, size = [], [], 0
        time.sleep(0.35)

    for idx, value in enumerate(values):
        if not value.strip() or re.fullmatch(r"[\d\W_]+", value, flags=re.UNICODE):
            output[idx] = value
            continue
        projected = size + len(value) + 14
        if projected > 1800:
            flush()
        batch.append(value)
        batch_indices.append(idx)
        size += len(value) + 14
    flush()
    return output


def collect_json_strings(value, collected):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in TRANSLATABLE_JSON_KEYS and isinstance(item, str) and not item.startswith("http"):
                collected.append((value, key, item))
            else:
                collect_json_strings(item, collected)
    elif isinstance(value, list):
        for item in value:
            collect_json_strings(item, collected)


def translate_page(code: str, target: str):
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    soup.html["lang"] = code
    soup.html["dir"] = "rtl" if code == "ar" else "ltr"
    canonical = page_url(code)

    canonical_tag = soup.find("link", rel="canonical")
    canonical_tag["href"] = canonical
    for tag in soup.find_all("link", rel="alternate"):
        # Preserve the complete reciprocal hreflang cluster generated on the master.
        pass

    for tag in soup.find_all("meta"):
        prop = tag.get("property") or tag.get("name")
        if prop in {"og:url"}:
            tag["content"] = canonical

    nodes = []
    for node in soup.find_all(string=True):
        if not isinstance(node, NavigableString) or node.parent.name in {"script", "style"}:
            continue
        text = str(node)
        if text.strip():
            nodes.append(node)

    attr_items = []
    for tag in soup.find_all(True):
        for attr in ("alt", "title", "aria-label"):
            if tag.has_attr(attr) and str(tag[attr]).strip():
                attr_items.append((tag, attr, str(tag[attr])))
    for tag in soup.find_all("meta"):
        key = tag.get("name") or tag.get("property")
        if key in {"description", "keywords", "og:title", "og:description", "twitter:title", "twitter:description"}:
            attr_items.append((tag, "content", tag.get("content", "")))

    scripts = []
    json_items = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or script.get_text())
        except json.JSONDecodeError:
            continue
        current = []
        collect_json_strings(data, current)
        scripts.append((script, data, current))
        json_items.extend(current)

    source_values = [str(node) for node in nodes]
    source_values += [item[2] for item in attr_items]
    source_values += [item[2] for item in json_items]
    translated = translate_values(source_values, target)

    cursor = 0
    for node in nodes:
        original = str(node)
        leading = original[:len(original)-len(original.lstrip())]
        trailing = original[len(original.rstrip()):]
        node.replace_with(leading + translated[cursor].strip() + trailing)
        cursor += 1
    for tag, attr, _ in attr_items:
        tag[attr] = translated[cursor].strip()
        cursor += 1
    for parent, key, _ in json_items:
        parent[key] = translated[cursor].strip()
        cursor += 1
    for script, data, _ in scripts:
        # Localize page-level URLs/language while retaining venue and media URLs.
        def localize(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "inLanguage":
                        obj[k] = code
                    elif isinstance(v, str) and v.startswith(BASE + "/street-art-galleries-barcelona/"):
                        obj[k] = v.replace(BASE + "/street-art-galleries-barcelona/", canonical)
                    else:
                        localize(v)
            elif isinstance(obj, list):
                for v in obj:
                    localize(v)
        localize(data)
        script.string = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    # Self-fragment publication links stay on the current language page.
    for a in soup.find_all("a", href=True):
        if a["href"].startswith(BASE + "/street-art-galleries-barcelona/#"):
            a["href"] = canonical + "#" + a["href"].split("#", 1)[1]
        elif a["href"].startswith("/") and not a["href"].startswith(f"/{code}/"):
            a["hreflang"] = "en"

    out = Path(code) / LANGUAGES[code][1] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding="utf-8")
    print(code, out, len(soup.get_text(" ", strip=True).split()))


def main():
    for code, (target, _) in LANGUAGES.items():
        for attempt in range(3):
            try:
                translate_page(code, target)
                break
            except Exception as exc:
                if attempt == 2:
                    raise
                print(f"Retrying {code} after translation error: {exc}")
                time.sleep(4 * (attempt + 1))


if __name__ == "__main__":
    main()
