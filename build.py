#!/usr/bin/env python3
"""Generuje index.html, kategorie.html a produkt.html ukázky Pletánky.cz z produkty.json.
Data produktů (názvy, ceny, dostupnost, fotky) jsou převzatá z pletanky.cz 7. 10. 2026."""
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
P = json.loads((ROOT / "produkty.json").read_text())
e = html.escape


def kc(v):
    s = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    s = s[:-3] if s.endswith(",00") else s
    return s + " Kč"


# ---------- ikonky (tenké linky) ----------
ICON = {
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>',
    "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1.2-3.6 4-5.3 7.5-5.3s6.3 1.7 7.5 5.3"/>',
    "bag": '<path d="M5.5 8.5h13l-1 11.5h-11z"/><path d="M9 8.5V7a3 3 0 0 1 6 0v1.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "filter": '<path d="M4 6h16M7 12h10M10 18h4"/>',
    "truck": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "mail": '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "gift": '<rect x="4" y="9" width="16" height="11" rx="1"/><path d="M4 13h16M12 9v11M12 9c-1.5-3-5-3.5-5-1.2C7 9 9.5 9 12 9zm0 0c1.5-3 5-3.5 5-1.2C17 9 14.5 9 12 9z"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "star": '<path d="m12 4 2.4 5 5.4.6-4 3.7 1.1 5.3L12 16l-4.9 2.6 1.1-5.3-4-3.7 5.4-.6z"/>',
    "ig": '<rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="17" cy="7" r=".6"/>',
    "fb": '<path d="M14 8h2.5V4.5H14A3.5 3.5 0 0 0 10.5 8v2.5H8V14h2.5v6H14v-6h2.5l.5-3.5h-3V8.5c0-.3.2-.5.5-.5z"/>',
    "minus": '<path d="M6 12h12"/>',
    "plus": '<path d="M12 6v12M6 12h12"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8v.4"/>',
    # piktogramy kategorií
    "yarn": '<circle cx="12" cy="12" r="7.5"/><path d="M6 8.5c4 .5 8.5 3.5 10.5 9M5 12.5c3.5 0 7.5 2.5 9 6.5M8.5 5.2c3.3 1.4 7.5 5 9 9.5M12 4.5c2.5 2 4.5 4.5 5.8 7"/><path d="M17 19.5c1.5.8 3 .5 3.5-.5"/>',
    "needles": '<path d="m5 19 12-12M8 20 20 8"/><circle cx="17.8" cy="6.2" r="1.3"/><circle cx="20.8" cy="7.2" r="1.3"/><path d="M4 20c-1 2 3 2 4 0"/>',
    "hook": '<path d="M7 20 17.5 6.5a1.8 1.8 0 1 0-2.8-2.2"/><path d="M10 16.2 12.2 18"/>',
    "knot": '<path d="M12 3v5M9 3v4c0 2 3 2.5 3 5M15 3v4c0 2-3 2.5-3 5"/><path d="M12 12c-2 0-4 1.5-4 4v5M12 12c2 0 4 1.5 4 4v5M12 12v9"/>',
    "bead": '<circle cx="7" cy="13" r="3"/><circle cx="13.5" cy="11" r="3"/><circle cx="19" cy="14" r="2.2"/><path d="M2.5 12.5c1 .3 1.5.4 1.5.4M10 12.3l.5-.2M16.5 12.2l.6.4"/>',
    "gem": '<path d="M6 4h12l3 5-9 11L3 9z"/><path d="M3 9h18M9 4l3 16M15 4l-3 16"/>',
    "clasp": '<circle cx="8" cy="13" r="4.5"/><path d="M12.5 13H20M17 13v-2.5"/><path d="M6.5 8.7 8 6"/>',
    "sweater": '<path d="M9 4c.5 1.5 1.5 2 3 2s2.5-.5 3-2l5 2.5-1.5 5-2-.7V20H7.5v-9.2l-2 .7L4 6.5z"/>',
    "hat": '<path d="M5 17c0-5 3-9.5 7-9.5s7 4.5 7 9.5"/><path d="M4 17h16v3H4zM12 7.5V5"/><circle cx="12" cy="4" r="1.3"/>',
    "sock": '<path d="M9 3h6v9l2.5 3.2a2.8 2.8 0 0 1-4.3 3.6L8.5 13A3 3 0 0 1 9 11z"/><path d="M9 6h6"/>',
    "blanket": '<path d="M4 6h16v10H4z"/><path d="M4 16c0 2 2 3 4 3h12v-3M4 9.5h16M4 13h16"/>',
    "toy": '<circle cx="12" cy="13" r="6"/><circle cx="7.5" cy="6.5" r="2"/><circle cx="16.5" cy="6.5" r="2"/><path d="M10 13h.01M14 13h.01M10.5 16c1 .8 2 .8 3 0"/>',
    "home": '<path d="M4 11 12 4l8 7"/><path d="M6.5 9.5V20h11V9.5"/><path d="M10 20v-4.5h4V20"/>',
    "ring": '<circle cx="12" cy="14" r="6"/><path d="m9.5 4 2.5 3 2.5-3z"/>',
}


def ico(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[name]}</svg>'


# ---------- produktová karta ----------
def card(p, href="produkt.html"):
    flags = ""
    if "action" in p.get("flags", []):
        flags += '<span class="flag flag--akce">Akce</span>'
    if "vyprodej" in p.get("flags", []):
        flags += '<span class="flag flag--vyprodej">Výprodej</span>'
    if p.get("save"):
        flags += f'<span class="flag flag--sleva">{e(p["save"])}</span>'
    std = f'<s class="price__std">{e(p["std"])}</s>' if p.get("std") else ""
    av = e(p.get("av") or "")
    name = p["name"].replace("cmDROPS", "cm DROPS")
    return f'''<article class="pcard reveal">
  <a class="pcard__img" href="{href}">
    <span class="pcard__flags">{flags}</span>
    <img src="{p["file"]}" alt="{e(name)}" loading="lazy" width="720" height="720">
  </a>
  <div class="pcard__body">
    <a class="pcard__name" href="{href}">{e(name)}</a>
    <span class="pcard__av">{ico("check","ico ico--xs")} {av}</span>
    <div class="pcard__foot">
      <span class="price">{std}<b>{kc(p["price"])}</b></span>
      <button class="pcard__add" type="button" data-add data-name="{e(name)}" data-price="{p["price"]}" data-img="{p["file"]}" aria-label="Přidat do košíku">{ico("bag","ico ico--sm")}<span>Do košíku</span></button>
    </div>
  </div>
</article>'''


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

MEGA = '''<div class="mega" role="region" aria-label="Příze na pletení">
  <div class="mega__in wrap">
    <div class="mega__col">
      <p class="mega__h">DROPS</p>
      <a href="kategorie.html">Brushed Alpaca Silk</a><a href="kategorie.html">Sky</a><a href="kategorie.html">Melody</a>
      <a href="kategorie.html">Air</a><a href="kategorie.html">Flora</a><a href="kategorie.html">Soft Tweed</a>
      <a href="kategorie.html">Nepal</a><a href="kategorie.html">Alpaca</a><a href="kategorie.html">Andes</a>
    </div>
    <div class="mega__col">
      <p class="mega__h">Podle složení</p>
      <a href="kategorie.html">Alpaka</a><a href="kategorie.html">Merino a vlna</a><a href="kategorie.html">Moherové příze</a>
      <a href="kategorie.html">Bavlna</a><a href="kategorie.html">Akryl a směsi</a>
    </div>
    <div class="mega__col">
      <p class="mega__h">Další značky</p>
      <a href="kategorie.html">Alize</a><a href="kategorie.html">YarnArt</a><a href="kategorie.html">Himalaya</a>
      <a href="kategorie.html">Vlna Hep</a><a href="kategorie.html">Pletánky</a>
    </div>
    <a class="mega__promo" href="kategorie.html">
      <img src="img/photo/moher.jpg" alt="">
      <span><small>Akce</small>Příze DROPS až −30&nbsp;%</span>
    </a>
  </div>
</div>'''


def header(active=""):
    links = ""
    for name, href, mega in NAV:
        cls = "nav__a" + (" is-active" if name == active else "")
        if mega:
            links += f'<li class="nav__li has-mega"><a class="{cls}" href="{href}">{name}{ico("down","ico ico--xs")}</a>{MEGA}</li>'
        else:
            links += f'<li class="nav__li"><a class="{cls}" href="{href}">{name}</a></li>'
    links += '<li class="nav__li"><a class="nav__a nav__a--akce" href="kategorie.html">Akce a výprodej</a></li>'
    return f'''<a class="skip" href="#obsah">Přejít na obsah</a>
<div class="topbar">
  <div class="wrap topbar__in">
    <span class="topbar__ship">{ico("truck","ico ico--sm")} Doprava zdarma od 2&nbsp;000&nbsp;Kč</span>
    <span class="topbar__mid">Příze DROPS v akci až −30&nbsp;%</span>
    <span class="topbar__links"><a href="#">info@pletanky.cz</a><a href="#">Doprava a platby</a><a href="#">CZK / EUR</a></span>
  </div>
</div>
<header class="hdr" id="hdr">
  <div class="wrap hdr__in">
    <button class="hdr__burger" type="button" aria-label="Menu" data-menu-open>{ico("menu")}</button>
    <a class="logo" href="index.html" aria-label="Pletánky – úvod">
      <span class="logo__mark" aria-hidden="true"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="15" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 15c8 0 17 5 21 15M7 21c7 0 14 3.5 17 10M13 7.5c6 2.5 13 9 15.5 17M20 5c4.5 3 8 7.5 10 12.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M33 31c3 1.5 5 .5 5.5-1" fill="none" stroke="#c6a15b" stroke-width="1.6" stroke-linecap="round"/></svg></span>
      <span class="logo__txt">Pletánky<small>příze &amp; tvoření</small></span>
    </a>
    <form class="search" role="search" onsubmit="return false">
      {ico("search","ico ico--sm")}
      <input type="search" placeholder="Hledat přízi, barvu nebo značku…" aria-label="Hledat">
      <span class="search__hint">např. <em>alpaka švestka</em></span>
    </form>
    <nav class="hdr__acts" aria-label="Účet a košík">
      <a class="hdr__act" href="#">{ico("user")}<span>Přihlásit</span></a>
      <button class="cartbtn" type="button" data-cart-open aria-label="Košík">
        <span class="cartbtn__ico">{ico("bag")}<b class="cartbtn__count" data-cart-count>0</b></span>
        <span class="cartbtn__txt"><small>Košík</small><b data-cart-total>0&nbsp;Kč</b></span>
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
    <nav class="mmenu">{items}<a class="mmenu__akce" href="kategorie.html">Akce a výprodej{ico("chev","ico ico--sm")}</a></nav>
    <div class="mmenu__foot"><a href="#">{ico("user","ico ico--sm")} Přihlášení</a><a href="#">{ico("mail","ico ico--sm")} info@pletanky.cz</a></div>
  </div>
</div>'''


def cart_drawer():
    return f'''<div class="drawer drawer--cart" data-cart aria-hidden="true">
  <div class="drawer__panel">
    <div class="drawer__head"><b>Váš košík</b><button type="button" data-cart-close aria-label="Zavřít">{ico("close")}</button></div>
    <div class="freeship"><p data-free-txt>Do dopravy zdarma zbývá <b>2&nbsp;000&nbsp;Kč</b></p><span class="freeship__bar"><i data-free-bar></i></span></div>
    <ul class="cartlist" data-cart-list><li class="cartlist__empty">Košík je zatím prázdný. Přidejte si první klubíčko 🧶</li></ul>
    <div class="drawer__foot">
      <p class="cartsum"><span>Celkem</span><b data-cart-total>0&nbsp;Kč</b></p>
      <a class="btn btn--plum btn--full" href="#">Pokračovat k objednávce <span class="btn__ico">{ico("arrow","ico ico--sm")}</span></a>
      <button class="btn btn--ghost btn--full" type="button" data-cart-close>Nakupovat dál</button>
    </div>
  </div>
</div>
<div class="toast" data-toast role="status" aria-live="polite"></div>'''


def about_panel():
    return f'''<button class="aboutbtn" type="button" data-about-open>{ico("info","ico ico--sm")} O ukázce</button>
<div class="drawer drawer--about" data-about aria-hidden="true">
  <div class="drawer__panel">
    <div class="drawer__head"><b>Nezávazná ukázka vzhledu</b><button type="button" data-about-close aria-label="Zavřít">{ico("close")}</button></div>
    <div class="about">
      <p>Ukázka pro <b>Pletánky.cz</b> od Studentských Webů. Je to klikací návrh vzhledu: úvodní strana, kategorie a detail produktu, na počítači i na mobilu.</p>
      <ul>
        <li>Názvy, ceny, dostupnost a fotky produktů jsou převzaté z pletanky.cz (stav 7.&nbsp;10.&nbsp;2026). Ilustrační fotky jsou volně licencované, nahradí je Vaše vlastní.</li>
        <li>Logo je zatím jen zástupné. Nové logo a barvy vizuální identity do návrhu doplníme.</li>
        <li>Všechno stavíme na Shoptetu (tarif Enterprise): vlastní šablona a CSS, megamenu, filtry podle parametrů, bannery, blog a napojení Instagramu. Objednávky, zboží i zákaznické účty zůstanou, kde jsou.</li>
        <li>Odkazy vedou jen mezi třemi ukázkovými stránkami, košík funguje jen naoko.</li>
      </ul>
      <p class="about__nav"><a href="index.html">Úvod</a><a href="kategorie.html">Kategorie</a><a href="produkt.html">Detail produktu</a></p>
    </div>
  </div>
</div>'''


def footer():
    return f'''<footer class="ftr">
  <div class="wrap ftr__grid">
    <div class="ftr__brand">
      <span class="logo__txt logo__txt--light">Pletánky<small>příze &amp; tvoření</small></span>
      <p>Příze na pletení a háčkování, macramé šňůry, korálky a všechno pro tvoření.</p>
      <p class="ftr__soc"><a href="#" aria-label="Instagram">{ico("ig")}</a><a href="#" aria-label="Facebook">{ico("fb")}</a></p>
    </div>
    <div><p class="ftr__h">Sortiment</p><a href="kategorie.html">Příze na pletení</a><a href="kategorie.html">Háčkovací příze</a><a href="kategorie.html">Špagáty a macramé</a><a href="kategorie.html">Korálky a kameny</a><a href="kategorie.html">Dárkové poukazy</a></div>
    <div><p class="ftr__h">Nakupování</p><a href="#">Doprava a platby</a><a href="#">Obchodní podmínky</a><a href="#">Ochrana osobních údajů</a><a href="#">Hodnocení obchodu</a></div>
    <div><p class="ftr__h">Kontakt</p><a href="#">{ico("mail","ico ico--sm")} info@pletanky.cz</a><a href="#">Kontakty</a><a href="#">Slevy</a></div>
  </div>
  <div class="wrap ftr__bottom"><span>© Pletánky.cz</span><span>Nezávazná ukázka vzhledu · Studentské Weby</span></div>
</footer>'''


def page(title, body, active="", cls="", desc="Nezávazná ukázka vzhledu e-shopu Pletánky.cz"):
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,50;1,9..144,300..700,50&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap&subset=latin-ext" rel="stylesheet">
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
{about_panel()}
</body>
</html>
'''


# ================= ÚVOD =================
TILES = [
    ("Příze na pletení", "Alpaka, merino, moher i bavlna", "img/photo/moher.jpg", "yarn", "t--big"),
    ("Háčkovací příze", "Kordonety, Moonlight, Sněhurka", "img/photo/kordonet.jpg", "hook", ""),
    ("Špagáty a macramé", "Šňůry, cordy, Twisted macrame", "img/photo/macrame-snura.jpg", "knot", ""),
    ("Pomůcky", "Jehlice, háčky, značky na očka", "img/photo/jehlice.jpg", "needles", "t--tall"),
    ("Korálky", "Ohňovky, mačkané, dřevěné", "img/photo/koralky.jpg", "bead", ""),
    ("Kameny a minerály", "Achát, ametyst a další", "img/photo/kameny.jpg", "gem", ""),
    ("Bižuterní komponenty", "Kaplíky, kaloty, zapínání", "img/photo/komponenty.jpg", "clasp", ""),
]


def tiles():
    out = ""
    for name, sub, img, ic, cls in TILES:
        out += f'''<a class="tile {cls} reveal" href="kategorie.html">
  <img src="{img}" alt="" loading="lazy">
  <span class="tile__pic">{ico(ic)}</span>
  <span class="tile__txt"><b>{name}</b><small>{sub}</small></span>
  <span class="tile__go">{ico("arrow","ico ico--sm")}</span>
</a>'''
    out += f'''<a class="tile tile--gift reveal" href="kategorie.html">
  <span class="tile__pic">{ico("gift")}</span>
  <span class="tile__txt"><b>Dárkové poukazy</b><small>Pro všechny, kdo rádi tvoří</small></span>
  <span class="tile__go">{ico("arrow","ico ico--sm")}</span>
</a>'''
    return out


PROJ = [("sweater", "Svetry a kardigany"), ("hat", "Čepice a šály"), ("sock", "Ponožky"), ("blanket", "Deky a pledy"),
        ("toy", "Amigurumi a hračky"), ("home", "Macramé do bytu"), ("ring", "Šperky a bižuterie")]
COMP = ["Alpaka", "Merino", "Moher", "Bavlna", "Hedvábí", "Akryl a směsi"]
WEIGHT = [("A", "jemné"), ("B", "slabší"), ("C", "střední"), ("D", "silnější"), ("E", "silné"), ("F", "velmi silné")]


def projects():
    p = "".join(f'<a class="proj reveal" href="kategorie.html"><span class="proj__ico">{ico(i)}</span><span>{n}</span></a>' for i, n in PROJ)
    c = "".join(f'<a class="chip" href="kategorie.html">{n}</a>' for n in COMP)
    w = "".join(f'<a class="chip chip--w" href="kategorie.html"><b>{g}</b>{t}</a>' for g, t in WEIGHT)
    return f'''<section class="sec sec--blush">
  <div class="wrap">
    <div class="sechead reveal">
      <span class="eyebrow">Na co se chystáte?</span>
      <h2 class="h2">Vyberte podle <em>projektu</em></h2>
      <p class="sechead__p">Nové rozčlenění sortimentu: zákaznice najde přízi podle toho, co chce tvořit, z čeho a jak silnou. Jeden produkt může být ve více kategoriích najednou.</p>
    </div>
    <div class="projs">{p}</div>
    <div class="chiprows reveal">
      <div class="chiprow"><span class="chiprow__l">Podle složení</span>{c}</div>
      <div class="chiprow"><span class="chiprow__l">Podle síly (skupiny DROPS)</span>{w}</div>
    </div>
  </div>
</section>'''


def rail(title_html, eyebrow, items, more="Zobrazit vše", sec_cls="sec"):
    cards = "".join(card(p) for p in items)
    return f'''<section class="{sec_cls}">
  <div class="wrap">
    <div class="sechead sechead--row reveal">
      <div><span class="eyebrow">{eyebrow}</span><h2 class="h2">{title_html}</h2></div>
      <div class="rail__ctrl"><a class="link" href="kategorie.html">{more} {ico("arrow","ico ico--sm")}</a>
        <button class="rail__btn" type="button" data-rail-prev aria-label="Předchozí">{ico("chev","ico ico--sm ico--flip")}</button>
        <button class="rail__btn" type="button" data-rail-next aria-label="Další">{ico("chev","ico ico--sm")}</button></div>
    </div>
    <div class="rail" data-rail>{cards}</div>
  </div>
</section>'''


IG = ["ig26", "ig18", "ig19", "ig25", "ig28", "ig23", "ig31", "ig29"]


def instagram():
    imgs = "".join(f'<a class="ig__i" href="#"><img src="img/ig/{i}.jpg" alt="Příspěvek @pletanky" loading="lazy"><span>{ico("ig")}</span></a>' for i in IG)
    return f'''<section class="sec sec--ig">
  <div class="wrap sechead sechead--center reveal">
    <span class="eyebrow">{ico("ig","ico ico--xs")} @pletanky</span>
    <h2 class="h2">Co se u nás <em>právě tvoří</em></h2>
    <p class="sechead__p">Pás z Instagramu se načítá automaticky přes napojení v Shoptetu.</p>
  </div>
  <div class="ig" data-marquee><div class="ig__track">{imgs}{imgs}</div></div>
</section>'''


BRANDS = ["DROPS", "Alize", "YarnArt", "Himalaya", "Addi", "Prym", "Pony", "Premax", "Vlna Hep"]

home_body = f'''
<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__txt">
      <span class="eyebrow eyebrow--gold">Příze · macramé · korálky</span>
      <h1 class="h1" data-split>Každý projekt začíná <em>jedním klubkem</em></h1>
      <p class="hero__p">Příze DROPS, Alize a YarnArt, šňůry na macramé, korálky, kameny a všechno, co k tvoření potřebujete. Vyberte si barvu, která Vám udělá radost.</p>
      <div class="hero__cta">
        <a class="btn btn--plum" href="kategorie.html">Vybrat přízi <span class="btn__ico">{ico("arrow","ico ico--sm")}</span></a>
        <a class="btn btn--ghost" href="kategorie.html">Akce DROPS až −30&nbsp;%</a>
      </div>
      <ul class="hero__usp">
        <li>{ico("truck","ico ico--sm")} Doprava zdarma od 2&nbsp;000&nbsp;Kč</li>
        <li>{ico("yarn","ico ico--sm")} Desítky odstínů od každé příze</li>
      </ul>
    </div>
    <div class="hero__art">
      <svg class="hero__ring" viewBox="0 0 400 400" aria-hidden="true"><circle cx="200" cy="200" r="190"/><circle cx="200" cy="200" r="182"/></svg>
      <div class="hero__arch"><img src="img/photo/hero-klubka.jpg" alt="Klubíčka příze v teplých odstínech" fetchpriority="high"></div>
      <a class="hero__float" href="produkt.html">
        <img src="img/p/prize-drops-brushed-alpaca-silk-44-svestka.jpg" alt="">
        <span><small>Odstín měsíce</small><b>Brushed Alpaca Silk 44 – švestka</b><em><s>81 Kč</s> 57 Kč</em></span>
      </a>
      <svg class="hero__sprig" viewBox="0 0 120 200" aria-hidden="true"><path d="M60 195C58 140 50 90 30 20" fill="none" stroke="#6b3560" stroke-width="1.6"/><g fill="#8a5a86"><circle cx="30" cy="20" r="6"/><circle cx="44" cy="44" r="5"/><circle cx="22" cy="58" r="5.5"/><circle cx="50" cy="80" r="5"/><circle cx="30" cy="96" r="6"/><circle cx="57" cy="118" r="4.5"/><circle cx="40" cy="135" r="5.5"/></g></svg>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true"><div class="strip__track">
  {"".join(f"<span>{t}</span><i>✦</i>" for t in ["Příze DROPS", "Alize", "YarnArt", "Macramé šňůry", "Korálky a kameny", "Bižuterní komponenty", "Dárkové poukazy"]*2)}
</div></div>

<section class="sec">
  <div class="wrap">
    <div class="sechead sechead--row reveal">
      <div><span class="eyebrow">Oblíbené kategorie</span><h2 class="h2">Do čeho se <em>pustíte</em> dnes?</h2></div>
      <a class="link" href="kategorie.html">Všechny kategorie {ico("arrow","ico ico--sm")}</a>
    </div>
    <div class="tiles">{tiles()}</div>
  </div>
</section>

{rail('Akce na příze <em>DROPS</em>', "Až −30 %", P["akce"], "Celá akce")}

{projects()}

<section class="sec">
  <div class="wrap story">
    <div class="story__img reveal"><img src="img/photo/inspirace-svetr.jpg" alt="Rozpletený svetr, sešit a klubíčka" loading="lazy">
      <span class="story__badge">Inspirace<br>&amp; návody</span></div>
    <div class="story__txt">
      <span class="eyebrow reveal">Z blogu</span>
      <h2 class="h2 reveal">Nevíte, jak začít? <em>Poradíme.</em></h2>
      <p class="reveal">Návody, tipy na kombinace přízí a nápady na projekty. Z článku se dá rovnou proklik na přízi, ze které je výrobek upletený.</p>
      <div class="posts">
        <a class="post reveal" href="#"><img src="img/photo/ruce-pleteni.jpg" alt="" loading="lazy"><span><small>Pro začátečnice</small><b>Jak vybrat přízi na první svetr</b></span></a>
        <a class="post reveal" href="#"><img src="img/photo/macrame-snura.jpg" alt="" loading="lazy"><span><small>Macramé</small><b>První závěs krok za krokem</b></span></a>
        <a class="post reveal" href="#"><img src="img/photo/ruzova-klubka.jpg" alt="" loading="lazy"><span><small>Tip</small><b>Příplet z alpaky a hedvábí: jak na něj</b></span></a>
      </div>
      <p class="story__note reveal">Ukázkové články</p>
    </div>
  </div>
</section>

{rail('Novinky a <em>oblíbené</em>', "Pro háčkování, macramé i šperky", P["mix"], "Zobrazit vše", "sec sec--cream")}

<section class="brands">
  <div class="wrap brands__in reveal">
    <span class="eyebrow">Značky, které u nás najdete</span>
    <div class="brands__row">{"".join(f'<a href="kategorie.html">{b}</a>' for b in BRANDS)}</div>
  </div>
</section>

{instagram()}

<section class="news">
  <div class="wrap news__in">
    <div class="news__txt reveal">
      <span class="eyebrow eyebrow--gold">Newsletter</span>
      <h2 class="h2 h2--light">Akce a novinky <em>jako první</em></h2>
      <p>Nové odstíny, slevy na příze a tipy na projekty. Jednou za čas, nikdy otravně.</p>
    </div>
    <form class="news__form reveal" onsubmit="return false">
      <input type="email" placeholder="Váš e-mail" aria-label="E-mail">
      <button class="btn btn--gold" type="submit">Odebírat <span class="btn__ico">{ico("arrow","ico ico--sm")}</span></button>
    </form>
    <svg class="news__ring" viewBox="0 0 400 400" aria-hidden="true"><circle cx="200" cy="200" r="190"/><circle cx="200" cy="200" r="181"/></svg>
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
  <button class="btn btn--plum btn--full filters__apply" type="button" data-filters-close>Zobrazit 43 produktů</button>
</aside>'''


cat_cards = "".join(card(p) for p in P["cat"])
cat_body = f'''
<section class="chero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Domů</a><i>/</i><a href="kategorie.html">Příze na pletení a háčkování</a><i>/</i><a href="kategorie.html">Mohérové příze</a><i>/</i><span>DROPS Brushed Alpaca Silk</span></nav>
    <div class="chero__in">
      <div class="chero__txt">
        <span class="eyebrow">DROPS · 43 odstínů · akce −29 %</span>
        <h1 class="h1 h1--cat">DROPS Brushed <em>Alpaca Silk</em></h1>
        <p>Luxusní směs hebké česané alpaky a jemně lesklého hedvábí. Lehoučká a překvapivě hřejivá příze ve vytříbených odstínech, od něžných béžových a šedých tónů po červené a fialové. Skvělá i jako příplet.</p>
        <ul class="specs">
          <li><small>Složení</small><b>77 % alpaka, 23 % hedvábí</b></li>
          <li><small>Klubko</small><b>25 g / 140 m</b></li>
          <li><small>Jehlice</small><b>5 mm</b></li>
          <li><small>Skupina</small><b>C · aran / worsted</b></li>
        </ul>
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
        <button class="btn btn--ghost btn--sm ctool__filter" type="button" data-filters-open>{ico("filter","ico ico--sm")} Filtrovat</button>
        <div class="sort" role="tablist"><button class="is-on" type="button">Nejprodávanější</button><button type="button">Nejlevnější</button><button type="button">Nejdražší</button><button type="button">Abecedně</button></div>
        <span class="ctool__count">43 produktů</span>
      </div>
      <div class="grid">{cat_cards}</div>
      <div class="more"><p>Zobrazeno 12 ze 43</p><span class="more__bar"><i style="width:28%"></i></span><button class="btn btn--ghost" type="button">Načíst dalších 31</button></div>
    </div>
  </div>
</section>
'''

# ================= PRODUKT =================
sv = next(p for p in P["cat"] if "44 - švestka" in p["name"])
others = [p for p in P["cat"] if p is not sv]
swatches = "".join(f'<a class="pswatch{" is-on" if p is sv else ""}" href="produkt.html" title="{e(p["name"].split(" Silk ")[1])}"><img src="{p["file"]}" alt=""></a>' for p in [sv] + others)
tools = [p for p in P["mix"] if any(k in p["name"] for k in ["ponožkové", "Značky na očka", "Háček", "Interchangeable"])]
prod_body = f'''
<section class="pd">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Domů</a><i>/</i><a href="kategorie.html">Příze na pletení a háčkování</a><i>/</i><a href="kategorie.html">Mohérové příze</a><i>/</i><a href="kategorie.html">DROPS Brushed Alpaca Silk</a></nav>
    <div class="pd__in">
      <div class="pd__gal">
        <div class="pd__main"><span class="pcard__flags"><span class="flag flag--akce">Akce</span><span class="flag flag--sleva">–29 %</span></span><img src="img/p/svestka-velka.jpg" alt="Příze DROPS Brushed Alpaca Silk 44 – švestka"></div>
        <div class="pd__thumbs"><button class="is-on" type="button"><img src="img/p/svestka-velka.jpg" alt=""></button><span class="pd__ph">Vaše<br>fotka</span><span class="pd__ph">Vaše<br>fotka</span></div>
      </div>
      <div class="pd__info">
        <p class="pd__brand">DROPS · Kód 94580</p>
        <h1 class="h1 h1--pd">Příze DROPS Brushed Alpaca Silk <em>44 – švestka</em></h1>
        <p class="pd__lead">Přepychová směs počesané alpaky a morušového hedvábí. Lehoučká, hřejivá a krásně vzdušná.</p>
        <div class="pd__price"><b>57&nbsp;Kč</b><s>81&nbsp;Kč</s><span class="flag flag--sleva">–29 %</span><small>47,11 Kč bez DPH · za klubko 25 g</small></div>
        <p class="pd__av">{ico("check","ico ico--sm")} Skladem <span>(55 ks)</span></p>
        <div class="pd__swh"><p>Odstín: <b>44 – švestka</b> <span>· dalších 42 odstínů</span></p><div class="pswatches">{swatches}</div></div>
        <div class="pd__buy">
          <div class="qty"><button type="button" data-qty="-1" aria-label="Méně">{ico("minus","ico ico--sm")}</button><input type="number" value="1" min="1" aria-label="Množství" data-qty-input><button type="button" data-qty="1" aria-label="Více">{ico("plus","ico ico--sm")}</button></div>
          <button class="btn btn--plum btn--buy" type="button" data-add data-name="Příze DROPS Brushed Alpaca Silk 44 - švestka" data-price="57" data-img="img/p/prize-drops-brushed-alpaca-silk-44-svestka.jpg" data-qty-from>{ico("bag","ico ico--sm")} Přidat do košíku</button>
        </div>
        <ul class="pd__usp">
          <li>{ico("truck","ico ico--sm")} Doprava zdarma od 2&nbsp;000&nbsp;Kč</li>
          <li>{ico("mail","ico ico--sm")} Nevíte si rady s množstvím? Napište nám</li>
        </ul>
        <ul class="specs specs--pd">
          <li><small>Složení</small><b>77 % alpaka, 23 % hedvábí</b></li>
          <li><small>Klubko</small><b>25 g / cca 140 m</b></li>
          <li><small>Jehlice / háček</small><b>5 mm</b></li>
          <li><small>Vzorek 10×10 cm</small><b>17 ok × 24 řad</b></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap">
    <div class="tabs" data-tabs>
      <div class="tabs__nav" role="tablist"><button class="is-on" type="button" data-tab="0">Popis</button><button type="button" data-tab="1">Parametry</button><button type="button" data-tab="2">Hodnocení</button></div>
      <div class="tabs__panel is-on">
        <p>Příze je lehoučká a překvapivě hřejivá – je proto velmi vhodná na drobné i větší kousky a můžete ji plést na silnějších jehlicích, takže práce rychle přibývá. Přízi DROPS Brushed Alpaca Silk lze využít rovněž jako efektní příplet v kombinaci s jinou přízí, výsledný úplet pak získá nebývalou jemnost!</p>
        <p>Prát v ruce, max. 30 °C, sušit volně rozložené.</p>
      </div>
      <div class="tabs__panel"><table class="ptable"><tr><th>Kategorie</th><td>DROPS Brushed Alpaca Silk</td></tr><tr><th>Složení</th><td>77 % alpaka, 23 % hedvábí</td></tr><tr><th>Skupina přízí</th><td>C (16–19 ok) / 10 ply / aran / worsted</td></tr><tr><th>Hmotnost / návin</th><td>25 g / 140 m</td></tr><tr><th>Velikost jehlic</th><td>5</td></tr><tr><th>Velikost háčku</th><td>5</td></tr><tr><th>Barva</th><td>červená</td></tr></table></div>
      <div class="tabs__panel"><p class="muted">Produkt zatím nikdo nehodnotil. Buďte první!</p></div>
    </div>
  </div>
</section>

{rail('Ke klubku se <em>hodí</em>', "Pomůcky", tools, "Všechny pomůcky", "sec sec--cream")}
{rail('Další odstíny <em>Brushed Alpaca Silk</em>', "Stejná příze", others, "Celá kategorie")}
'''

(ROOT / "index.html").write_text(page("Pletánky.cz – příze, macramé a korálky | ukázka vzhledu", home_body))
(ROOT / "kategorie.html").write_text(page("DROPS Brushed Alpaca Silk – Pletánky.cz | ukázka vzhledu", cat_body, "Příze na pletení"))
(ROOT / "produkt.html").write_text(page("Příze DROPS Brushed Alpaca Silk 44 – švestka – Pletánky.cz | ukázka vzhledu", prod_body, "Příze na pletení", "page-pd"))
print("ok")
