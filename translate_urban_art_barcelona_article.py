"""Build complete static translations of the Urban Art Barcelona article."""
from __future__ import annotations
import json, re, time
from pathlib import Path
from bs4 import BeautifulSoup, Doctype, NavigableString
from deep_translator import GoogleTranslator

BASE="https://urbanartsnews.com"
SOURCE=Path("articles/urban-art-barcelona/index.html")
LANGUAGES={
"ca":("ca","art-urba-barcelona"),"es":("es","arte-urbano-barcelona"),
"de":("de","urbane-kunst-barcelona"),"fr":("fr","art-urbain-barcelone"),
"it":("it","arte-urbana-barcellona"),"pt":("pt","arte-urbana-barcelona"),
"nl":("nl","urban-art-barcelona"),"sv":("sv","urban-konst-barcelona"),
"ja":("ja","baruserona-urban-art"),"ar":("ar","الفن-الحضري-برشلونة"),
"el":("el","astiki-techni-varkeloni"),"ko":("ko","bareusellona-dosi-misul"),
"pl":("pl","sztuka-miejska-barcelona"),"tr":("tr","barselona-kentsel-sanat"),
"zh-hans":("zh-CN","巴塞罗那城市艺术"),"ru":("ru","gorodskoe-iskusstvo-barselony"),
"da":("da","gadekunst-barcelona"),"no":("no","gatekunst-barcelona")}
NAMES=["Urban Arts News","Urban Arts News Editorial Team","Barcelona","Raval","El Gòtic","Poblenou",
"Museu d'Art Contemporani de Barcelona","MACBA","Plaça dels Àngels","Catalan","Art Is Trash",
"Francisco de Pájaro","Ashwan","Si Beriana","Camil Escruela","Mark Rox","El Rughi","CINO",
"Artevistas Gallery","Artevistas","BienCuadrado","BAS Barcelona Art Street Museum","BAS",
"English","Català","Español","Deutsch","Français","Italiano","Português","Nederlands","Svenska",
"日本語","العربية","Ελληνικά","한국어","Polski","Türkçe","简体中文","Русский","Dansk","Norsk"]
JSON_KEYS={"headline","description","name","caption","keywords"}

def url(code):
    return f"{BASE}/{code}/articles/{LANGUAGES[code][1]}/"

def protect(text):
    repl={}
    for i,value in enumerate(sorted(NAMES,key=len,reverse=True)):
        token=f"ZXQ{i:03d}QXZ"
        if value in text:
            text=text.replace(value,token); repl[token]=value
    return text,repl

def restore(text,repl):
    for token,value in repl.items():
        text=re.sub(re.escape(token),value,text,flags=re.I)
    return text

def translate_one(value,target,depth=0):
    protected,repl=protect(value)
    for attempt in range(4):
        try:
            result=GoogleTranslator(source="en",target=target).translate(protected)
            if result:
                return restore(result,repl)
        except Exception:
            time.sleep(1.5*(attempt+1))
    words=value.split()
    if len(words)>8 and depth<4:
        mid=len(words)//2
        return translate_one(" ".join(words[:mid]),target,depth+1)+" "+translate_one(" ".join(words[mid:]),target,depth+1)
    return value

def translate_values(values,target):
    out=[]
    for value in values:
        if not value.strip() or re.fullmatch(r"[\d\W_]+",value,re.UNICODE):
            out.append(value); continue
        out.append(translate_one(value,target))
        time.sleep(.12)
    return out

def collect_json(obj,items):
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key in JSON_KEYS and isinstance(value,str) and not value.startswith("http"):
                items.append((obj,key,value))
            else: collect_json(value,items)
    elif isinstance(obj,list):
        for value in obj: collect_json(value,items)

def translate_page(code,target):
    soup=BeautifulSoup(SOURCE.read_text(encoding="utf-8"),"html.parser")
    soup.html["lang"]=code
    soup.html["dir"]="rtl" if code=="ar" else "ltr"
    canonical=url(code)
    soup.find("link",rel="canonical")["href"]=canonical
    for tag in soup.find_all("meta"):
        key=tag.get("property") or tag.get("name")
        if key=="og:url": tag["content"]=canonical
    nodes=[]
    for node in soup.find_all(string=True):
        if isinstance(node,NavigableString) and not isinstance(node,Doctype) and node.parent.name not in {"script","style"} and str(node).strip():
            nodes.append(node)
    attrs=[]
    for tag in soup.find_all(True):
        for attr in ("alt","title","aria-label"):
            if tag.has_attr(attr) and str(tag[attr]).strip(): attrs.append((tag,attr,str(tag[attr])))
    for tag in soup.find_all("meta"):
        key=tag.get("name") or tag.get("property")
        if key in {"description","og:title","og:description","twitter:title","twitter:description"}:
            attrs.append((tag,"content",tag.get("content","")))
    scripts=[]; json_items=[]
    for tag in soup.find_all("script",attrs={"type":"application/ld+json"}):
        try: data=json.loads(tag.string or tag.get_text())
        except Exception: continue
        current=[]; collect_json(data,current); json_items.extend(current); scripts.append((tag,data))
    values=[str(n) for n in nodes]+[x[2] for x in attrs]+[x[2] for x in json_items]
    translated=translate_values(values,target); cursor=0
    for node in nodes:
        original=str(node); lead=original[:len(original)-len(original.lstrip())]; trail=original[len(original.rstrip()):]
        node.replace_with(lead+translated[cursor].strip()+trail); cursor+=1
    for tag,attr,_ in attrs: tag[attr]=translated[cursor].strip(); cursor+=1
    for parent,key,_ in json_items: parent[key]=translated[cursor].strip(); cursor+=1
    for tag,data in scripts:
        def localize(obj):
            if isinstance(obj,dict):
                for k,v in obj.items():
                    if k=="inLanguage": obj[k]=code
                    elif k in {"mainEntityOfPage"}: obj[k]=canonical
                    else: localize(v)
            elif isinstance(obj,list):
                for v in obj: localize(v)
        localize(data); tag.string=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    # Internal English destinations remain valid; declare their language for crawlers.
    for a in soup.find_all("a",href=True):
        if a["href"].startswith("/") and not a.get("hreflang"): a["hreflang"]="en"
    out=Path(code)/"articles"/LANGUAGES[code][1]/"index.html"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(str(soup),encoding="utf-8")
    words=len(soup.get_text(" ",strip=True).split())
    if words<900: raise RuntimeError(f"{code}: incomplete translation ({words} words)")
    print(code,out,words)

def update_sitemap():
    path=Path("sitemap.xml"); text=path.read_text(encoding="utf-8")
    entries=[]
    for code in LANGUAGES:
        page=url(code)
        if f"<loc>{page}</loc>" not in text:
            entries.append(f'<url><loc>{page}</loc><lastmod>2026-09-03</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>')
    if entries:
        text=text.replace("</urlset>","".join(entries)+"</urlset>")
        path.write_text(text,encoding="utf-8")

def main():
    for code,(target,_) in LANGUAGES.items():
        translate_page(code,target)
    update_sitemap()

if __name__=="__main__": main()
