import os, json, html
BASE="/vidivas-novy"
FINAL="https://vidivas.cz"
TEL="+420739878732"; TELH="739 878 732"; MAIL="info@vidivas.cz"
MISE="Pomáháme řemeslníkům, aby jejich online profil byl moderní a funkční pro dnešní dobu."
ENDPOINT="https://vidivas.cz/api/poptavka"
pages=[]  # (path,title)

def e(s): return html.escape(s,quote=True)

def layout(path,title,desc,body,crumbs,extra_ld=None,h1_hero=False):
    url=FINAL+path
    ld=[{"@context":"https://schema.org","@type":"ProfessionalService","@id":FINAL+"/#firma","name":"vidivas.cz – David Kočí","url":FINAL+"/","telephone":TEL,"email":MAIL,"founder":{"@type":"Person","name":"David Kočí"},"identifier":{"@type":"PropertyValue","name":"IČO","value":"04781872"},"areaServed":{"@type":"Country","name":"Česká republika"},"description":"Weby pro řemeslníky: web, texty a návod pro Google profil a Firmy.cz, hosting a správa."}]
    bl=[{"@type":"ListItem","position":i+1,"name":n,"item":FINAL+p} for i,(n,p) in enumerate(crumbs)]
    ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":bl})
    if extra_ld: ld+=extra_ld
    ldh="".join('<script type="application/ld+json">%s</script>'%json.dumps(x,ensure_ascii=False) for x in ld)
    nav=f'''<header class="top"><div class="wrap bar"><a class="logo" href="{BASE}/">vidivas<span>.cz</span></a>
<nav aria-label="Hlavní"><a href="{BASE}/cenik/">Ceník</a><a href="{BASE}/web-pro-elektrikare/">Obory</a><a href="{BASE}/google-profil-a-firmy-cz/">Návody</a><a href="{BASE}/kraje/">Kraje</a></nav>
<a class="tel" href="tel:{TEL}">{TELH}</a><a class="btn sm" href="{BASE}/#poptavka">Nezávazná poptávka</a></div></header>'''
    foot=f'''<footer><div class="wrap"><p class="mise">{MISE}</p>
<div class="fcols"><div><strong>vidivas.cz</strong><br>David Kočí · IČO 04781872<br>Nejsem plátce DPH, ceny jsou konečné.<br><a href="tel:{TEL}">{TELH}</a><br><a href="mailto:{MAIL}">{MAIL}</a></div>
<div><strong>Stránky</strong><br><a href="{BASE}/cenik/">Ceník</a><br><a href="{BASE}/podminky/">Podmínky</a><br><a href="{BASE}/google-profil-a-firmy-cz/">Google profil a Firmy.cz</a><br><a href="{BASE}/kraje/">Působíme ve všech krajích</a></div>
<div><strong>Pro obory</strong><br><a href="{BASE}/web-pro-elektrikare/">Elektrikáři</a><br><a href="{BASE}/web-pro-instalatere/">Instalatéři</a><br><a href="{BASE}/web-pro-tesare/">Tesaři</a></div></div>
<p class="small">Předváděcí verze, není určena k indexaci. © 2026 David Kočí</p></div></footer>
<div class="sticky"><a class="btn" href="tel:{TEL}">Zavolat</a><a class="btn alt" href="{BASE}/#poptavka">Poptat</a></div>'''
    out=f'''<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="cs_CZ"><meta property="og:site_name" content="vidivas.cz"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#0f2742"><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{BASE}/style.css">{ldh}</head><body>
<a class="skip" href="#obsah">Přeskočit na obsah</a>{nav}<main id="obsah">{body}</main>{foot}
<script src="{BASE}/app.js" defer></script></body></html>'''
    fp=("."+path+"index.html") if path!="/" else "./index.html"
    os.makedirs(os.path.dirname(fp) or ".",exist_ok=True)
    open(fp,"w",encoding="utf-8").write(out)
    pages.append((path,title))

def crumbs_bar(items):
    return '<nav class="crumbs wrap" aria-label="Drobečková navigace">'+" › ".join(f'<a href="{BASE}{p}">{n}</a>' if i<len(items)-1 else f'<span>{n}</span>' for i,(n,p) in enumerate(items))+'</nav>'

def form():
    return f'''<section class="sec dark" id="poptavka"><div class="wrap two"><div class="reveal"><h2>Nezávazná poptávka</h2>
<p>Napište, co děláte a kde působíte. Ozvu se vám, ukážeme si, co by pomohlo, a ukázku vašeho webu dostanete předem. Odpovídám obvykle do 24 hodin.</p>
<p class="big"><a href="tel:{TEL}">{TELH}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
<form class="reveal" id="poptavka-form" name="poptavka" method="POST" action="{ENDPOINT}">
<div class="hp" aria-hidden="true"><label>Nevyplňujte <input name="firma-web" tabindex="-1" autocomplete="off"></label></div>
<label>Jméno<input name="jmeno" type="text" required autocomplete="name"></label>
<label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label>
<label>E-mail (nepovinné)<input name="email" type="email" autocomplete="email"></label>
<label>Co děláte a kde působíte?<textarea name="zprava" rows="4" required></textarea></label>
<label class="chk"><input type="checkbox" name="souhlas" required> Beru na vědomí zásady zpracování osobních údajů (David Kočí, správce údajů; použiji je jen k odpovědi na poptávku).</label>
<button class="btn" type="submit">Odeslat poptávku</button>
<p class="msg" role="status" aria-live="polite"></p></form></div></section>'''

def faq_html(items):
    return "".join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
def faq_ld(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

FAQ=[("Kolik to stojí a co je v ceně?","Plná varianta stojí 2 500 Kč jednorázově a 690 Kč měsíčně. V ceně je web, hosting, správa, drobné změny, texty a kategorie pro Google a Firmy.cz s návodem a poradenství k profilům. Varianta jen web stojí 2 500 Kč jednorázově a 490 Kč měsíčně. Ceny jsou konečné, nejsem plátce DPH."),
("Proč platit měsíčně?","Z měsíční platby se hradí hosting, správa a drobné změny webu. Web vám nepředávám jako hotový kus, který pak nikdo nespravuje, ale pronajímám a starám se o něj."),
("Komu patří web a doména, když skončím?","Doména patří vám a zůstane vám i po odchodu. Web a hosting jsou moje a pronajímám vám je. Když přestanete platit, pošlu upozornění a po lhůtě web vypnu."),
("Můžu skončit kdykoli?","Ano. Zaplacený měsíc dojede a dál platit nemusíte. Je ale potřeba počítat s tím, že bez platby web přestane být online."),
("Musím mít fotky a texty?","Ne. Texty připravím z toho, co mi o práci řeknete. Fotky z vaší práce se hodí, ale začít se dá i bez nich."),
("Co je SEO a AEO lidsky?","SEO znamená, že vás najdou ve vyhledávání na Googlu a Seznamu. AEO znamená, že web je napsaný tak, aby z něj uměli správně odpovídat i AI asistenti, když se na vás někdo zeptá."),
("Založíte mi Google profil za mě?","Profil zakládá a ověřuje majitel firmy, tak to Google vyžaduje. Já připravím texty, kategorie a návod krok za krokem a poradím, když si nebudete vědět rady."),
("Jak rychle bude web hotový?","Ukázku vašeho webu dostanete předem a bez závazku. Konkrétní termín dodání domluvíme podle toho, co je potřeba, ještě před platbou."),
("Co když přestanete fungovat vy?","Tohle zatím nemám pevně sepsané. Podmínky předání proto doplním, než se služba pro další klienty spustí.")]

def hero(h1,sub,extra=""):
    return f'''<section class="hero"><div class="wrap"><p class="eyebrow">Web pro řemeslníky</p><h1>{h1}</h1><p class="lead">{sub}</p>
<div class="cta"><a class="btn" href="tel:{TEL}">Zavolat {TELH}</a><a class="btn alt" href="{BASE}/#poptavka">Chci ukázku webu</a></div>{extra}
<ul class="pills"><li>Ukázka předem</li><li>Výpověď kdykoli</li><li>Doména zůstává vám</li></ul></div></section>'''

CO=["Web s nastavením SEO a AEO","Texty a kategorie pro Google a Firmy.cz s návodem","Formulář","Hosting a správa"]
def codostanete():
    li="".join(f'<li class="reveal"><span class="ck">✓</span><strong>{x}</strong></li>' for x in CO)
    return f'<ul class="gets">{li}</ul><p class="note reveal">Profily si zakládáte a ověřujete sami, my vás krok za krokem provedeme.</p>'
def ceny():
    return f'''<div class="plans"><article class="plan feat reveal"><span class="tag">Doporučená</span><h3>Plná</h3><p class="price">2 500 Kč <small>jednorázově</small></p><p class="price">+ 690 Kč <small>měsíčně</small></p>
<ul><li>Web a hosting</li><li>Správa a drobné změny</li><li>Texty a kategorie pro Google a Firmy.cz s návodem</li><li>Poradenství k profilům</li></ul><a class="btn" href="{BASE}/#poptavka">Chci plnou variantu</a></article>
<article class="plan reveal"><h3>Jen web</h3><p class="price">2 500 Kč <small>jednorázově</small></p><p class="price">+ 490 Kč <small>měsíčně</small></p>
<ul><li>Web a hosting</li><li>Základní správa</li><li>Bez poradenství k profilům</li></ul><a class="btn alt dk" href="{BASE}/#poptavka">Chci jen web</a></article></div>
<p class="note reveal">Ceny jsou konečné, nejsem plátce DPH. 690 Kč měsíčně je zhruba 23 Kč denně. Dvě kola úprav v ceně.</p>'''
def podminky():
    return '''<ul class="terms"><li class="reveal"><strong>Vypovědět můžete kdykoli.</strong> Zaplacený měsíc dojede, dál platit nemusíte.</li>
<li class="reveal"><strong>Doména je vaše</strong> a zůstane vám i po odchodu.</li>
<li class="reveal"><strong>Web a hosting jsou naše</strong> a jen vám je pronajímáme. Když přestanete platit, pošleme upozornění a po lhůtě web vypneme.</li></ul>'''

# ---- HOME
home=f'''<section class="hero big"><div class="wrap"><p class="eyebrow">Pomáháme řemeslníkům</p><h1>Aby vás zákazníci našli a zavolali.</h1>
<p class="lead">{MISE} Web, Google a Firmy.cz v jednom.</p>
<div class="cta"><a class="btn" href="tel:{TEL}">Zavolat {TELH}</a><a class="btn alt" href="#poptavka">Chci ukázku webu</a></div>
<ul class="pills"><li>Ukázka předem</li><li>Výpověď kdykoli</li><li>Doména zůstává vám</li></ul></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Zákazník dnes nejdřív hledá. Pak teprve volá.</h2>
<p class="reveal">Hledá na Googlu, na Seznamu, v mapách a čím dál častěji se ptá AI asistentů. Když tam nejste, nebo máte zastaralý profil, může zavolat někomu jinému. Platí to i u řemeslníka, který má práce dost z doporučení: lidé si ho před zavoláním často stejně najdou.</p></div></section>
<section class="sec alt"><div class="wrap"><h2 class="reveal">Co dostanete</h2>{codostanete()}</div></section>
<section class="sec"><div class="wrap"><h2 class="reveal">Jak to funguje</h2><ol class="steps">
<li class="reveal"><b>1</b>Ukázka vašeho webu zdarma, bez závazku</li><li class="reveal"><b>2</b>Schválíte, zaplatíte vstupní cenu</li><li class="reveal"><b>3</b>Nasadíme web na vaši doménu</li><li class="reveal"><b>4</b>Dostanete texty a návod pro Google a Firmy.cz</li><li class="reveal"><b>5</b>Měsíčně se o web staráme</li></ol></div></section>
<section class="sec alt"><div class="wrap"><h2 class="reveal">Ceník</h2>{ceny()}<p class="center reveal"><a href="{BASE}/cenik/">Podrobný ceník</a></p></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Férové podmínky</h2>{podminky()}<p class="center reveal"><a href="{BASE}/podminky/">Celé podmínky</a></p></div></section>
<section class="sec alt"><div class="wrap"><h2 class="reveal">Web podle vašeho oboru</h2><p class="reveal">Ukázku postavím na míru vaší firmě, zdarma. Pro začátek se podívejte, jak web pro váš obor řešíme:</p>
<div class="cards"><a class="card reveal" href="{BASE}/web-pro-elektrikare/"><h3>Elektrikáři</h3><p>Revize, instalace, havárie.</p></a><a class="card reveal" href="{BASE}/web-pro-instalatere/"><h3>Instalatéři</h3><p>Voda, topení, odpady.</p></a><a class="card reveal" href="{BASE}/web-pro-tesare/"><h3>Tesaři</h3><p>Krovy, pergoly, dřevostavby.</p></a></div></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Kdo za tím stojí</h2><p class="reveal">Jmenuji se David Kočí a weby dělám sám. Píšete a voláte přímo mně, ne agentuře. IČO 04781872. Odpovídám obvykle do 24 hodin.</p></div></section>
<section class="sec alt"><div class="wrap narrow"><h2 class="reveal">Časté dotazy</h2>{faq_html(FAQ)}</div></section>
{form()}'''
svc={"@context":"https://schema.org","@type":"Service","name":"Online viditelnost pro řemeslníky","provider":{"@id":FINAL+"/#firma"},"areaServed":{"@type":"Country","name":"Česká republika"},"description":"Web s nastavením SEO a AEO, texty a kategorie pro Google a Firmy.cz s návodem, formulář, hosting a správa.","offers":[{"@type":"Offer","name":"Plná","priceCurrency":"CZK","price":"2500","description":"2 500 Kč jednorázově + 690 Kč měsíčně"},{"@type":"Offer","name":"Jen web","priceCurrency":"CZK","price":"2500","description":"2 500 Kč jednorázově + 490 Kč měsíčně"}]}
layout("/","Web pro řemeslníky: 2 500 Kč + měsíčně, Google a Firmy.cz | vidivas.cz","Pomáháme řemeslníkům mít moderní a funkční online profil. Web, texty a návod pro Google a Firmy.cz. Ukázka předem, výpověď kdykoli, doména zůstává vám.",home,[("Úvod","/")],[svc,faq_ld(FAQ)])

# ---- CENIK
b=f'''{crumbs_bar([("Úvod","/"),("Ceník","/cenik/")])}<section class="hero sm"><div class="wrap"><h1>Ceník webu pro řemeslníka</h1><p class="lead">Dvě varianty, obě se stejnou vstupní cenou 2 500 Kč. Ceny jsou konečné, nejsem plátce DPH.</p></div></section>
<section class="sec"><div class="wrap">{ceny()}</div></section>
<section class="sec alt"><div class="wrap narrow"><h2 class="reveal">Rozdíl mezi variantami</h2><div class="tablewrap reveal"><table><thead><tr><th></th><th>Plná</th><th>Jen web</th></tr></thead><tbody>
<tr><td>Jednorázově</td><td>2 500 Kč</td><td>2 500 Kč</td></tr><tr><td>Měsíčně</td><td>690 Kč</td><td>490 Kč</td></tr>
<tr><td>Web a hosting</td><td>ano</td><td>ano</td></tr><tr><td>Správa</td><td>ano, včetně drobných změn</td><td>základní</td></tr>
<tr><td>Texty a návod pro Google a Firmy.cz</td><td>ano</td><td>ne</td></tr><tr><td>Poradenství k profilům</td><td>ano</td><td>ne</td></tr></tbody></table></div></div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Podmínky</h2>{podminky()}</div></section>
<section class="sec alt"><div class="wrap narrow"><h2 class="reveal">Kolik stojí web pro řemeslníka u nás?</h2><p class="reveal">Web pro řemeslníka u nás stojí 2 500 Kč jednorázově a pak 690 Kč měsíčně (plná varianta) nebo 490 Kč měsíčně (jen web). V ceně je hosting a správa. Doména zůstává vám.</p></div></section>{form()}'''
layout("/cenik/","Ceník webu pro řemeslníky od 2 500 Kč | vidivas.cz","Ceník: plná varianta 2 500 Kč + 690 Kč měsíčně, jen web 2 500 Kč + 490 Kč měsíčně. Ceny konečné, nejsem plátce DPH.",b,[("Úvod","/"),("Ceník","/cenik/")],[svc])

# ---- PODMINKY
b=f'''{crumbs_bar([("Úvod","/"),("Podmínky","/podminky/")])}<section class="hero sm"><div class="wrap"><h1>Podmínky služby</h1><p class="lead">Napsané lidsky. Právně závazné znění smlouvy doplním před spuštěním služby.</p></div></section>
<section class="sec"><div class="wrap narrow">{podminky()}<h2 class="reveal">Co platí navíc</h2><ul class="terms"><li class="reveal">Ukázku vašeho webu dostanete předem a bez závazku, platíte až po schválení.</li><li class="reveal">V ceně jsou dvě kola úprav.</li><li class="reveal">Google profil a Firmy.cz zakládá a ověřuje majitel firmy. My připravíme texty a kategorie a provedeme vás.</li><li class="reveal">Ceny jsou konečné, nejsem plátce DPH.</li></ul></div></section>{form()}'''
layout("/podminky/","Podmínky služby | vidivas.cz","Výpověď kdykoli, doména zůstává vám, web a hosting jsou pronajaté. Podmínky služby Online viditelnost.",b,[("Úvod","/"),("Podmínky","/podminky/")])

# ---- OBORY
obory={"elektrikare":("Elektrikáři","elektrikáře","elektrikář","Elektro",
 ["Elektroinstalace","Revize elektro","Opravy a havárie","Rozvaděče","Hromosvody"],
 "Lidé hledají elektrikáře ve chvíli, kdy něco přestalo fungovat, nebo když potřebují revizi. V obou případech chtějí rychle vidět, co děláte, kde a jak vám zavolat.",
 ["Elektroinstalace v domech a bytech","Revize elektro","Opravy a řešení poruch","Rozvaděče a jističe"],"Elektrikář","Elektrikář (elektroinstalace)"),
"instalatere":("Instalatéři","instalatéra","instalatér","Instalace",
 ["Vodoinstalace","Topení","Odpady","Rekonstrukce koupelen","Havárie"],
 "Instalatéra lidé shánějí často narychlo, třeba při úniku vody. Na webu proto musí být hned vidět telefon, oblast působení a to, co opravdu děláte.",
 ["Vodoinstalace a odpady","Topení a otopné systémy","Rekonstrukce koupelen","Opravy a havárie"],"Instalatér","Instalatér"),
"tesare":("Tesaři","tesaře","tesař","Tesařství",
 ["Krovy a střechy","Pergoly a přístřešky","Dřevostavby","Terasy","Opravy dřevěných konstrukcí"],
 "U tesařiny se vybírá podle toho, co už jste postavili. Web proto stojí na popisu služeb, oblasti působení a ukázkách práce, které máte.",
 ["Krovy a střechy","Pergoly a přístřešky","Dřevostavby a terasy","Opravy dřevěných konstrukcí"],"Tesař","Tesař")}
for k,(nm,gen,sg,_,kw,intro,svcs,occ,occname) in obory.items():
    p=f"/web-pro-{k}/"
    fq=[(f"Potřebuje {sg} vlastní web?",f"Web není povinný, ale zákazník si vás před zavoláním často vyhledá. Když najde jen starý nebo žádný profil, může zavolat někomu jinému. Web s Google profilem a Firmy.cz zvyšuje šanci, že vás najdou a zavolají."),
        (f"Kolik stojí web pro {gen}?","Plná varianta stojí 2 500 Kč jednorázově a 690 Kč měsíčně, varianta jen web 2 500 Kč a 490 Kč měsíčně. Ceny jsou konečné."),
        ("Musím mít na web vlastní fotky?","Nemusíte. Pokud fotky z vaší práce máte, použijeme je. Nic nevymýšlíme a nepoužíváme cizí ukázky jako vaše.")]
    sl="".join(f"<li class='reveal'>{s}</li>" for s in svcs)
    kwh="".join(f"<li>{x}</li>" for x in kw)
    b=f'''{crumbs_bar([("Úvod","/"),(f"Web pro {gen}",p)])}{hero(f"Web pro {gen}, po kterém zazvoní telefon",intro)}
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Co by na webu {sg}e nemělo chybět</h2><ul class="terms">{sl}</ul>
<p class="reveal">Každá služba má na webu svůj krátký popis, aby ji uměl najít zákazník i vyhledávač. Číslo a oblast působení jsou vidět hned.</p></div></section>
<section class="sec alt"><div class="wrap"><h2 class="reveal">Co dostanete</h2>{codostanete()}</div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Na co lidé hledají {gen}</h2><p class="reveal">Typické hledání je služba a místo, například „{sg} + vaše město“. Proto web i profily píšeme s vašimi službami a oblastí, kde opravdu pracujete.</p><ul class="pills dk">{kwh}</ul></div></section>
<section class="sec alt"><div class="wrap">{ceny()}</div></section>
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Časté dotazy</h2>{faq_html(fq)}</div></section>
<section class="sec alt"><div class="wrap narrow"><p class="reveal">Vaši ukázku postavíme na míru vaší firmě, zdarma. Další obory: <a href="{BASE}/web-pro-elektrikare/">elektrikáři</a>, <a href="{BASE}/web-pro-instalatere/">instalatéři</a>, <a href="{BASE}/web-pro-tesare/">tesaři</a>. Vaše město nebo kraj najdete mezi <a href="{BASE}/kraje/">kraji</a>.</p></div></section>{form()}'''
    layout(p,f"Web pro {gen} od 2 500 Kč + Google a Firmy.cz | vidivas.cz",f"Web pro {gen}: služby, kontakt, texty a návod pro Google a Firmy.cz. 2 500 Kč + 690 Kč měsíčně. Ukázka předem, výpověď kdykoli.",b,[("Úvod","/"),(f"Web pro {gen}",p)],[svc,faq_ld(fq)])

# ---- NAVODY
def navod(path,title,h1,desc,steps,tips,name):
    s="".join(f"<li class='reveal'><b>{i+1}</b>{t}</li>" for i,t in enumerate(steps))
    t="".join(f"<li class='reveal'>{x}</li>" for x in tips)
    ld={"@context":"https://schema.org","@type":"HowTo","name":h1,"step":[{"@type":"HowToStep","position":i+1,"text":re_strip(t)} for i,t in enumerate(steps)]}
    b=f'''{crumbs_bar([("Úvod","/"),(name,path)])}<section class="hero sm"><div class="wrap"><h1>{h1}</h1><p class="lead">{desc}</p></div></section>
<section class="sec"><div class="wrap narrow"><p class="reveal">Profil zakládá a ověřuje majitel firmy, protože to vyžaduje služba sama. Postup se může časem mírně změnit, proto se řiďte tím, co ukazuje obrazovka.</p><ol class="steps">{s}</ol>
<h2 class="reveal">Na co si dát pozor</h2><ul class="terms">{t}</ul>
<p class="reveal">V balíčku „Plná“ pro vás připravím texty a kategorie a provedu vás tímto postupem. <a href="{BASE}/cenik/">Ceník</a></p></div></section>{form()}'''
    layout(path,title,desc,b,[("Úvod","/"),(name,path)],[ld])
import re
def re_strip(s): return re.sub(r"<[^>]+>","",s)
navod("/google-profil-a-firmy-cz/","Google profil a Firmy.cz pro řemeslníky: návod | vidivas.cz","Google profil firmy a Firmy.cz: návod krok za krokem","Dva profily, které zákazníkům ukážou, že existujete, kde působíte a jak vám zavolat. Obecný návod, jak na to.",
 ["<strong>Google profil firmy:</strong> přihlaste se do Google účtu a v Google Mapách nebo ve vyhledávání zvolte přidání firmy.","Zadejte název firmy tak, jak ho používáte v běžném provozu, a vyberte hlavní kategorii (např. elektrikář, instalatér).","U firmy bez provozovny, kam zákazníci nechodí, zvolte oblast působení místo veřejné adresy.","Doplňte telefon, adresu webu, otevírací dobu a krátký popis služeb.","Dokončete ověření, které Google nabídne (např. kódem, telefonem nebo videem). Zvolený způsob určuje Google.","<strong>Firmy.cz:</strong> na Firmy.cz si založte účet a zapište firmu zdarma. Vyplňte název, kategorii, kontakty a popis.","Ověřte údaje podle pokynů Firmy.cz a doplňte web a služby."],
 ["Název, telefon a adresa webu mají být všude stejné.","Nepište do názvu firmy dodatečná klíčová slova, Google to může zamítnout.","Uvádějte jen služby, které opravdu děláte, a fotky jen vlastní.","Nikomu nesdělujte ověřovací kódy mimo formulář Googlu nebo Firmy.cz."],"Google profil a Firmy.cz")
# single-purpose second guide pages
navod("/navod-google-profil/","Návod: Google profil firmy pro řemeslníka | vidivas.cz","Jak založit Google profil firmy","Krok za krokem, bez technického žargonu.",
 ["Přihlaste se do Google účtu.","V Google Mapách vyberte přidání firmy.","Zadejte název a hlavní kategorii.","Zvolte, zda zákazníky přijímáte na adrese, nebo působíte v oblasti.","Doplňte telefon, web a popis služeb.","Dokončete ověření podle toho, co Google nabídne."],
 ["Údaje držte shodné s webem.","Fotky používejte vlastní.","Ověřovací kódy patří jen do Googlu."],"Návod: Google profil")
navod("/navod-firmy-cz/","Návod: zápis na Firmy.cz pro řemeslníka | vidivas.cz","Jak se zapsat na Firmy.cz","Základní zápis na Firmy.cz krok za krokem.",
 ["Založte si účet na Firmy.cz.","Zvolte přidání firmy a vyplňte název a IČO.","Vyberte kategorii a oblast působení.","Doplňte telefon, e-mail, web a popis služeb.","Ověřte údaje podle pokynů Firmy.cz."],
 ["Používejte stejné údaje jako na webu a v Google profilu.","Popis pište lidsky a konkrétně.","Neuvádějte služby, které neděláte."],"Návod: Firmy.cz")

# ---- KRAJE
K=[
("praha","Praha","Hlavní město Praha","Praha",["Praha 1–22","Praha-východ a západ (sousední kraj)"],
 "V Praze je řemeslníků hodně a zákazníci si vybírají hlavně podle městské části. Obecný název „elektrikář Praha“ je velmi obsazený, proto má smysl psát konkrétní čtvrti a typ zakázek, například byty, panelové domy nebo kanceláře.",
 "Hledání bývá rozdělené na městské části (např. Praha 4, Praha 9). Google mapy tu rozhodují víc než u menších měst.",
 "Do profilu uveďte, které městské části opravdu obsloužíte, a nepřehánějte oblast působení."),
("stredocesky","Středočeský kraj","Středočeský kraj","Praha",["Kladno","Mladá Boleslav","Kolín","Kutná Hora","Beroun","Mělník","Příbram","Nymburk","Benešov","Rakovník"],
 "Středočeský kraj obklopuje Prahu. Řemeslník tu často pracuje jak ve městech, tak v obcích a rodinných domech kolem nich, a zákazníci hledají podle nejbližšího města.",
 "Lidé zadávají název okresního města nebo menší obce. Dojezd se tu pohybuje mezi městem a okolními vesnicemi, takže je vhodné vypsat obce, kam opravdu jezdíte.",
 "Vytvořte popis oblasti podle okresů (např. Kladensko, Mladoboleslavsko) a doplňte skutečné obce."),
("jihocesky","Jihočeský kraj","Jihočeský kraj","České Budějovice",["České Budějovice","Tábor","Písek","Strakonice","Jindřichův Hradec","Český Krumlov","Prachatice"],
 "V Jihočeském kraji je mnoho menších měst a venkovských obcí, a tak se řemeslníci často starají o rozlehlou oblast. Zákazníci hledají podle nejbližšího města a regionu.",
 "Časté je hledání podle okresu nebo menšího města. Mapy a Firmy.cz tu pomáhají odlišit řemeslníky z jiných částí kraje.",
 "V oblasti působení uveďte konkrétní okresy a vyhněte se vágnímu „celé jižní Čechy“, když tam reálně nejezdíte."),
("plzensky","Plzeňský kraj","Plzeňský kraj","Plzeň",["Plzeň","Klatovy","Domažlice","Rokycany","Tachov","Sušice"],
 "Plzeňský kraj tvoří velká Plzeň s okolím a menší města v dalších okresech. Pro řemeslníka je důležité rozlišit zakázky v Plzni a ve městech na okrajích kraje.",
 "Zákazníci hledají podle Plzně nebo podle okresního města. Vyplatí se mít stránku nebo popis služeb, který jmenuje obě skupiny míst.",
 "Napište, zda pracujete jen v Plzni a okolí, nebo jezdíte i do okresů jako Domažlice, Klatovy či Tachov."),
("karlovarsky","Karlovarský kraj","Karlovarský kraj","Karlovy Vary",["Karlovy Vary","Cheb","Sokolov","Mariánské Lázně","Ostrov","Aš"],
 "Karlovarský kraj je menší kraj s lázeňskými městy a pohraniční polohou. Řemeslníci tu mohou obsluhovat domácnosti i firmy, ubytování nebo penziony.",
 "Hledání je často vázané na konkrétní město (Karlovy Vary, Cheb, Sokolov). Menší konkurence ve vyhledávání může znamenat, že se dá dostat dopředu i s krátkým, ale kvalitním webem.",
 "Pokud obsluhujete penziony nebo provozovny, zmiňte to v popisu služeb. Jen pokud to opravdu děláte."),
("ustecky","Ústecký kraj","Ústecký kraj","Ústí nad Labem",["Ústí nad Labem","Most","Teplice","Chomutov","Děčín","Litoměřice","Louny","Žatec"],
 "Ústecký kraj je hustě osídlený, s mnoha většími městy vedle sebe. Řemeslník může v rámci jednoho dne obsloužit několik měst.",
 "Lidé hledají podle konkrétního města (Teplice, Most, Chomutov) a rozhoduje blízkost. Dobře funguje výčet měst, kam dojíždíte.",
 "Popište dojezd pro každé větší město zvlášť a nespoléhejte na jediný obecný název kraje."),
("liberecky","Liberecký kraj","Liberecký kraj","Liberec",["Liberec","Jablonec nad Nisou","Česká Lípa","Semily","Turnov","Jilemnice"],
 "V Libereckém kraji jsou vedle měst i horské oblasti s rekreačními objekty. Řemeslníci tu mohou řešit domy, chalupy i chaty.",
 "Hledání se dělí na Liberecko, Jablonecko, Českolipsko a Podkrkonoší. Zákazníci často zadávají název menšího města nebo oblasti.",
 "Pokud děláte i chaty a chalupy, napište to samostatně a uveďte oblasti, kam jezdíte."),
("kralovehradecky","Královéhradecký kraj","Královéhradecký kraj","Hradec Králové",["Hradec Králové","Trutnov","Náchod","Jičín","Rychnov nad Kněžnou","Dvůr Králové nad Labem"],
 "Královéhradecký kraj spojuje větší Hradec Králové s menšími městy a podhorskými oblastmi. Zakázky bývají v rodinných domech i v rekreačních objektech.",
 "Zákazníci hledají podle Hradce Králové nebo podle okresu (Trutnov, Náchod, Jičín). Vyplatí se zmínit, které okresy skutečně pokrýváte.",
 "Uveďte hlavní město působení a pak seznam okolních měst. Jen těch, kam opravdu dojíždíte."),
("pardubicky","Pardubický kraj","Pardubický kraj","Pardubice",["Pardubice","Chrudim","Svitavy","Ústí nad Orlicí","Přelouč","Litomyšl","Žamberk"],
 "Pardubický kraj má několik středně velkých měst a rozptýlené osídlení v okolí. Řemeslníci často působí napříč okresy.",
 "Lidé zadávají město nebo okres (Chrudim, Svitavy, Ústí nad Orlicí). Mapy a Firmy.cz pomáhají v menších městech, kde je ve vyhledávání méně konkurence.",
 "V popisu uveďte všechny okresy, kde pracujete, a doplňte konkrétní příklady zakázek, které opravdu máte."),
("vysocina","Kraj Vysočina","Kraj Vysočina","Jihlava",["Jihlava","Třebíč","Žďár nad Sázavou","Havlíčkův Brod","Pelhřimov","Velké Meziříčí"],
 "Na Vysočině je hodně menších měst a malých obcí, kde se často spoléhá na doporučení. I tam si ale lidé řemeslníka před zavoláním vyhledají.",
 "Hledání se opírá o okresní města (Jihlava, Třebíč, Žďár, Havlíčkův Brod, Pelhřimov). V malých obcích funguje, když je uvedeno nejbližší město.",
 "Uveďte nejbližší okresní město a rozsah dojezdu. Rozptýlené osídlení znamená větší vzdálenosti."),
("jihomoravsky","Jihomoravský kraj","Jihomoravský kraj","Brno",["Brno","Znojmo","Břeclav","Hodonín","Vyškov","Blansko","Mikulov"],
 "Jihomoravský kraj táhne velké Brno a kolem něj města i vinařské obce. Konkurence ve vyhledávání je největší v Brně, v okolí bývá menší.",
 "„Elektrikář Brno“ je silně obsazený dotaz. Prostor mají hledání podle městských částí a okolních měst (Blansko, Vyškov, Znojmo, Břeclav, Hodonín).",
 "Rozlište Brno a zbytek kraje, každé s vlastním popisem a příkladem služeb."),
("olomoucky","Olomoucký kraj","Olomoucký kraj","Olomouc",["Olomouc","Prostějov","Přerov","Šumperk","Jeseník","Hranice","Zábřeh"],
 "Olomoucký kraj spojuje Olomouc s Prostějovem, Přerovem a horskými oblastmi na severu (Šumperk, Jeseník). Dojezdové vzdálenosti se mezi nížinou a horami liší.",
 "Zákazníci hledají podle města (Olomouc, Prostějov, Přerov) nebo regionu (Jesenicko, Šumpersko).",
 "Pokud obsluhujete Jeseníky, zmiňte to zvlášť, protože tamní zákazníci hledají jinak než v okolí Olomouce."),
("zlinsky","Zlínský kraj","Zlínský kraj","Zlín",["Zlín","Kroměříž","Uherské Hradiště","Vsetín","Valašské Meziříčí","Rožnov pod Radhoštěm"],
 "Zlínský kraj tvoří Zlín s okolím, Slovácko a Valašsko. Zákazníci mezi těmito oblastmi rozlišují a berou je jako vlastní regiony.",
 "Typické je hledání podle města nebo regionu (Valašsko, Slovácko). Vhodné je psát místní názvy tak, jak je lidé používají.",
 "Uveďte místní názvy oblastí, kde pracujete, a nepište je, pokud tam nepracujete."),
("moravskoslezsky","Moravskoslezský kraj","Moravskoslezský kraj","Ostrava",["Ostrava","Opava","Frýdek-Místek","Karviná","Havířov","Nový Jičín","Třinec","Bruntál"],
 "Moravskoslezský kraj patří k nejlidnatějším a je v něm několik velkých měst těsně u sebe. Řemeslník proto často pracuje ve více městech současně.",
 "Dotazy míří na konkrétní města (Ostrava, Opava, Havířov, Karviná, Frýdek-Místek) a konkurence je v Ostravě vysoká. Zbytek kraje nabízí víc prostoru.",
 "Uveďte aspoň tři až čtyři města, kam skutečně dojíždíte, a pro Ostravu doplňte městské obvody."),
]
rows=""
for slug,nm,full,seat,towns,a,b2,c in K:
    p=f"/kraje/{slug}/"
    tw=", ".join(towns)
    fq=[(f"Dělá vidivas.cz weby i v kraji: {nm}?",f"Ano, pracuji online po celé České republice, tedy i pro řemeslníky v kraji {nm}. Domlouvá se telefonem nebo e-mailem."),
        (f"Kolik stojí web pro řemeslníka z kraje {nm}?","Plná varianta stojí 2 500 Kč jednorázově a 690 Kč měsíčně, jen web 2 500 Kč a 490 Kč měsíčně. Cena nezávisí na kraji.")]
    b=f'''{crumbs_bar([("Úvod","/"),("Kraje","/kraje/"),(nm,p)])}{hero(f"Web pro řemeslníky: {full}",a)}
<section class="sec"><div class="wrap narrow"><h2 class="reveal">Jak se tu hledá</h2><p class="reveal">{b2}</p>
<h2 class="reveal">Typická města a oblasti</h2><p class="reveal">{tw}.</p>
<h2 class="reveal">Naše rada pro řemeslníky z kraje</h2><p class="reveal">{c}</p></div></section>
<section class="sec alt"><div class="wrap"><h2 class="reveal">Co dostanete</h2>{codostanete()}</div></section>
<section class="sec"><div class="wrap">{ceny()}</div></section>
<section class="sec alt"><div class="wrap narrow"><h2 class="reveal">Časté dotazy</h2>{faq_html(fq)}<p class="reveal">Přehled <a href="{BASE}/kraje/">všech krajů</a>. Návody: <a href="{BASE}/navod-google-profil/">Google profil</a>, <a href="{BASE}/navod-firmy-cz/">Firmy.cz</a>.</p></div></section>{form()}'''
    layout(p,f"Web pro řemeslníky: {full} | vidivas.cz",f"Web pro řemeslníky z kraje {nm}: jak se tu hledá, typická města ({', '.join(towns[:3])}), ceny od 2 500 Kč. Online po celé ČR.",b,[("Úvod","/"),("Kraje","/kraje/"),(nm,p)],[svc,faq_ld(fq)])
    rows+=f'<a class="card reveal" href="{BASE}{p}"><h3>{nm}</h3><p>{", ".join(towns[:3])} a další</p></a>'
b=f'''{crumbs_bar([("Úvod","/"),("Kraje","/kraje/")])}<section class="hero sm"><div class="wrap"><h1>Weby pro řemeslníky ve všech krajích</h1><p class="lead">Pracuji online po celé České republice. Domlouváme se telefonem nebo e-mailem, vyberte svůj kraj.</p></div></section>
<section class="sec"><div class="wrap"><div class="cards">{rows}</div></div></section>{form()}'''
layout("/kraje/","Weby pro řemeslníky ve všech krajích ČR | vidivas.cz","Web, Google profil a Firmy.cz pro řemeslníky v každém kraji České republiky. Online, telefonem nebo e-mailem.",b,[("Úvod","/"),("Kraje","/kraje/")])

# ---- sitemap, robots, llms, 404
us="".join(f"<url><loc>{FINAL}{p}</loc></url>" for p,_ in pages)
open("sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{us}</urlset>')
open("robots.txt","w").write("User-agent: *\nDisallow: /\n\n# Předváděcí verze. Po schválení se při výměně za ostrý web zapne indexace a doplní Sitemap.\n")
open("llms.txt","w").write(f"# vidivas.cz\n> {MISE}\nWeb, texty a kategorie pro Google a Firmy.cz s návodem, formulář, hosting a správa. Plná: 2 500 Kč + 690 Kč měsíčně. Jen web: 2 500 Kč + 490 Kč měsíčně. Ceny konečné, nejsem plátce DPH.\nKontakt: {TELH}, {MAIL}\n")
open("404.html","w").write(f'<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Stránka nenalezena</title><body style="font-family:sans-serif;padding:2rem"><h1>Stránka nenalezena</h1><p><a href="{BASE}/">Zpět na úvod</a></p></body></html>')
open("favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0f2742"/><text x="16" y="23" font-size="20" font-family="sans-serif" font-weight="700" text-anchor="middle" fill="#ff8a1f">v</text></svg>')
open(".nojekyll","w").write("")
print(len(pages),"pages")
