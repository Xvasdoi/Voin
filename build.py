#!/usr/bin/env python3
"""Генерує сторінки сайту академії «Воїн» з даних у папці data/.

Запуск:  python3 build.py
Після зміни будь-якого файлу в data/ достатньо перезапустити скрипт.
"""
import json
import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
DATA = ROOT / "data"
SITE_URL = "https://xvasdoi.github.io/Voin/"

club = json.loads((DATA / "club.json").read_text("utf-8"))
coaches = json.loads((DATA / "coaches.json").read_text("utf-8"))
athletes = json.loads((DATA / "athletes.json").read_text("utf-8"))
news = json.loads((DATA / "news.json").read_text("utf-8"))
coach_by_id = {c["id"]: c for c in coaches}
hall_by_id = {h["id"]: h for h in club["halls"]}
YEAR = datetime.date.today().year
YEARS = YEAR - club["founded"]

# ------------------------------------------------------------------ іконки
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "telegram": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "viber": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9.5 9.5c.5 2 2 3.5 5 5"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "navigate": '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "menu": '<line x1="4" x2="20" y1="7" y2="7"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="17" y2="17"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "swords": '<polyline points="14.5 17.5 3 6 3 3 6 3 17.5 14.5"/><line x1="13" x2="19" y1="19" y2="13"/><line x1="16" x2="20" y1="16" y2="20"/><line x1="19" x2="21" y1="21" y2="19"/><polyline points="14.5 6.5 18 3 21 3 21 6 17.5 9.5"/><line x1="5" x2="9" y1="14" y2="18"/><line x1="7" x2="4" y1="17" y2="20"/><line x1="3" x2="5" y1="19" y2="21"/>',
    "grapple": '<path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1.33-6 4Z"/>',
    "shirt": '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>',
    "footprints": '<path d="M4 16v-2.38C4 11.5 2.97 10.5 3 8c.03-2.72 1.49-6 4.5-6C9.37 2 10 3.8 10 5.5c0 3.11-2 5.66-2 8.68V16a2 2 0 1 1-4 0Z"/><path d="M20 20v-2.38c0-2.12 1.03-3.12 1-5.62-.03-2.72-1.49-6-4.5-6C14.63 6 14 7.8 14 9.5c0 3.11 2 5.66 2 8.68V20a2 2 0 1 0 4 0Z"/><path d="M16 17h4"/><path d="M4 13h4"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
}
TIKTOK = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5c-1.42 0-2.6-1.16-2.6-2.6 0-1.72 1.66-3.01 3.37-2.48V9.66c-3.45-.46-6.47 2.22-6.47 5.64 0 3.33 2.76 5.7 5.69 5.7 3.14 0 5.69-2.55 5.69-5.7V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3s-1.88.09-3.24-1.48z"/></svg>'


def icon(name):
    if name == "tiktok":
        return TIKTOK
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + '</svg>')


e = escape

# ------------------------------------------------------------------ навігація
PAGES = [
    ("index.html", "Головна"),
    ("trenery.html", "Тренери"),
    ("gordist.html", "Гордість академії"),
    ("novyny.html", "Новини"),
    ("pro-akademiyu.html", "Про академію"),
    ("zapys.html", "Розклад і ціни"),
]
JOIN = "zapys.html#grupy"


def picture(src, fallback, alt, size=1000, eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source srcset="{e(src)}" type="image/webp">'
            f'<img src="{e(fallback)}" alt="{e(alt)}" width="{size}" height="{size}" {load}'
            f'{" class=" + chr(34) + cls + chr(34) if cls else ""}></picture>')


def social_links(cls="social"):
    s = club["social"]
    return (f'<div class="socials">'
            f'<a class="{cls}" href="{e(s["instagram"])}" target="_blank" rel="noopener">{icon("instagram")}Instagram</a>'
            f'<a class="{cls}" href="{e(s["tiktok"])}" target="_blank" rel="noopener">{icon("tiktok")}TikTok</a>'
            f'<a class="{cls}" href="{e(s["telegramChannel"])}" target="_blank" rel="noopener">{icon("telegram")}Telegram-канал</a>'
            f'</div>')


def contact_buttons(c, size=""):
    """Кнопки зв'язку з тренером."""
    ct = c["contacts"]
    sm = " btn--sm" if size == "sm" else ""
    first = True
    out = []

    def cls():
        nonlocal first
        k = "btn--primary" if first else "btn--ghost"
        first = False
        return k

    if ct.get("telegram"):
        out.append(f'<a class="btn {cls()}{sm}" href="{e(ct["telegram"])}" target="_blank" rel="noopener">{icon("telegram")}Telegram</a>')
    if ct.get("phone"):
        if ct.get("viber"):
            out.append(f'<a class="btn {cls()}{sm}" href="viber://chat?number=%2B{ct["phone"].lstrip("+")}">{icon("viber")}Viber</a>')
        out.append(f'<a class="btn {cls()}{sm}" href="tel:{e(ct["phone"])}">{icon("phone")}Подзвонити</a>')
    return '<div class="btn-row">' + "".join(out) + "</div>"


def achievements_list(items):
    return '<ul class="achievements">' + "".join(
        f'<li>{icon("trophy")}<span>{e(a)}</span></li>' for a in items) + "</ul>"


def coach_card(c, full=True):
    photo = picture(c["photo"], c["photoFallback"], c["name"])
    badge = f'<span class="person__badge">{e(c["role"])}</span>' if c.get("role") else ""
    tags = '<div class="tags">' + "".join(f'<span class="tag tag--accent">{e(d)}</span>' for d in c["disciplines"]) + "</div>"
    role = ""
    if c.get("type") == "duo":
        role = '<p class="person__role">Тренери дитячої групи</p>'
    elif c.get("role"):
        role = f'<p class="person__role">{e(c["role"])}</p>'
    if c.get("type") == "duo":
        body_ach = "".join(
            f'<div class="person__member"><h4>{e(m["name"])}</h4>{achievements_list(m["achievements"])}</div>'
            for m in c["members"]) if full else achievements_list([a for m in c["members"] for a in m["achievements"][:1]])
    else:
        body_ach = achievements_list(c["achievements"])
    halls = ", ".join(hall_by_id[h]["address"].split(", Луцьк")[0] for h in c.get("halls", []))
    meta = (f'<ul class="person__meta">'
            f'<li>{icon("users")}<span>{e(c.get("groups", ""))}</span></li>'
            + (f'<li>{icon("map-pin")}<span>{e(halls)}</span></li>' if halls else "")
            + "</ul>")
    notice = ""
    if c.get("experiencedOnly"):
        notice = f'<p class="notice">{icon("info")}<span>Група лише для досвідчених спортсменів. Новачкам радимо почати з інших груп.</span></p>'
    actions = (f'<div class="person__actions">{contact_buttons(c, "sm")}</div>' if full
               else f'<div class="person__actions"><a class="link-arrow" href="trenery.html#{c["id"]}">Детальніше та запис {icon("arrow")}</a></div>')
    return (f'<article class="person reveal" id="{c["id"]}">'
            f'<div class="person__photo">{photo}{badge}</div>'
            f'<div class="person__body">'
            f'<h3 class="person__name">{e(c["name"])}</h3>{role}{tags}'
            f'{body_ach}{meta if full else ""}{notice if full else ""}{actions}'
            f'</div></article>')


def athlete_card(a):
    photo = picture(a["photo"], a["photoFallback"], a["name"])
    tags = '<div class="tags">' + "".join(f'<span class="tag">{e(d)}</span>' for d in a["disciplines"]) + "</div>"
    return (f'<article class="person person--compact reveal" id="{a["id"]}">'
            f'<div class="person__photo">{photo}</div>'
            f'<div class="person__body"><h3 class="person__name">{e(a["name"])}</h3>{tags}'
            f'{achievements_list(a["achievements"])}</div></article>')


def schedule_table():
    rows = []
    for s in club["schedule"]:
        c = coach_by_id[s["coach"]]
        hall = hall_by_id[s["hall"]]["address"].split(", Луцьк")[0]
        rows.append(
            f'<tr><td>{e(s["days"])}</td><td><span class="time">{e(s["time"])}</span></td>'
            f'<td><div class="group-name">{e(s["group"])}</div><div class="group-coach">{e(c["name"])}</div></td>'
            f'<td class="muted">{e(hall)}</td></tr>')
    return ('<div class="table-wrap"><table class="schedule"><caption class="visually-hidden">Розклад тренувань</caption>'
            '<thead><tr><th scope="col">Дні</th><th scope="col">Час</th><th scope="col">Група і тренер</th><th scope="col">Зал</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table></div>')


def price_card():
    p = club["price"]
    return (f'<div class="price-card reveal"><span class="eyebrow">Абонемент</span>'
            f'<div class="price-card__value">{p["monthly"]}<small>{e(p["currency"])}/міс</small></div>'
            f'<ul><li>{icon("check")}Тренування за розкладом своєї групи</li>'
            f'<li>{icon("check")}Тренери — чемпіони світу та Європи</li>'
            f'<li>{icon("check")}Підготовка до змагань</li></ul>'
            f'<a class="btn btn--primary btn--block" href="{JOIN}">Записатись на тренування</a></div>')


def map_embed(h):
    q = quote(h["address"])
    return (f'<iframe src="https://maps.google.com/maps?q={q}&amp;z=16&amp;output=embed" '
            f'title="Карта: {e(h["address"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')


def hall_cards():
    out = []
    for h in club["halls"]:
        trainers = [c["name"] for c in coaches if h["id"] in c.get("halls", [])]
        who = (f'<p>Тренують: {e(", ".join(trainers))}</p>' if trainers
               else '<p>Розклад занять у цьому залі уточнюйте у тренерів.</p>')
        out.append(
            f'<article class="hall reveal"><div class="hall__map">{map_embed(h)}</div>'
            f'<div class="hall__body"><h3 class="h-sm">{e(h["title"])}</h3>'
            f'<p>{icon("map-pin") if False else ""}{e(h["address"])}</p>{who}'
            f'<div class="btn-row"><a class="btn btn--ghost btn--sm" href="{e(h["mapUrl"])}" target="_blank" rel="noopener">{icon("navigate")}Прокласти маршрут</a></div>'
            f'</div></article>')
    return '<div class="grid grid--2">' + "".join(out) + "</div>"


def news_card(n):
    if n.get("photos"):
        media = f'<img src="{e(n["photos"][0])}" alt="{e(n["title"])}" loading="lazy">'
        gallery = ('<div class="news-gallery">' + "".join(
            f'<a href="{e(p)}" target="_blank" rel="noopener"><img src="{e(p)}" alt="{e(n["title"])}, фото {i + 1}" loading="lazy"></a>'
            for i, p in enumerate(n["photos"][1:])) + "</div>") if len(n["photos"]) > 1 else ""
    else:
        media = ('<div class="news-card__placeholder"><div><img src="assets/img/logo.png" alt="" width="96" height="96" loading="lazy">'
                 '<p>Фото незабаром</p></div></div>')
        gallery = ""
    date = f'<span class="tag">{icon("calendar")}{e(n["date"])}</span>' if n.get("date") else ""
    paras = "".join(f"<p>{e(t)}</p>" for t in n["text"])
    return (f'<article class="news-card reveal" id="{n["id"]}"><div class="news-card__media">{media}</div>'
            f'<div class="news-card__body">{date}<h3 class="h-md">{e(n["title"])}</h3>{paras}{gallery}</div></article>')


def groups_cards():
    misiuk = coach_by_id["andrii-misiuk"]
    duo = coach_by_id["tetiana-astakhova-ivan-poremchuk"]
    zin = coach_by_id["andrii-zinchuk"]
    groups = [
        ("smile", "Діти до 13 років", duo, "Грепплінг та ММА в ігровій і безпечній формі. Пн, Ср, Пт о 17:00.",
         "Найкращий старт для дитини: координація, сила, дисципліна і впевненість у собі."),
        ("target", "Новачки та всі рівні", misiuk, "ММА для дітей і дорослих, з нуля або з досвідом. Розклад уточнюйте у тренера.",
         "Підходить, якщо ви ніколи не займалися єдиноборствами."),
        ("flame", "Досвідчені спортсмени", zin, "Група головного тренера. Пн, Ср, Пт та Вт, Чт о 18:30.",
         "Лише для досвідчених спортсменів: підготовка до змагань."),
    ]
    out = []
    for ic, title, c, sched, hint in groups:
        out.append(
            f'<article class="card reveal"><div class="card__icon">{icon(ic)}</div>'
            f'<h3 class="h-md">{e(title)}</h3>'
            f'<p><strong style="color:var(--text)">{e(c["name"])}</strong></p>'
            f'<p>{e(sched)}</p><p>{e(hint)}</p>'
            f'<div class="card__foot">{contact_buttons(c, "sm")}</div></article>')
    return '<div class="grid grid--3">' + "".join(out) + "</div>"


def first_training_list():
    icons = ["shirt", "footprints", "shield", "droplet"]
    ft = club["firstTraining"]
    items = "".join(
        f'<li class="reveal"><span class="checklist__icon">{icon(icons[i % 4])}</span>'
        f'<div><h3>{e(it["title"])}</h3><p>{e(it["text"])}</p></div></li>'
        for i, it in enumerate(ft["items"]))
    return f'<p class="lead" style="margin-bottom:28px">{e(ft["intro"])}</p><ul class="checklist">{items}</ul>'


def cta_block():
    return (f'<div class="cta reveal"><div><h2 class="h-lg">Прийди на перше тренування</h2>'
            f'<p>Обери свою групу, напиши або зателефонуй тренеру — і ми чекаємо тебе в залі на Карбишева, 1.</p></div>'
            f'<div class="btn-row"><a class="btn btn--light" href="{JOIN}">Обрати групу {icon("arrow")}</a></div></div>')


# ------------------------------------------------------------------ каркас сторінки
def layout(page, title, description, body):
    nav = "".join(
        f'<li><a class="nav__link" href="{href}"{" aria-current=" + chr(34) + "page" + chr(34) if href == page else ""}>{e(label)}</a></li>'
        for href, label in PAGES)
    full_title = f"{title} — Академія ММА «Воїн», Луцьк" if page != "index.html" else "Академія ММА «Воїн» — змішані єдиноборства в Луцьку"
    hall = hall_by_id["karbysheva"]
    zin = coach_by_id["andrii-zinchuk"]["contacts"]
    mis = coach_by_id["andrii-misiuk"]["contacts"]
    footer_nav = "".join(f'<li><a href="{h}">{e(l)}</a></li>' for h, l in PAGES)
    ld = {
        "@context": "https://schema.org", "@type": "SportsClub",
        "name": club["fullName"], "url": SITE_URL, "logo": SITE_URL + "assets/img/logo.png",
        "foundingDate": str(club["founded"]),
        "address": [{"@type": "PostalAddress", "streetAddress": h["address"].split(", Луцьк")[0],
                     "addressLocality": "Луцьк", "addressRegion": "Волинська область",
                     "postalCode": "43000", "addressCountry": "UA"} for h in club["halls"]],
        "telephone": zin["phone"],
        "sameAs": list(club["social"].values()),
    }
    return f'''<!doctype html>
<html lang="uk" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#0a0a0b">
<link rel="canonical" href="{SITE_URL}{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:locale" content="uk_UA">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE_URL}assets/img/icon-512.png">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sofia+Sans+Extra+Condensed:wght@800;900&family=Sofia+Sans:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v={BUILD_ID}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">Перейти до змісту</a>
<header class="header">
  <div class="container header__inner">
    <a class="brand" href="index.html" aria-label="Академія ММА «Воїн» — на головну">
      <img src="assets/img/logo.png" alt="" width="46" height="46">
      <span><span class="brand__name">Воїн</span><span class="brand__sub">Академія ММА · Луцьк</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Головне меню">
      <ul class="nav__list">{nav}</ul>
      <div class="nav__extra">
        <a class="btn btn--primary btn--block" href="{JOIN}">Записатись на тренування</a>
        {social_links()}
      </div>
    </nav>
    <a class="btn btn--primary btn--sm header__cta" href="{JOIN}">Записатись</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Відкрити меню">
      <span class="icon-open">{icon("menu")}</span><span class="icon-close">{icon("close")}</span>
    </button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/logo.png" alt="" width="46" height="46"><span><span class="brand__name">Воїн</span><span class="brand__sub">Академія ММА · Луцьк</span></span></a>
        <p style="margin-top:16px">{e(club["fullName"])}. Працюємо з {club["founded"]} року.</p>
        {social_links()}
      </div>
      <div><h3>Розділи</h3><ul>{footer_nav}</ul></div>
      <div><h3>Зали</h3>
        {"".join(f'<p><a href="{e(h["mapUrl"])}" target="_blank" rel="noopener">{icon("map-pin")}{e(h["address"].split(", Луцьк")[0])}</a></p>' for h in club["halls"])}
        <p>Луцьк, Волинська область</p>
      </div>
      <div><h3>Запис</h3>
        <p>Андрій Зінчук<br><a href="tel:{zin["phone"]}">{e(zin["phoneDisplay"])}</a></p>
        <p>Андрій Місюк<br><a href="tel:{mis["phone"]}">{e(mis["phoneDisplay"])}</a></p>
        <p>Дитяча група<br><a href="{e(coach_by_id["tetiana-astakhova-ivan-poremchuk"]["contacts"]["telegram"])}" target="_blank" rel="noopener">Telegram Тетяни</a></p>
      </div>
    </div>
    <div class="footer__bottom"><span>© {YEAR} Академія ММА «Воїн». Усі права захищено.</span><span>Луцьк · з {club["founded"]} року</span></div>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn btn--primary" href="{JOIN}">Записатись</a>
  <a class="btn btn--ghost" href="tel:{mis["phone"]}" aria-label="Подзвонити">{icon("phone")}Дзвінок</a>
</div>
<script src="assets/js/main.js?v={BUILD_ID}" defer></script>
</body>
</html>
'''


BUILD_ID = datetime.datetime.now().strftime("%Y%m%d%H%M")


# ------------------------------------------------------------------ сторінки
def page_home():
    coach_cards = "".join(coach_card(c, full=False) for c in coaches)
    ath = "".join(athlete_card(a) for a in athletes[:4])
    latest = news_card(news[0]) if news else ""
    body = f'''
<section class="hero">
  <div class="container">
    <div class="hero__grid">
      <div>
        <p class="eyebrow">Луцьк · з {club["founded"]} року</p>
        <h1 class="h-xl hero__title">Академія ММА <span class="accent">«Воїн»</span></h1>
        <p class="lead">Змішані єдиноборства та грепплінг для дітей і дорослих. Тренери — чемпіони світу та Європи, заслужений тренер України.</p>
        <div class="btn-row">
          <a class="btn btn--primary" href="{JOIN}">Записатись на тренування {icon("arrow")}</a>
          <a class="btn btn--ghost" href="zapys.html#rozklad">{icon("clock")}Розклад і ціни</a>
        </div>
      </div>
      <div class="hero__emblem"><img src="assets/img/logo.png" alt="Емблема академії ММА «Воїн»" width="800" height="800" fetchpriority="high"></div>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat__value">{YEARS}<small>років</small></div><div class="stat__label">готуємо чемпіонів</div></div>
      <div class="stat"><div class="stat__value">{sum(len(c.get("members", [None])) for c in coaches)}</div><div class="stat__label">тренери-чемпіони</div></div>
      <div class="stat"><div class="stat__value">{len(club["halls"])}</div><div class="stat__label">зали в Луцьку</div></div>
      <div class="stat"><div class="stat__value">{club["price"]["monthly"]}<small>грн</small></div><div class="stat__label">абонемент на місяць</div></div>
    </div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="napriamy">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Напрями</p><h2 class="h-lg" id="napriamy">Чого ми навчаємо</h2></div></div>
    <div class="grid grid--2">
      <article class="card reveal"><div class="card__icon">{icon("swords")}</div><h3 class="h-md">ММА</h3>
        <p>Змішані єдиноборства: ударна техніка, боротьба в стійці та в партері. Найповніша система підготовки бійця — від загальної фізичної форми до виступів на змаганнях.</p>
        <div class="tags"><span class="tag">Діти</span><span class="tag">Дорослі</span><span class="tag">Новачки</span><span class="tag">Спортсмени</span></div></article>
      <article class="card reveal"><div class="card__icon">{icon("grapple")}</div><h3 class="h-md">Грепплінг</h3>
        <p>Боротьба без ударів: кидки, контроль, больові та задушливі прийоми. Безпечний старт для дітей, що розвиває силу, гнучкість і мислення.</p>
        <div class="tags"><span class="tag">Діти до 13 років</span><span class="tag">Змагання</span></div></article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="treneri">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Команда</p><h2 class="h-lg" id="treneri">Наші тренери</h2>
      <p class="lead">Чемпіони світу та Європи, які самі виходили в клітку і знають шлях до перемоги.</p></div>
      <a class="link-arrow" href="trenery.html">Усі тренери {icon("arrow")}</a></div>
    <div class="grid grid--3">{coach_cards}</div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="gordist">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Гордість академії</p><h2 class="h-lg" id="gordist">Наші чемпіони</h2>
      <p class="lead">Вихованці академії, які представляють Луцьк та Україну на національних і міжнародних аренах.</p></div>
      <a class="link-arrow" href="gordist.html">Усі спортсмени {icon("arrow")}</a></div>
    <div class="grid grid--4">{ath}</div>
  </div>
</section>

<section class="section" aria-labelledby="rozklad-home">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Розклад</p><h2 class="h-lg" id="rozklad-home">Коли тренуємось</h2>
      <p class="lead">Зал на вул. Карбишева, 1. Розклад групи Андрія Місюка уточнюйте у тренера.</p></div></div>
    <div class="grid" style="grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);align-items:start" data-split>
      <div class="reveal">{schedule_table()}</div>
      {price_card()}
    </div>
  </div>
</section>

<section class="section section--surface" aria-labelledby="novyny-home">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Новини</p><h2 class="h-lg" id="novyny-home">Життя клубу</h2></div>
      <a class="link-arrow" href="novyny.html">Усі новини {icon("arrow")}</a></div>
    {latest}
  </div>
</section>

<section class="section" aria-label="Запис">
  <div class="container">{cta_block()}</div>
</section>
'''
    return layout("index.html", "Головна",
                  f"Академія змішаних єдиноборств ММА «Воїн» у Луцьку з {club['founded']} року. ММА та грепплінг для дітей і дорослих, тренери — чемпіони світу та Європи. Абонемент {club['price']['monthly']} грн/міс.",
                  body)


def page_hero(crumb, eyebrow, title, lead):
    return f'''<section class="page-hero"><div class="container">
<p class="breadcrumbs"><a href="index.html">Головна</a> / {e(crumb)}</p>
<p class="eyebrow">{e(eyebrow)}</p><h1 class="h-xl">{e(title)}</h1>
<p class="lead">{e(lead)}</p></div></section>'''


def page_coaches():
    cards = "".join(coach_card(c) for c in coaches)
    body = page_hero("Тренери", "Команда", "Тренери",
                     "Оберіть тренера та запишіться напряму: Telegram, Viber або дзвінок.") + f'''
<section class="section"><div class="container"><div class="grid grid--3">{cards}</div></div></section>
<section class="section section--surface"><div class="container">{cta_block()}</div></section>'''
    return layout("trenery.html", "Тренери",
                  "Тренери академії ММА «Воїн» у Луцьку: Андрій Зінчук, Андрій Місюк, Тетяна Астахова та Іван Поремчук. Досягнення, групи та контакти для запису.",
                  body)


def page_pride():
    cards = "".join(athlete_card(a) for a in athletes)
    body = page_hero("Гордість академії", "Наші чемпіони", "Гордість академії",
                     "Спортсмени «Воїна», які приносять медалі Луцьку та Україні. Кожна перемога — результат дисципліни, характеру й щоденної праці.") + f'''
<section class="section"><div class="container"><div class="grid grid--4">{cards}</div></div></section>
<section class="section section--surface"><div class="container">{cta_block()}</div></section>'''
    return layout("gordist.html", "Гордість академії",
                  "Чемпіони академії ММА «Воїн»: чемпіони світу, Європи та України з ММА, грепплінгу, панкратіону та козацького двобою.",
                  body)


def page_news():
    cards = "".join(news_card(n) for n in news)
    body = page_hero("Новини", "Життя клубу", "Новини",
                     "Змагання, перемоги та події академії. Більше новин — у нашому Instagram і Telegram-каналі.") + f'''
<section class="section"><div class="container"><div class="grid">{cards}</div>
<div style="margin-top:40px"><p class="muted">Слідкуйте за нами в соцмережах:</p>{social_links()}</div></div></section>'''
    return layout("novyny.html", "Новини", "Новини академії ММА «Воїн»: змагання, перемоги спортсменів та події клубу.", body)


def page_about():
    zin = coach_by_id["andrii-zinchuk"]
    values = "".join(
        f'<div class="value reveal"><span class="value__num">0{i + 1}</span><h3 class="h-md">{e(v["title"])}</h3><p>{e(v["text"])}</p></div>'
        for i, v in enumerate(club["values"]))
    body = page_hero("Про академію", f"З {club['founded']} року", "Про академію",
                     "Простір, де гартується сила духу, залізна дисципліна та прагнення до перемоги.") + f'''
<section class="section"><div class="container about-intro">
  <p class="quote reveal">Сила духу. <span>Дисципліна.</span> Перемога.</p>
  <div class="about-intro__text reveal"><p>{e(club["about"])}</p></div>
</div></section>

<section class="section section--surface" aria-labelledby="founder"><div class="container founder">
  <div class="founder__photo reveal">{picture(zin["photo"], zin["photoFallback"], zin["name"])}</div>
  <div class="reveal"><p class="eyebrow">Засновник</p><h2 class="h-lg" id="founder">{e(club["founder"])}</h2>
    <p class="lead" style="margin-top:20px">Заснував академію «Воїн» у {club["founded"]} році. Заслужений тренер України, тренер національної збірної України з ММА серед дорослих. Головний тренер академії.</p>
    <a class="link-arrow" href="trenery.html#andrii-zinchuk">Про тренера {icon("arrow")}</a></div>
</div></section>

<section class="section" aria-labelledby="values"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Цінності</p><h2 class="h-lg" id="values">Наші головні цінності</h2></div></div>
  <div class="values">{values}</div>
</div></section>

<section class="section section--surface" aria-labelledby="zaly"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Де ми</p><h2 class="h-lg" id="zaly">Наші зали</h2></div></div>
  {hall_cards()}
</div></section>

<section class="section"><div class="container">{cta_block()}</div></section>'''
    return layout("pro-akademiyu.html", "Про академію",
                  f"Академія змішаних єдиноборств ММА «Воїн» заснована у {club['founded']} році Андрієм Зінчуком. Наші цінності, історія та зали в Луцьку.",
                  body)


def page_join():
    faq = [
        ("З якого віку можна займатися?", "Для дітей до 13 років є окрема група з грепплінгу та ММА (Тетяна Астахова та Іван Поремчук). Андрій Місюк тренує всі вікові групи. Точний вік, з якого приймають дитину, уточнюйте у тренера."),
        ("Я ніколи не займався. Можна прийти?", "Так. Новачкам радимо групу Андрія Місюка (всі рівні) або дитячу групу. Група Андрія Зінчука — лише для досвідчених спортсменів."),
        ("Скільки коштує?", f"Абонемент на місяць — {club['price']['monthly']} грн."),
        ("Де проходять тренування?", "Зал на вул. Карбишева, 1, Луцьк. Також у академії є зал на вул. Львівській, 75 — розклад занять там уточнюйте у тренерів."),
    ]
    faq_html = "".join(
        f'<details><summary>{e(q)}{icon("plus")}</summary><div class="faq__a"><p>{e(a)}</p></div></details>'
        for q, a in faq)
    body = page_hero("Розклад і ціни", "Запис", "Запис на тренування",
                     "Три кроки: оберіть групу, напишіть тренеру, приходьте на перше тренування.") + f'''
<section class="section" id="grupy" aria-labelledby="grupy-h"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Крок 1</p><h2 class="h-lg" id="grupy-h">Оберіть групу</h2>
    <p class="lead">Натисніть кнопку — і ви одразу напишете або зателефонуєте тренеру.</p></div></div>
  {groups_cards()}
</div></section>

<section class="section section--surface" id="rozklad" aria-labelledby="rozklad-h"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Крок 2</p><h2 class="h-lg" id="rozklad-h">Розклад і ціни</h2>
    <p class="lead">Зал на вул. Карбишева, 1. Розклад групи Андрія Місюка та занять на вул. Львівській, 75 уточнюйте у тренерів.</p></div></div>
  <div class="grid" style="grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);align-items:start" data-split>
    <div class="reveal">{schedule_table()}</div>
    {price_card()}
  </div>
</div></section>

<section class="section" id="pershe" aria-labelledby="pershe-h"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Крок 3</p><h2 class="h-lg" id="pershe-h">Що взяти на перше тренування</h2></div></div>
  {first_training_list()}
</div></section>

<section class="section section--surface" id="kontakty" aria-labelledby="kontakty-h"><div class="container">
  <div class="section-head"><div><p class="eyebrow">Контакти</p><h2 class="h-lg" id="kontakty-h">Як нас знайти</h2></div>
    {social_links()}</div>
  {hall_cards()}
</div></section>

<section class="section" aria-labelledby="faq-h"><div class="container" style="max-width:900px">
  <div class="section-head"><div><p class="eyebrow">Питання</p><h2 class="h-lg" id="faq-h">Часті питання</h2></div></div>
  <div class="faq">{faq_html}</div>
</div></section>'''
    return layout("zapys.html", "Розклад і ціни",
                  f"Запис до академії ММА «Воїн» у Луцьку: групи для дітей, новачків і досвідчених спортсменів, розклад тренувань, абонемент {club['price']['monthly']} грн/міс, адреси залів.",
                  body)


PAGES_BUILD = {
    "index.html": page_home,
    "trenery.html": page_coaches,
    "gordist.html": page_pride,
    "novyny.html": page_news,
    "pro-akademiyu.html": page_about,
    "zapys.html": page_join,
}

if __name__ == "__main__":
    for name, fn in PAGES_BUILD.items():
        (ROOT / name).write_text(fn(), "utf-8")
        print("built", name)
    # 404 та службові файли
    (ROOT / ".nojekyll").write_text("")
    urls = "".join(f"<url><loc>{SITE_URL}{'' if p == 'index.html' else p}</loc></url>" for p in PAGES_BUILD)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', "utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", "utf-8")
