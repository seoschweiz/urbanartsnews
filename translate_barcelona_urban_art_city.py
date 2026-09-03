"""Create complete static translations of the Barcelona urban-art city page."""
from __future__ import annotations
import json,re,time
from pathlib import Path
from bs4 import BeautifulSoup,Doctype,NavigableString
from deep_translator import GoogleTranslator

BASE="https://urbanartsnews.com"
SOURCE=Path("urban-art-city/barcelona/spain/index.html")
LANGUAGES={
"ca":("ca","ciutat-art-urba/barcelona/espanya"),"es":("es","ciudad-arte-urbano/barcelona/espana"),
"de":("de","urbane-kunst-stadt/barcelona/spanien"),"fr":("fr","ville-art-urbain/barcelone/espagne"),
"it":("it","citta-arte-urbana/barcellona/spagna"),"pt":("pt","cidade-arte-urbana/barcelona/espanha"),
"nl":("nl","urban-art-stad/barcelona/spanje"),"sv":("sv","urban-konst-stad/barcelona/spanien"),
"ja":("ja","urban-art-city/baruserona/supein"),"ar":("ar","مدينة-الفن-الحضري/برشلونة/إسبانيا"),
"el":("el","poli-astikis-technis/varkeloni/ispania"),"ko":("ko","dosi-misul/bareusellona/seupein"),
"pl":("pl","miasto-sztuki-miejskiej/barcelona/hiszpania"),"tr":("tr","kentsel-sanat-sehri/barselona/ispanya"),
"zh-hans":("zh-CN","城市艺术/巴塞罗那/西班牙"),"ru":("ru","gorod-ulichnogo-iskusstva/barselona/ispaniya"),
"da":("da","urban-kunst-by/barcelona/spanien"),"no":("no","urban-kunst-by/barcelona/spania")}
TITLES={
"ca":"Art urbà i artistes de carrer de Barcelona | Urban Arts News",
"es":"Arte urbano y artistas callejeros de Barcelona | Urban Arts News",
"de":"Urbane Kunst und Street-Art-Künstler in Barcelona | Urban Arts News",
"fr":"Art urbain et artistes de rue à Barcelone | Urban Arts News",
"it":"Arte urbana e street artist a Barcellona | Urban Arts News",
"pt":"Arte urbana e artistas de rua de Barcelona | Urban Arts News",
"nl":"Urban art en straatkunstenaars in Barcelona | Urban Arts News",
"sv":"Urban konst och gatukonstnärer i Barcelona | Urban Arts News",
"ja":"バルセロナのアーバンアートとストリートアーティスト | Urban Arts News",
"ar":"الفن الحضري وفنانو الشوارع في برشلونة | Urban Arts News",
"el":"Αστική τέχνη και καλλιτέχνες δρόμου στη Βαρκελώνη | Urban Arts News",
"ko":"바르셀로나 도시 예술과 거리 예술가 | Urban Arts News",
"pl":"Sztuka miejska i artyści uliczni w Barcelonie | Urban Arts News",
"tr":"Barselona kentsel sanatı ve sokak sanatçıları | Urban Arts News",
"zh-hans":"巴塞罗那城市艺术与街头艺术家 | Urban Arts News",
"ru":"Городское искусство и уличные художники Барселоны | Urban Arts News",
"da":"Urban kunst og gadekunstnere i Barcelona | Urban Arts News",
"no":"Urban kunst og gatekunstnere i Barcelona | Urban Arts News"}
PROTECTED=["Urban Arts News","Barcelona","Art Is Trash","Ashwan","Si Beriana","Xavi Ceerre","Camil Escruela",
"Mark Rox","Pop Art POV","Eslicer","Werens Graffiti","El Rughi","Stefano Phen","CINO","Instagram",
"Festival Cruïlla","BAS Museum","Time Out Worldwide","Barcelona Secreta","Google Maps",
"English","Català","Español","Deutsch","Français","Italiano","Português","Nederlands","Svenska",
"日本語","العربية","Ελληνικά","한국어","Polski","Türkçe","简体中文","Русский","Dansk","Norsk"]
JSON_KEYS={"name","description","headline","caption","keywords"}

def page_url(code):
    return f"{BASE}/{code}/{LANGUAGES[code][1]}/"

def protect(text):
    replacements={}
    for i,value in enumerate(sorted(PROTECTED,key=len,reverse=True)):
        token=f"ZXQ{i:03d}QXZ"
        if value in text:
            text=text.replace(value,token); replacements[token]=value
    return text,replacements

def restore(text,replacements):
    for token,value in replacements.items():
        text=re.sub(re.escape(token),value,text,flags=re.I)
    return text

def request(value,target,depth=0):
    for attempt in range(4):
        try:
            result=GoogleTranslator(source="en",target=target).translate(value)
            if result:return result
        except Exception:time.sleep(1.5*(attempt+1))
    words=value.split()
    if len(words)>8 and depth<4:
        middle=len(words)//2
        return request(" ".join(words[:middle]),target,depth+1)+" "+request(" ".join(words[middle:]),target,depth+1)
    return value

def translate_values(values,target):
    output=[""]*len(values); batch=[]; indices=[]; size=0
    def flush():
        nonlocal batch,indices,size
        if not batch:return
        marker="\nZXSEPZX\n"; items=[]; maps=[]
        for value in batch:
            item,mapping=protect(value);items.append(item);maps.append(mapping)
        translated=request(marker.join(items),target)
        parts=re.split(r"\s*ZXSEPZX\s*",translated,flags=re.I)
        if len(parts)!=len(batch):parts=[request(item,target) for item in items]
        for idx,part,mapping in zip(indices,parts,maps):output[idx]=restore(part,mapping)
        batch=[];indices=[];size=0;time.sleep(.3)
    for idx,value in enumerate(values):
        if not value.strip() or re.fullmatch(r"[\d\W_]+",value,re.UNICODE):
            output[idx]=value;continue
        if size+len(value)+14>1800:flush()
        batch.append(value);indices.append(idx);size+=len(value)+14
    flush();return output

def collect_json(obj,items):
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key in JSON_KEYS and isinstance(value,str) and not value.startswith("http"):items.append((obj,key,value))
            else:collect_json(value,items)
    elif isinstance(obj,list):
        for value in obj:collect_json(value,items)

def translate_page(code,target):
    soup=BeautifulSoup(SOURCE.read_text(encoding="utf-8"),"html.parser")
    soup.html["lang"]=code;soup.html["dir"]="rtl" if code=="ar" else "ltr"
    canonical=page_url(code)
    soup.title.string=TITLES[code]
    for meta in soup.find_all("meta"):
        key=meta.get("property") or meta.get("name")
        if key in {"og:title","twitter:title"}:meta["content"]=TITLES[code]
    soup.find("link",rel="canonical")["href"]=canonical
    for tag in soup.find_all("meta"):
        key=tag.get("property") or tag.get("name")
        if key=="og:url":tag["content"]=canonical
        if key=="og:locale":tag["content"]=code.replace("-","_")
    nodes=[]
    for node in soup.find_all(string=True):
        if isinstance(node,NavigableString) and not isinstance(node,Doctype) and node.parent.name not in {"script","style"} and str(node).strip():nodes.append(node)
    attrs=[]
    for tag in soup.find_all(True):
        for attr in ("alt","title","aria-label"):
            if tag.has_attr(attr) and str(tag[attr]).strip():attrs.append((tag,attr,str(tag[attr])))
    for tag in soup.find_all("meta"):
        key=tag.get("name") or tag.get("property")
        if key in {"description","og:title","og:description","twitter:title","twitter:description"}:
            attrs.append((tag,"content",tag.get("content","")))
    scripts=[];json_items=[]
    for tag in soup.find_all("script",attrs={"type":"application/ld+json"}):
        try:data=json.loads(tag.string or tag.get_text())
        except Exception:continue
        current=[];collect_json(data,current);json_items.extend(current);scripts.append((tag,data))
    translated=translate_values([str(n) for n in nodes]+[x[2] for x in attrs]+[x[2] for x in json_items],target);cursor=0
    for node in nodes:
        original=str(node);lead=original[:len(original)-len(original.lstrip())];trail=original[len(original.rstrip()):]
        node.replace_with(lead+translated[cursor].strip()+trail);cursor+=1
    for tag,attr,_ in attrs:tag[attr]=translated[cursor].strip();cursor+=1
    for parent,key,_ in json_items:parent[key]=translated[cursor].strip();cursor+=1
    for tag,data in scripts:
        def localize(obj):
            if isinstance(obj,dict):
                for k,v in obj.items():
                    if k=="inLanguage":obj[k]=code
                    elif isinstance(v,str) and v.startswith(BASE+"/urban-art-city/barcelona/spain/"):
                        obj[k]=v.replace(BASE+"/urban-art-city/barcelona/spain/",canonical)
                    else:localize(v)
            elif isinstance(obj,list):
                for v in obj:localize(v)
        localize(data);tag.string=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    for a in soup.find_all("a",href=True):
        if a["href"].startswith("/") and not a.get("hreflang"):a["hreflang"]="en"
    out=Path(code)/LANGUAGES[code][1]/"index.html";out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(str(soup),encoding="utf-8")
    visible=soup.get_text(" ",strip=True)
    if len(visible)<3000:raise RuntimeError(f"{code}: incomplete translation")
    print(code,out,len(visible))

def update_sitemap():
    path=Path("sitemap.xml");text=path.read_text(encoding="utf-8");entries=[]
    for code in LANGUAGES:
        current=page_url(code)
        if f"<loc>{current}</loc>" not in text:
            entries.append(f'<url><loc>{current}</loc><lastmod>2026-09-03</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>')
    if entries:path.write_text(text.replace("</urlset>","".join(entries)+"</urlset>"),encoding="utf-8")

def main():
    for code,(target,_) in LANGUAGES.items():translate_page(code,target)
    update_sitemap()

if __name__=="__main__":main()
