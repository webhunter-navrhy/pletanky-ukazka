#!/usr/bin/env python3
"""Generuje index.html, kategorie.html, produkt.html ukázky Pletánky.cz (verze 3) z produkty.json.
Data produktů (názvy, ceny, dostupnost, fotky, složení) jsou převzatá z pletanky.cz 7. a 10. 10. 2026.
Verze 2 podle zpětné vazby klientky z 9. 10. 2026: jedno písmo, jeden nadpis na sekci, banner přes celou šířku,
ostré rohy a jemné linky, fotky u projektů, blog jako dlaždice, rozbalení info u produktů, recenze,
Verze 3 (10. 10. 2026, podle reakce klientky): světlá varianta se zlatými tlačítky, horní a spodní lišta bordó, logo vlevo a vyhledávání uprostřed,
kategorie nepravidelně (ostré linie), sekce „Krása podzimu“ (téma měsíce) + malý Odstín měsíce v banneru, recenze v jednom řádku, nová prohlášení. První verze je archivovaná ve v1/."""
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
P = json.loads((ROOT / "produkty.json").read_text())
e = html.escape


def kc(v):
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    s = s[:-3] if s.endswith(",00") else s
    return s.replace(" ", "&nbsp;") + "&nbsp;Kč"


# ---------- ikonky (tenké linky) ----------
ICON = {
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1.2-3.6 4-5.3 7.5-5.3s6.3 1.7 7.5 5.3"/>',
    "bag": '<path d="M5.5 8.5h13l-1 11.5h-11z"/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "filter": '<path d="M4 6h16M7 12h10M10 18h4"/>',
    "truck": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    "mail": '<rect x="3.5" y="6" width="17" height="12"/><path d="m4 7 8 6 8-6"/>',
    "gift": '<rect x="4" y="9" width="16" height="11"/><path d="M4 13h16M12 9v11M12 9c-1.5-3-5-3.5-5-1.2C7 9 9.5 9 12 9zm0 0c1.5-3 5-3.5 5-1.2C17 9 14.5 9 12 9z"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "star": '<path d="m12 4 2.4 5 5.4.6-4 3.7 1.1 5.3L12 16l-4.9 2.6 1.1-5.3-4-3.7 5.4-.6z"/>',
    "ig": '<rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17" cy="7" r=".6"/>',
    "fb": '<path d="M14 8h2.5V4.5H14A3.5 3.5 0 0 0 10.5 8v2.5H8V14h2.5v6H14v-6h2.5l.5-3.5h-3V8.5c0-.3.2-.5.5-.5z"/>',
    "minus": '<path d="M6 12h12"/>',
    "plus": '<path d="M12 6v12M6 12h12"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8v.4"/>',
    "yarn": '<circle cx="12" cy="12" r="7.5"/><path d="M6 8.5c4 .5 8.5 3.5 10.5 9M5 12.5c3.5 0 7.5 2.5 9 6.5M8.5 5.2c3.3 1.4 7.5 5 9 9.5M12 4.5c2.5 2 4.5 4.5 5.8 7"/>',
    "palette": '<path d="M12 4a8 8 0 1 0 0 16c1.2 0 1.8-.8 1.8-1.7 0-1.3-1-1.5-1-2.6 0-1 .8-1.7 1.8-1.7H17a3 3 0 0 0 3-3C20 7 16.4 4 12 4z"/><circle cx="8" cy="11" r="1"/><circle cx="10.5" cy="7.8" r="1"/><circle cx="14.5" cy="8" r="1"/>',
    "cols": '<rect x="3.5" y="5" width="7.5" height="14"/><rect x="13" y="5" width="7.5" height="14"/>',
}


def ico(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


def stars(n=5, cls="stars"):
    return f'<span class="{cls}" aria-label="{n} z 5 hvězdiček">' + "".join(ico("star", "ico ico--star") for _ in range(n)) + "</span>"


# ---------- produktová karta (po najetí se rozbalí info, vzor cernaovecka.cz) ----------
def card(p, href="produkt.html"):
    flags = ""
    if "action" in p.get("flags", []):
        flags += '<span class="flag">Akce</span>'
    if "vyprodej" in p.get("flags", []):
        flags += '<span class="flag">Výprodej</span>'
    if p.get("save"):
        flags += f'<span class="flag flag--sleva">{e(p["save"])}</span>'
    std = f'<s>{e(p["std"]).replace(" ", "&nbsp;")}</s>' if p.get("std") else ""
    name = p["name"].replace("cmDROPS", "cm DROPS")
    inf = p.get("info") or {}
    lead = f'<p class="pc__lead">{e(inf["lead"])}</p>' if inf.get("lead") else ""
    specs = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in inf.get("specs", []))
    specs = f'<dl class="pc__specs">{specs}</dl>' if specs else ""
    return f'''<article class="pc">
  <div class="pc__box">
    <a class="pc__img" href="{href}">
      <span class="pc__flags">{flags}</span>
      <img src="{p["file"]}" alt="{e(name)}" loading="lazy" width="720" height="720">
    </a>
    <a class="pc__name" href="{href}">{e(name)}</a>
    <p class="pc__price">{std}<b>{kc(p["price"])}</b></p>
    <div class="pc__more">
      {lead}{specs}
      <p class="pc__av">{ico("check","ico ico--xs")} {e(p.get("av") or "")}</p>
      <button class="btn btn--cart btn--full" type="button" data-add data-name="{e(name)}" data-price="{p["price"]}" data-img="{p["file"]}">{ico("bag","ico ico--sm")}<span>Do košíku</span></button>
    </div>
  </div>
</article>'''


def sechead(title):
    return f'<div class="sh"><h2 class="h2">{title}</h2></div>'


def products(title, items, more, more_href="kategorie.html", cls="sec"):
    cards = "".join(card(p) for p in items)
    return f'''<section class="{cls}">
  <div class="wrap">
    {sechead(title)}
    <div class="pgrid">{cards}</div>
    <p class="sec__more"><a class="btn btn--line" href="{more_href}">{more}</a></p>
  </div>
</section>'''


# ---------- společné části ----------
NAV = [
    ("Příze na pletení", "kategorie.html", True),
    ("Háčkovací příze", "kategorie.html", False),
    ("Špagáty a macramé", "kategorie.html", False),
    ("Pomůcky", "kategorie.html", False),
    ("Korálky", "kategorie.html", False),
    ("Kameny a minerály", "kategorie.html", False),
    ("Bižuterní komponenty", "kategorie.html", False),
    ("Značky", "kategorie.html", False),
]

def _mt(label, img):
    return f'<a class="mega__t" href="kategorie.html"><span class="mega__ti"><img src="{img}" alt="" loading="lazy"></span><span>{label}</span></a>'


MEGAS = {
    "Příze na pletení": ("Podle složení", [("Alpaka", "img/p/prize-drops-brushed-alpaca-silk-44-svestka.jpg"), ("Merino a vlna", "img/p/prize-drops-andes-uni-colour-0100-smetanova.jpg"),
        ("Moherové příze", "img/photo/moher.jpg"), ("Bavlna", "img/p/prize-drops-flora-uni-colour-37-ranni-opar.jpg"), ("Akryl a směsi", "img/photo/ruzova-klubka.jpg")],
        "Podle síly příze", ["A jemné", "B slabší", "C střední", "D silnější", "E silné", "F velmi silné"]),
    "Háčkovací příze": ("Druhy", [("Kordonety", "img/photo/kordonet.jpg"), ("Moonlight", "img/p/prize-moonlight-8220-hneda.jpg"), ("Bavlna na háčkování", "img/p/prize-dolphin-baby-80310-tmavy-cyklamen.jpg"), ("Na amigurumi", "img/v2/proj-amigurumi.jpg")], None, None),
    "Špagáty a macramé": ("Druhy", [("Šňůry a cordy", "img/photo/macrame-snura.jpg"), ("Twisted macramé", "img/p/twisted-macrame-755-zelena.jpg"), ("Macramé bavlna", "img/p/prize-macrame-cotton-spectrum-1327-bezova-kastanova-tmavy-ty.jpg")], None, None),
    "Pomůcky": ("Druhy", [("Jehlice", "img/photo/jehlice.jpg"), ("Háčky", "img/p/hacek-drops-pro-circus-4-13-cm.jpg"), ("Značky na očka", "img/p/znacky-na-ocka-drops-stitch-markers-30ks.jpg"), ("Sady jehlic", "img/p/drops-pro-classic-interchangeable-circular-needles-set-3-5-8.jpg")], None, None),
    "Korálky": ("Druhy", [("Ohňovky", "img/photo/koralky.jpg"), ("Mačkané", "img/photo/koralky.jpg"), ("Dřevěné", "img/photo/koralky.jpg")], None, None),
    "Kameny a minerály": ("Druhy", [("Ametyst", "img/p/ametyst-kulicka-fazetovana-6mm.jpg"), ("Achát", "img/photo/kameny.jpg"), ("Všechny kameny", "img/photo/kameny.jpg")], None, None),
    "Bižuterní komponenty": ("Druhy", [("Kaplíky", "img/photo/komponenty.jpg"), ("Kaloty", "img/photo/komponenty.jpg"), ("Zapínání", "img/photo/komponenty.jpg")], None, None),
    "Značky": ("Značky", [("DROPS", "img/p/prize-drops-brushed-alpaca-silk-23-bordo.jpg"), ("Alize", "img/p/alize-puffy-310-bezova.jpg"), ("YarnArt", "img/p/prize-dolphin-baby-80310-tmavy-cyklamen.jpg"), ("Himalaya", "img/photo/ruzova-klubka.jpg"), ("Pletánky", "img/photo/klubko.jpg")],
        "DROPS příze", ["Brushed Alpaca Silk", "Sky", "Melody", "Air", "Flora", "Soft Tweed", "Nepal", "Alpaca", "Andes"]),
}


def mega(name):
    h, tiles, h2, links = MEGAS[name]
    side = ""
    if links:
        side = f'<div class="mega__col"><p class="mega__h">{h2}</p>' + "".join(f'<a href="kategorie.html">{l}</a>' for l in links) + '</div>'
    t = "".join(_mt(l, i) for l, i in tiles)
    return f'''<div class="mega" role="region" aria-label="{name}">
  <div class="mega__in wrap">
    <div class="mega__main"><p class="mega__h">{h}</p><div class="mega__tiles">{t}</div></div>
    {side}
  </div>
</div>'''


def header(active=""):
    links = ""
    for name, href, _m in NAV:
        cls = "nav__a" + (" is-active" if name == active else "")
        if name in MEGAS:
            links += f'<li class="nav__li has-mega"><a class="{cls}" href="{href}">{name}{ico("down","ico ico--xs")}</a>{mega(name)}</li>'
        else:
            links += f'<li class="nav__li"><a class="{cls}" href="{href}">{name}</a></li>'
    links += '<li class="nav__li"><a class="nav__a nav__a--akce" href="kategorie.html">Akce</a></li>'
    return f'''<a class="skip" href="#obsah">Přejít na obsah</a>
<div class="topbar">
  <div class="wrap topbar__in">
    <span>{ico("truck","ico ico--sm")} Doprava zdarma od 2&nbsp;000&nbsp;Kč</span>
    <span class="topbar__mid">Příze DROPS v akci až −30&nbsp;%</span>
    <span class="topbar__links"><a href="#">Doprava a platby</a><a href="#">Kontakt</a><a href="#">CZK / EUR</a></span>
  </div>
</div>
<header class="hdr" id="hdr">
  <div class="wrap hdr__in">
    <button class="hdr__burger" type="button" aria-label="Menu" data-menu-open>{ico("menu")}</button>
    <a class="logo" href="index.html" aria-label="Pletánky – úvod">
      <span class="logo__txt">Pletánky</span><small class="logo__sub">příze &amp; tvoření</small>
    </a>
    <form class="search" role="search" onsubmit="return false">
      {ico("search","ico ico--sm")}
      <input type="search" placeholder="Hledat přízi, barvu nebo značku…" aria-label="Hledat">
    </form>
    <nav class="hdr__acts" aria-label="Účet a košík">
      <a class="hdr__act" href="#">{ico("user")}<span>Přihlášení</span></a>
      <button class="hdr__act cartbtn" type="button" data-cart-open aria-label="Košík">
        <span class="cartbtn__ico">{ico("bag")}<b class="cartbtn__count" data-cart-count>0</b></span>
        <span data-cart-total>0&nbsp;Kč</span>
      </button>
    </nav>
  </div>
  <nav class="nav" aria-label="Kategorie">
    <ul class="wrap nav__ul">{links}</ul>
  </nav>
</header>'''


def mobile_menu():
    items = "".join(f'<a href="{h}">{n}{ico("chev","ico ico--sm")}</a>' for n, h, _ in NAV)
    return f'''<div class="drawer drawer--menu" data-menu aria-hidden="true">
  <div class="drawer__panel">
    <div class="drawer__head"><span class="logo__txt">Pletánky</span><button type="button" data-menu-close aria-label="Zavřít">{ico("close")}</button></div>
    <nav class="mmenu">{items}<a class="mmenu__akce" href="kategorie.html">Akce{ico("chev","ico ico--sm")}</a></nav>
    <div class="mmenu__foot"><a href="#">{ico("user","ico ico--sm")} Přihlášení</a><a href="#">{ico("mail","ico ico--sm")} info@pletanky.cz</a></div>
  </div>
</div>'''


def cart_drawer():
    return f'''<div class="drawer drawer--cart" data-cart aria-hidden="true">
  <div class="drawer__panel">
    <div class="drawer__head"><b>Košík</b><button type="button" data-cart-close aria-label="Zavřít">{ico("close")}</button></div>
    <div class="freeship"><p data-free-txt>Do dopravy zdarma zbývá <b>2&nbsp;000&nbsp;Kč</b></p><span class="freeship__bar"><i data-free-bar></i></span></div>
    <ul class="cartlist" data-cart-list><li class="cartlist__empty">Košík je zatím prázdný.</li></ul>
    <div class="drawer__foot">
      <p class="cartsum"><span>Celkem</span><b data-cart-total>0&nbsp;Kč</b></p>
      <a class="btn btn--cart btn--full" href="#">Pokračovat k objednávce</a>
      <button class="btn btn--line btn--full" type="button" data-cart-close>Nakupovat dál</button>
    </div>
  </div>
</div>
<div class="toast" data-toast role="status" aria-live="polite"></div>'''


def demo_panel():
    """Přepínač barevných variant + informace o ukázce (není součást e-shopu)."""
    return f'''<div class="demo" role="region" aria-label="Ovládání ukázky">
  <span class="demo__l">{ico("palette","ico ico--sm")}<span>Nezávazná ukázka, verze 5</span></span>
  <button type="button" class="demo__b" data-theme-set="d" aria-label="Fialová varianta"><i class="demo__sw demo__sw--d"></i><span>Fialová</span></button>
  <button type="button" class="demo__b" data-theme-set="e" aria-label="Červená varianta"><i class="demo__sw demo__sw--e"></i><span>Červená</span></button>
  <button type="button" class="demo__info" data-about-open aria-label="O ukázce">{ico("info","ico ico--sm")}<span>O ukázce</span></button>
</div>
<div class="drawer drawer--about" data-about aria-hidden="true">
  <div class="drawer__panel">
    <div class="drawer__head"><b>Nezávazná ukázka, verze 5</b><button type="button" data-about-close aria-label="Zavřít">{ico("close")}</button></div>
    <div class="about">
      <p>Upravená ukázka vzhledu e-shopu <b>Pletánky.cz</b> od Studentských Webů podle Vaší zpětné vazby.</p>
      <ul>
        <li>Barvy: lišty i drobné detaily (tlačítka, akce, ceny) mají vždy stejný odstín. Dole je přepínač: fialová (odstín původních lišt) a červená (odstín dosavadních akcentů).</li>
        <li>Logo je vlevo, vyhledávání uprostřed. Oblíbené kategorie mají původní rozložení, rohy tlačítek a fotek jsou jemně zaoblené.</li>
        <li>Sekce „Krása podzimu“ je prostor pro téma měsíce a doporučené produkty, její název i výběr se dá měnit. Odstín měsíce je v banneru jako malý rámeček.</li>
        <li>Jedno písmo pro všechny nadpisy i názvy, u každé sekce jeden nadpis, jemně zaoblené rohy a sekce oddělené jemnou linkou.</li>
        <li>Najeďte myší na produkt: rozbalí se složení, návin, jehlice a tlačítko do košíku.</li>
        <li>Recenze jsou skutečná hodnocení z Vaší stránky Hodnocení obchodu (stav 10.&nbsp;10.&nbsp;2026). Komentáře k produktům jsou jen ilustrační místa.</li>
        <li>Názvy, ceny a údaje produktů jsou z pletanky.cz. Fotky v banneru, u projektů a v blogu jsou ilustrační (volně použitelné z Pexels), nahradí je Vaše vlastní. Logo je zatím zástupné.</li>
        <li>Všechno se dá postavit jako vlastní vzhled na Shoptetu. Objednávky, zboží i zákaznické účty zůstanou, kde jsou.</li>
      </ul>
      <p class="about__nav"><a href="index.html">Úvod</a><a href="kategorie.html">Kategorie</a><a href="produkt.html">Detail produktu</a><a href="v1/index.html">První verze</a></p>
    </div>
  </div>
</div>'''


def footer():
    return f'''<footer class="ftr">
  <div class="wrap ftr__grid">
    <div class="ftr__brand">
      <span class="logo__txt">Pletánky</span>
      <p>Příze na pletení a háčkování, macramé šňůry, korálky a všechno pro tvoření.</p>
      <p class="ftr__soc"><a href="#" aria-label="Instagram">{ico("ig")}</a><a href="#" aria-label="Facebook">{ico("fb")}</a></p>
    </div>
    <div><p class="ftr__h">Sortiment</p><a href="kategorie.html">Příze na pletení</a><a href="kategorie.html">Háčkovací příze</a><a href="kategorie.html">Špagáty a macramé</a><a href="kategorie.html">Korálky a kameny</a><a href="kategorie.html">Dárkové poukazy</a></div>
    <div><p class="ftr__h">Nakupování</p><a href="#">Doprava a platby</a><a href="#">Obchodní podmínky</a><a href="#">Ochrana osobních údajů</a><a href="#">Hodnocení obchodu</a></div>
    <div><p class="ftr__h">Kontakt</p><a href="#">info@pletanky.cz</a><a href="#">Kontakty</a><a href="#">Blog a návody</a></div>
  </div>
  <div class="wrap ftr__bottom"><span>© Pletánky.cz</span><span>Nezávazná ukázka vzhledu · Studentské Weby</span></div>
</footer>'''


THEME_JS = "<script>(function(){var q=new URLSearchParams(location.search).get('barvy'),t=(q==='e'||q==='d')?q:(sessionStorage.getItem('pl-theme')||'d');document.documentElement.setAttribute('data-theme',t)})();if(new URLSearchParams(location.search).has('nahled'))document.documentElement.classList.add('is-preview')</script>"

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap&subset=latin-ext" rel="stylesheet">'


def page(title, body, active="", cls="", desc="Nezávazná ukázka vzhledu e-shopu Pletánky.cz"):
    return f'''<!doctype html>
<html lang="cs" data-theme="d">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:image" content="https://webhunter-navrhy.github.io/pletanky-ukazka/img/v2/hero.jpg">
<meta property="og:title" content="{e(title)}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Store","name":"Pletánky.cz","url":"https://www.pletanky.cz","description":"Příze, háčkování, macramé, korálky a bižuterní komponenty"}}</script>
{THEME_JS}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<link rel="stylesheet" href="style.css?v=0">
<script src="main.js?v=0" defer></script>
</head>
<body class="{cls}">
{header(active)}
<main id="obsah">
{body}
</main>
{footer()}
{mobile_menu()}
{cart_drawer()}
{demo_panel()}
</body>
</html>
'''


# ================= ÚVOD =================
TILES = [
    ("Příze na pletení", "Alpaka, merino, moher i bavlna od DROPS, Alize a YarnArt", "img/photo/moher.jpg"),
    ("Háčkovací příze", "Kordonety, Moonlight, Sněhurka a další", "img/photo/kordonet.jpg"),
    ("Špagáty a macramé", "Šňůry, cordy a Twisted macrame", "img/photo/macrame-snura.jpg"),
    ("Pomůcky", "Jehlice, háčky a značky na očka", "img/photo/jehlice.jpg"),
    ("Korálky", "Ohňovky, mačkané i dřevěné", "img/photo/koralky.jpg"),
    ("Kameny a minerály", "Achát, ametyst a další", "img/photo/kameny.jpg"),
    ("Bižuterní komponenty", "Kaplíky, kaloty, zapínání", "img/photo/komponenty.jpg"),
    ("Dárkové poukazy", "Pro všechny, kdo rádi tvoří", "img/photo/klubko.jpg"),
]


MOSAIC = [" t--big", "", "", " t--tall", "", "", "", ""]


def tile(name, sub, img, href="kategorie.html", tag="", cls=""):
    tag = f"<small>{tag}</small>" if tag else ""
    return f'''<a class="tile{cls}" href="{href}">
  <img src="{img}" alt="" loading="lazy">
  <span class="tile__box">{tag}<b>{name}</b><span class="tile__more"><span>{sub}</span></span></span>
</a>'''


PROJ = [("Svetry a kardigany", "img/v2/proj-svetry.jpg"), ("Čepice a šály", "img/v2/proj-cepice.jpg"),
        ("Ponožky", "img/v2/proj-ponozky.jpg"), ("Deky a pledy", "img/v2/proj-deky.jpg"),
        ("Hračky a amigurumi", "img/v2/proj-amigurumi.jpg"), ("Macramé do bytu", "img/v2/proj-macrame.jpg"),
        ("Šperky a bižuterie", "img/v2/proj-sperky.jpg")]
COMP = ["Alpaka", "Merino", "Moher", "Bavlna", "Hedvábí", "Akryl a směsi"]
WEIGHT = [("A", "jemné"), ("B", "slabší"), ("C", "střední"), ("D", "silnější"), ("E", "silné"), ("F", "velmi silné")]


def projects():
    p = "".join(f'<a class="proj" href="kategorie.html"><span class="proj__img"><img src="{i}" alt="" loading="lazy"></span><span class="proj__n">{n}</span></a>' for n, i in PROJ)
    c = "".join(f'<a class="chip" href="kategorie.html">{n}</a>' for n in COMP)
    w = "".join(f'<a class="chip" href="kategorie.html"><b>{g}</b> {t}</a>' for g, t in WEIGHT)
    return f'''<section class="sec">
  <div class="wrap">
    {sechead("Vyberte podle projektu")}
    <div class="projs">{p}</div>
  </div>
</section>'''


POSTS = [
    ("Pro začátečnice", "Jak vybrat přízi na první svetr", "Jaká síla příze, kolik klubek a z jakého materiálu. Krok za krokem až k prvnímu nahozenému oku.", "img/photo/ruce-pleteni.jpg"),
    ("Macramé", "První závěs krok za krokem", "Tři základní uzly, jedna dřevěná tyčka a odpoledne času. Ukážeme, jakou šňůru vybrat.", "img/v2/blog-macrame.jpg"),
    ("Tip", "Příplet z alpaky a hedvábí", "Jak Brushed Alpaca Silk změkčí a zjemní téměř jakoukoli přízi a jak spočítat spotřebu.", "img/photo/ruzova-klubka.jpg"),
    ("Háčkování", "Taška z bavlněné příze", "Pevná a pratelná taška na léto. Návod s fotkami a seznam všeho, co budete potřebovat.", "img/v2/blog-taska.jpg"),
]


def blog():
    t = "".join(tile(n, x, i, "#", tag) for tag, n, x, i in POSTS)
    return f'''<section class="sec">
  <div class="wrap">
    {sechead("Z blogu")}
    <div class="tiles tiles--blog">{t}</div>
    <p class="sec__note">Ukázkové články</p>
    <p class="sec__more"><a class="btn btn--line" href="#">Všechny články</a></p>
  </div>
</section>'''


# skutečná hodnocení z https://www.pletanky.cz/hodnoceni-obchodu/ (stav 10. 10. 2026), jména zkrácená
REVIEWS = [
    ("Lenka S.", "16. 4. 2026", "Maximální spokojenost, velmi rychlé vyřízení objednávky, rychlé dodání, nakupuji opakovaně."),
    ("Gabriela F.", "15. 1. 2026", "Skvělý obchůdek, dobrý výběr i ceny, ochotní a vstřícní lidé a rychlé dodání. Jsem moc spokojená, nakupuji opakovaně, určitě jen doporučuji."),
    ("Jana K.", "18. 8. 2025", "Velmi rychlé dodání, jeden den objednáte, druhý máte a pak už jen pletete a háčkujete a je to krása :-)"),
    ("Jana A.", "11. 7. 2025", "Ihned při zaplacení odesláno. Udělala jsem chybu v e-mailu ale s lidma na podpoře se dalo skvěle domluvit. Vlny dorazily v pořádku a v uvedené kvalitě. Určitě budu zde znovu objednávat ❤️"),
    ("Ivana H.", "24. 11. 2025", "Vždy vše v pořádku. Doporučuji."),
    ("Pavla W.", "13. 4. 2026", "Určitě doporučuji"),
]
DIST = [(5, 4549), (4, 22), (3, 6), (2, 1), (1, 2)]


def reviews():
    total = sum(n for _, n in DIST)
    bars = "".join(f'<li><span>{s}</span>{ico("star","ico ico--star")}<i><b style="width:{n / total * 100:.1f}%"></b></i><em>{n:,}</em></li>'.replace(",", "&nbsp;") for s, n in DIST)
    cards = "".join(f'<figure class="rv">{stars()}<blockquote>{e(t)}</blockquote><figcaption><b>{e(n)}</b><span>{d.replace(" ", "&nbsp;")}</span></figcaption></figure>' for n, d, t in REVIEWS[:3])
    pc = [p for p in P["cat"] if any(k in p["name"] for k in ["44 - švestka", "20 - růžový", "41 - pšeničné"])]
    comments = "".join(f'''<figure class="rv rv--prod"><a class="rv__p" href="produkt.html"><img src="{p["file"]}" alt="" loading="lazy"><span>{e(p["name"])}</span></a>{stars()}<blockquote class="rv__ph">Tady se automaticky zobrazí poslední komentář zákaznice k tomuto produktu.</blockquote><figcaption><b>Jméno zákaznice</b><span class="tag">ilustrační</span></figcaption></figure>''' for p in pc)
    return f'''<section class="sec">
  <div class="wrap">
    {sechead("Recenze zákazníků")}
    <div class="rvs">
      <div class="rvs__sum">
        <p class="rvs__score">5,0</p>
        {stars(5, "stars stars--lg")}
        <p class="rvs__cnt">{total:,} hodnocení obchodu</p>
        <ul class="rvs__dist">{bars}</ul>
        <a class="btn btn--line btn--full" href="#">Všechna hodnocení</a>
      </div>
      <div class="rvs__main" data-tabs>
        <div class="rvs__tabs" role="tablist"><button class="is-on" type="button" data-tab>Hodnocení obchodu</button><button type="button" data-tab>Komentáře k produktům</button></div>
        <div class="tabs__panel is-on"><div class="rvs__grid">{cards}</div><p class="sec__note">Skutečná hodnocení ze stránky Hodnocení obchodu na pletanky.cz. V Shoptetu se načítají samy.</p></div>
        <div class="tabs__panel"><div class="rvs__grid rvs__grid--3">{comments}</div><p class="sec__note">Ilustrační ukázka: komentáře k produktům se zobrazí, jakmile je zákaznice napíšou.</p></div>
      </div>
    </div>
  </div>
</section>'''.replace("4,580", "4&nbsp;580")


IG = ["ig26", "ig18", "ig19", "ig25", "ig28", "ig23", "ig31", "ig29", "ig20", "ig21", "ig22", "ig24", "ig27", "ig30"]


def instagram():
    imgs = "".join(f'<a class="film__i" href="#"><img src="img/ig/{i}.jpg" alt="Příspěvek @pletanky" loading="lazy"></a>' for i in IG)
    return f'''<section class="sec sec--film">
  <div class="wrap">{sechead('Instagram <a href="#">@pletanky</a>')}</div>
  <div class="film"><div class="film__track">{imgs}{imgs}</div></div>
</section>'''


svestka = next(p for p in P["cat"] if "44 - švestka" in p["name"])

home_body = f'''
<section class="banner">
  <picture><source media="(max-width:760px)" srcset="img/v2/hero-m.jpg"><img class="banner__img" src="img/v2/hero.jpg" alt="Pletený svetr a šálek kávy" fetchpriority="high"></picture>
  <div class="wrap banner__in">
    <div class="banner__box">
      <h1 class="h1">Každý projekt začíná jedním klubkem</h1>
      <p>Příze DROPS, Alize a YarnArt, šňůry na macramé, korálky a kameny. Vyberte si barvu, která Vám udělá radost.</p>
      <a class="motm-mini" href="produkt.html"><img src="img/p/svestka-velka.jpg" alt=""><span><small>Odstín měsíce</small><b>DROPS Brushed Alpaca Silk 44 – švestka</b></span></a>
      <div class="banner__cta">
        <a class="btn btn--cart" href="kategorie.html">Vybrat přízi</a>
        <a class="btn btn--line" href="kategorie.html">Akce DROPS až −30&nbsp;%</a>
      </div>
    </div>
  </div>
</section>

<div class="usp">
  <div class="wrap usp__in">
    <span>{ico("yarn","ico ico--sm")} Široký výběr produktů</span>
    <span>{ico("gift","ico ico--sm")} Balíme s láskou</span>
    <span>{ico("check","ico ico--sm")} Tvoříme vědomě</span>
    <span>{ico("star","ico ico--sm")} Prodáváme, co sami používáme</span>
  </div>
</div>

<section class="sec">
  <div class="wrap">
    {sechead("Oblíbené kategorie")}
    <div class="tiles tiles--orig">{"".join(tile(*t, cls=c) for t, c in zip(TILES, MOSAIC))}</div>
  </div>
</section>

{products("Akce", P["akce"][:4], "Celá akce")}

{projects()}

<section class="sec">
  <div class="wrap">
    {sechead("Krása podzimu")}
    <p class="sec__lead">Téma měsíce: tipy a doporučené produkty k nákupu.</p>
    <div class="pgrid">{"".join(card(p) for p in P["mix"][4:8])}</div>
    <p class="sec__more"><a class="btn btn--line" href="kategorie.html">Všechny tipy</a></p>
  </div>
</section>

{products("Novinky", P["mix"][:4], "Všechny novinky")}

{blog()}

{reviews()}

{instagram()}

<section class="news">
  <div class="wrap news__in">
    <h2 class="h2">Newsletter</h2>
    <p>Nové odstíny, akce na příze a tipy na projekty. Jednou za čas, nikdy otravně.</p>
    <form class="news__form" onsubmit="return false">
      <input type="email" placeholder="Váš e-mail" aria-label="E-mail">
      <button class="btn btn--cart" type="submit">Odebírat</button>
    </form>
  </div>
</section>
'''

# ================= KATEGORIE =================
SWATCH = {"44": "#5b2340", "23": "#7a1f2c", "34": "#d9cbe3", "43": "#3a1d2c", "20": "#e8cfc6", "36": "#b4875a",
          "40": "#efe3d6", "05": "#9b8670", "08": "#b45a85", "37": "#f6c6a0", "06": "#ef6a5c", "41": "#c7a12a"}


def filters():
    sw = "".join(f'<button class="sw" type="button" style="--c:{c}" aria-label="odstín {k}"></button>' for k, c in SWATCH.items())
    return f'''<aside class="filters" data-filters>
  <div class="filters__head"><b>Filtrovat</b><button type="button" data-filters-close aria-label="Zavřít">{ico("close")}</button></div>
  <div class="fgroup"><p class="fgroup__h">Dostupnost</p><label class="chk"><input type="checkbox" checked><span></span>Skladem <em>43</em></label><label class="chk"><input type="checkbox"><span></span>V akci <em>43</em></label></div>
  <div class="fgroup"><p class="fgroup__h">Cena</p><div class="range"><i style="left:0;right:0"></i><b style="left:0"></b><b style="right:0"></b></div><p class="range__v"><span>57 Kč</span><span>57 Kč</span></p></div>
  <div class="fgroup"><p class="fgroup__h">Barva</p><div class="sws">{sw}</div></div>
  <div class="fgroup"><p class="fgroup__h">Velikost jehlic</p><label class="chk"><input type="checkbox"><span></span>5 mm <em>43</em></label></div>
  <div class="fgroup"><p class="fgroup__h">Značka</p><label class="chk"><input type="checkbox" checked><span></span>DROPS <em>43</em></label></div>
  <button class="btn btn--cart btn--full filters__apply" type="button" data-filters-close>Zobrazit 43 produktů</button>
</aside>'''


cat_cards = "".join(card(p) for p in P["cat"])
cat_body = f'''
<section class="chero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Domů</a><i>/</i><a href="kategorie.html">Příze na pletení a háčkování</a><i>/</i><a href="kategorie.html">Mohérové příze</a><i>/</i><span>DROPS Brushed Alpaca Silk</span></nav>
    <div class="chero__in">
      <div class="chero__txt">
        <h1 class="h1 h1--cat">DROPS Brushed Alpaca Silk</h1>
        <p>Luxusní směs hebké česané alpaky a jemně lesklého hedvábí. Lehoučká a překvapivě hřejivá příze ve vytříbených odstínech, od něžných béžových a šedých tónů po červené a fialové. Skvělá i jako příplet.</p>
        <dl class="specs">
          <div><dt>Složení</dt><dd>77 % alpaka, 23 % hedvábí</dd></div>
          <div><dt>Klubko</dt><dd>25 g / 140 m</dd></div>
          <div><dt>Jehlice</dt><dd>5 mm</dd></div>
          <div><dt>Skupina</dt><dd>C · aran / worsted</dd></div>
        </dl>
      </div>
      <div class="chero__img"><img src="img/photo/ruzova-klubka.jpg" alt=""></div>
    </div>
    <div class="subcats">
      <a class="subcat is-on" href="kategorie.html">Brushed Alpaca Silk</a><a class="subcat" href="kategorie.html">Kid-Silk</a><a class="subcat" href="kategorie.html">Melody</a><a class="subcat" href="kategorie.html">Air</a><a class="subcat" href="kategorie.html">Alize Mohair</a><a class="subcat" href="kategorie.html">Mohair De Luxe</a>
    </div>
  </div>
</section>

<section class="cbody">
  <div class="wrap cbody__in">
    {filters()}
    <div class="clist">
      <div class="ctool">
        <button class="btn btn--line btn--sm ctool__filter" type="button" data-filters-open>{ico("filter","ico ico--sm")} Filtrovat</button>
        <div class="sort" role="tablist"><button class="is-on" type="button">Nejprodávanější</button><button type="button">Nejlevnější</button><button type="button">Nejdražší</button><button type="button">Abecedně</button></div>
        <span class="ctool__count">43 produktů</span>
      </div>
      <div class="pgrid pgrid--3">{cat_cards}</div>
      <div class="more"><p>Zobrazeno 12 ze 43</p><span class="more__bar"><i style="width:28%"></i></span><button class="btn btn--line" type="button">Načíst dalších 31</button></div>
    </div>
  </div>
</section>
'''

# ================= PRODUKT =================
sv = svestka
others = [p for p in P["cat"] if p is not sv]
swatches = "".join(f'<a class="pswatch{" is-on" if p is sv else ""}" href="produkt.html" title="{e(p["name"].split(" Silk ")[1])}"><img src="{p["file"]}" alt=""></a>' for p in [sv] + others)
tools = [p for p in P["mix"] if any(k in p["name"] for k in ["ponožkové", "Značky na očka", "Háček", "Interchangeable"])]
prod_body = f'''
<section class="pd">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Domů</a><i>/</i><a href="kategorie.html">Příze na pletení a háčkování</a><i>/</i><a href="kategorie.html">Mohérové příze</a><i>/</i><a href="kategorie.html">DROPS Brushed Alpaca Silk</a></nav>
    <div class="pd__in">
      <div class="pd__gal">
        <div class="pd__main"><span class="pc__flags"><span class="flag">Akce</span><span class="flag flag--sleva">–29 %</span></span><img src="img/p/svestka-velka.jpg" alt="Příze DROPS Brushed Alpaca Silk 44 – švestka"></div>
        <div class="pd__thumbs"><button class="is-on" type="button"><img src="img/p/svestka-velka.jpg" alt=""></button><span class="pd__ph">Vaše<br>fotka</span><span class="pd__ph">Vaše<br>fotka</span></div>
      </div>
      <div class="pd__info">
        <p class="pd__brand">DROPS · Kód 94580</p>
        <h1 class="h1 h1--pd">Příze DROPS Brushed Alpaca Silk 44 – švestka</h1>
        <p class="pd__lead">Přepychová směs počesané alpaky a morušového hedvábí. Lehoučká, hřejivá a krásně vzdušná.</p>
        <div class="pd__price"><b>57&nbsp;Kč</b><s>81&nbsp;Kč</s><span class="flag flag--sleva">–29 %</span><small>47,11 Kč bez DPH · za klubko 25 g</small></div>
        <p class="pd__av">{ico("check","ico ico--sm")} Skladem <span>(55 ks)</span></p>
        <div class="pd__swh"><p>Odstín: <b>44 – švestka</b> <span>· dalších 42 odstínů</span></p><div class="pswatches">{swatches}</div></div>
        <div class="pd__buy">
          <div class="qty"><button type="button" data-qty="-1" aria-label="Méně">{ico("minus","ico ico--sm")}</button><input type="number" value="1" min="1" aria-label="Množství" data-qty-input><button type="button" data-qty="1" aria-label="Více">{ico("plus","ico ico--sm")}</button></div>
          <button class="btn btn--cart btn--buy" type="button" data-add data-name="Příze DROPS Brushed Alpaca Silk 44 - švestka" data-price="57" data-img="img/p/prize-drops-brushed-alpaca-silk-44-svestka.jpg" data-qty-from>{ico("bag","ico ico--sm")} Přidat do košíku</button>
        </div>
        <ul class="pd__usp">
          <li>{ico("truck","ico ico--sm")} Doprava zdarma od 2&nbsp;000&nbsp;Kč</li>
          <li>{ico("mail","ico ico--sm")} Nevíte si rady s množstvím? Napište nám</li>
        </ul>
        <dl class="specs specs--pd">
          <div><dt>Složení</dt><dd>77 % alpaka, 23 % hedvábí</dd></div>
          <div><dt>Klubko</dt><dd>25 g / cca 140 m</dd></div>
          <div><dt>Jehlice / háček</dt><dd>5 mm</dd></div>
          <div><dt>Vzorek 10×10 cm</dt><dd>17 ok × 24 řad</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap">
    <div class="tabs" data-tabs>
      <div class="tabs__nav" role="tablist"><button class="is-on" type="button" data-tab>Popis</button><button type="button" data-tab>Parametry</button><button type="button" data-tab>Hodnocení</button></div>
      <div class="tabs__panel is-on">
        <p>Příze je lehoučká a překvapivě hřejivá – je proto velmi vhodná na drobné i větší kousky a můžete ji plést na silnějších jehlicích, takže práce rychle přibývá. Přízi DROPS Brushed Alpaca Silk lze využít rovněž jako efektní příplet v kombinaci s jinou přízí, výsledný úplet pak získá nebývalou jemnost!</p>
        <p>Prát v ruce, max. 30 °C, sušit volně rozložené.</p>
      </div>
      <div class="tabs__panel"><table class="ptable"><tr><th>Kategorie</th><td>DROPS Brushed Alpaca Silk</td></tr><tr><th>Složení</th><td>77 % alpaka, 23 % hedvábí</td></tr><tr><th>Skupina přízí</th><td>C (16–19 ok) / 10 ply / aran / worsted</td></tr><tr><th>Hmotnost / návin</th><td>25 g / 140 m</td></tr><tr><th>Velikost jehlic</th><td>5</td></tr><tr><th>Velikost háčku</th><td>5</td></tr><tr><th>Barva</th><td>červená</td></tr></table></div>
      <div class="tabs__panel"><p class="muted">Produkt zatím nikdo nehodnotil. Buďte první!</p></div>
    </div>
  </div>
</section>

{products("Ke klubku se hodí", tools, "Všechny pomůcky")}
{products("Další odstíny", others[:4], "Celá kategorie")}
'''

# ================= SROVNÁNÍ VARIANT =================
cmp_page = f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Pletánky.cz – barevné varianty vedle sebe | ukázka vzhledu</title>
{FONTS}
<link rel="stylesheet" href="style.css?v=0">
</head>
<body class="cmp">
<header class="cmp__head">
  <a class="cmp__back" href="index.html">← Zpět do ukázky</a>
  <p>Obě barevné varianty vedle sebe. Každou stránku můžete posouvat a proklikávat zvlášť.</p>
  <span class="cmp__pages"><button type="button" class="is-on" data-cmp="index.html">Úvod</button><button type="button" data-cmp="kategorie.html">Kategorie</button><button type="button" data-cmp="produkt.html">Detail</button></span>
</header>
<main class="cmp__grid">
  <figure><figcaption><b>A</b> Světlá: bílá, smetanová a champagne, zlatá tlačítka „do košíku“</figcaption><div class="cmp__frame"><iframe src="index.html?barvy=a&amp;nahled=1" title="Varianta A" loading="eager"></iframe></div></figure>
  <figure><figcaption><b>B</b> Zlatá horní a spodní lišta, bordó místo zlaté</figcaption><div class="cmp__frame"><iframe src="index.html?barvy=b&amp;nahled=1" title="Varianta B" loading="eager"></iframe></div></figure>
</main>
<script>
const fit=()=>document.querySelectorAll('.cmp__frame').forEach(fr=>{{
  const f=fr.querySelector('iframe'),w=fr.clientWidth,h=fr.clientHeight,vw=w<700?w:1440,s=w/vw;
  f.style.width=vw+'px';f.style.height=(h/s)+'px';f.style.transform='scale('+s+')';
}});
addEventListener('resize',fit);fit();
document.querySelectorAll('[data-cmp]').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelectorAll('[data-cmp]').forEach(x=>x.classList.toggle('is-on',x===b));
  document.querySelectorAll('.cmp__frame iframe').forEach((f,i)=>f.src=b.dataset.cmp+'?barvy='+(i?'b':'a')+'&nahled=1');
}}));
</script>
</body>
</html>
'''

(ROOT / "index.html").write_text(page("Pletánky.cz – příze, macramé a korálky | ukázka vzhledu", home_body))
(ROOT / "kategorie.html").write_text(page("DROPS Brushed Alpaca Silk – Pletánky.cz | ukázka vzhledu", cat_body, "Příze na pletení"))
(ROOT / "produkt.html").write_text(page("Příze DROPS Brushed Alpaca Silk 44 – švestka – Pletánky.cz | ukázka vzhledu", prod_body, "Příze na pletení", "page-pd"))
print("ok")
