# -*- coding: utf-8 -*-
"""Генератор статического сайта «Поезд Последней Войны» (site/*.html + site/en/*.html).
Правь тексты/константы здесь и перегенерируй:  python site/_build.py
Редизайн 2026-07-25 по брифам game-marketer + art-director (см. WORKLOG):
дуо-герой без апскейла, тестер-CTA (единственная оранж-доминанта), полоса 10 биомов
из готовых слоёв, anti-features, ретина-кадры в рамках «полевой терминал», scroll-reveal.
Тексты легалок = scripts/ui/legal/LegalDocs.gd (единый источник, суть 1:1; правки — синхронно!).
Godot папку не видит (site/.gdignore). Деплой: см. память site-deploy (subtree → didogames-site)."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

GAME_RU = "Поезд Последней Войны"
GAME_EN = "The Last War: Train"   # флаг ASO: калька, кандидат на пересмотр вместе с листингом
BASE = "https://didogames.net"
DEV_RU = "Dido Games"
DEV_EN = "Dido Games"
EMAIL = "support@didogames.net"   # вся внешняя коммуникация (владелец 2026-07-25)
DATE_RU = "5 июля 2026 г."   # = LegalDocs.EFFECTIVE_DATE_RU; обновить к публикации
DATE_EN = "July 5, 2026"
# TODO(юрист): заменить на конкретную юрисдикцию перед сабмитом в стор.
LAW_RU = "правом страны постоянного проживания Разработчика"
LAW_EN = "the laws of the Developer's country of residence"
# ESP-эндпоинт почтовой формы (EmailOctopus/MailerLite). Пусто → форма скрыта, CTA = заявка в тест.
ESP_ACTION = ""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&'
         'family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500&display=swap&subset=cyrillic"'
         ' rel="stylesheet">')

# Имена биомов = набор UI_BIOME_* (то, что игрок видит в меню/сторах; рекомендация АД).
BIOMES_RU = ["ЛЕДЯНЫЕ ПУСТОШИ", "МЁРТВЫЙ ЛЕС", "ГОРНЫЙ ПЕРЕВАЛ", "ТОКСИЧНАЯ ЗОНА",
             "ПЕПЕЛЬНАЯ ПУСТОШЬ", "МЁРТВЫЙ МЕГАПОЛИС", "РАДИОАКТИВНАЯ ПУСТЫНЯ",
             "ЗАТОПЛЕННАЯ ЗОНА", "КЛАДБИЩЕ МАШИН", "ЛЕДЯНАЯ ЦИТАДЕЛЬ"]
BIOMES_EN = ["ICE WASTES", "DEAD FOREST", "MOUNTAIN PASS", "TOXIC ZONE",
             "ASH WASTES", "DEAD MEGALOPOLIS", "RADIOACTIVE DESERT",
             "FLOODED ZONE", "MACHINE GRAVEYARD", "ICE CITADEL"]


def chrome_top(lang: str, depth: str, rel: str) -> str:
    game = GAME_RU if lang == "ru" else GAME_EN
    nav = {
        "ru": [("index.html#svodka", "Сводка"), ("index.html#marshrut", "Маршрут"),
               ("index.html#kadry", "Кадры"), ("support.html", "Поддержка")],
        "en": [("index.html#svodka", "Overview"), ("index.html#marshrut", "The route"),
               ("index.html#kadry", "Screens"), ("support.html", "Support")],
    }[lang]
    base = rel[3:] if rel.startswith("en/") else rel
    ru_href = (base if lang == "ru" else "../" + base)
    en_href = ("en/" + base if lang == "ru" else base)
    links = " ".join('<a href="%s">%s</a>' % (h, t) for h, t in nav)
    return (
        '<div class="secureline"><span class="dot"></span>'
        '<span>SECURE_LINE // %s</span><span class="grow"></span>%s '
        '<nav class="langs"><a href="%s" class="%s">RU</a><a href="%s" class="%s">EN</a></nav></div>'
        % (game.upper(), links,
           ru_href, "active" if lang == "ru" else "",
           en_href, "active" if lang == "en" else "")
    )


def chrome_foot(lang: str, depth: str) -> str:
    t = {
        "ru": ("РАЗРАБОТЧИК", "СВЯЗЬ", "ДОКУМЕНТЫ", "Политика конфиденциальности",
               "Условия использования", "Поддержка",
               "© 2026 %s. «%s». Виртуальные предметы не имеют денежной стоимости." % (DEV_RU, GAME_RU),
               "Соло-инди на Godot: код, дизайн и арт-продакшн — один человек."),
        "en": ("DEVELOPER", "CONTACT", "DOCUMENTS", "Privacy Policy", "Terms of Use", "Support",
               "© 2026 %s. \"%s\". Virtual items have no monetary value." % (DEV_EN, GAME_EN),
               "A solo indie on Godot: code, design and art production by one person."),
    }[lang]
    dev = DEV_RU if lang == "ru" else DEV_EN
    return (
        '<footer><div class="foot-inner">'
        '<div class="foot-block foot-logo"><img src="%(d)sassets/img/logo.png" alt=""><span>%(game)s</span></div>'
        '<div class="foot-block"><div class="field">%(f0)s</div>%(dev)s<br><span style="font-size:13px">%(solo)s</span></div>'
        '<div class="foot-block"><div class="field">%(f1)s</div><a href="mailto:%(mail)s">%(mail)s</a></div>'
        '<div class="foot-block"><div class="field">%(f2)s</div>'
        '<a href="privacy.html">%(p)s</a><a href="terms.html">%(tm)s</a><a href="support.html">%(s)s</a></div>'
        '<div class="stamp" aria-hidden="true"><img src="%(d)sassets/img/logo.png" alt=""></div>'
        '</div><div class="foot-note">%(note)s</div></footer>'
        % {"d": depth, "game": (GAME_RU if lang == "ru" else GAME_EN), "dev": dev, "mail": EMAIL,
           "f0": t[0], "f1": t[1], "f2": t[2], "p": t[3], "tm": t[4], "s": t[5],
           "note": t[6], "solo": t[7]}
    )


def page(lang: str, title: str, body: str, rel: str = "index.html") -> str:
    depth = "../" if rel.startswith("en/") else ""
    return (
        '<!doctype html><html lang="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>%s</title>'
        '<link rel="icon" type="image/png" href="%sassets/img/favicon.png">'
        '<link rel="apple-touch-icon" href="%sassets/img/logo.png">'
        '%s<link rel="stylesheet" href="%sassets/style.css"></head><body>'
        % (lang, title, depth, depth, FONTS, depth)
    ) + chrome_top(lang, depth, rel) + body + chrome_foot(lang, depth) + "</body></html>"


# ── ЛЕНДИНГ ──────────────────────────────────────────────────────────────────
REVEAL_JS = (
    '<script>(function(){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
    'var io=new IntersectionObserver(function(es){es.forEach(function(e){'
    'if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{threshold:.15});'
    'document.querySelectorAll(".rv").forEach(function(el){io.observe(el);});})();</script>'
)


def landing(lang: str) -> str:
    d = "../" if lang == "en" else ""
    ru = lang == "ru"
    L = {
        "eyebrow": "МАРШРУТ 01 // СЕКТОР 01" if ru else "ROUTE 01 // SECTOR 01",
        "name": GAME_RU if ru else GAME_EN,
        "tag": ("Целиться не нужно — зенитки бьют сами. Ты ловишь кристаллы, что падают с неба, "
                "и между волнами решаешь, какой системе поезда жить.") if ru else
               ("No aiming — the turrets handle that. You catch the crystals falling from the sky, "
                "and between waves you decide which of the train's systems survives."),
        "facts": ("Дизельпанк ПВО-выживание · 10 биомов · дерево на 190+ узлов · без энергии и таймеров")
                 if ru else
                 ("Dieselpunk AA-survival · 10 biomes · a 190+ node tree · no energy, no timers"),
        "cta": "ЗАПИСАТЬСЯ В ЗАКРЫТЫЙ ТЕСТ" if ru else "JOIN THE CLOSED TEST",
        "cta_mail_subj": ("Закрытый тест — Поезд Последней Войны" if ru else "Closed test — The Last War: Train"),
        "cta_mail_body": ("Привет! Хочу участвовать в закрытом тесте. Мой Android-девайс: " if ru
                          else "Hi! I want to join the closed test. My Android device: "),
        "status": ("СТАТУС: ПОДГОТОВКА К ЗАКРЫТОМУ ТЕСТУ · ANDROID ПЕРВЫМ · iOS ПОЗЖЕ" if ru
                   else "STATUS: PREPARING CLOSED TESTING · ANDROID FIRST · iOS LATER"),
        "svodka_field": "ФОРМУЛЯР 141-У" if ru else "FILE 141-U",
        "svodka": "СВОДКА" if ru else "OVERVIEW",
        "kadry_field": "АРХИВ ШТАБА" if ru else "HQ ARCHIVE",
        "kadry": "КАДРЫ" if ru else "SCREENS",
        "route_field": "МАРШРУТ // 10 СЕКТОРОВ" if ru else "THE ROUTE // 10 SECTORS",
        "route": "ОТ ПУСТОШЕЙ ДО ЦИТАДЕЛИ" if ru else "WASTES TO CITADEL",
        "what_field": "РЕЖИМ // AA-SURVIVAL" if ru else "MODE // AA-SURVIVAL",
        "what_h": "Что это за игра" if ru else "What this game is",
        "what_rows": [("РЕЖИМ" if ru else "MODE", "аркадное ПВО-выживание, портрет, одна рука" if ru
                       else "arcade AA-survival, portrait, one hand"),
                      ("ЦИКЛ" if ru else "LOOP", "волна → кристаллы → дерево узлов → волна" if ru
                       else "wave → crystals → node tree → wave"),
                      ("СЕССИЯ" if ru else "SESSION", "≈ 4 минуты на миссию" if ru else "≈ 4 minutes per mission")],
        "anti_h": "Чего здесь нет" if ru else "What's not here",
        "anti": (["Энергии и таймеров ожидания", "Обязательного интернета — кампания играется офлайн",
                  "Платы за забеги — они бесплатные", "Рекламы посреди боя — только добровольная за бонус"]
                 if ru else
                 ["No energy, no wait timers", "No forced internet — the campaign plays offline",
                  "No paying per run — runs are free", "No mid-combat ads — rewarded only, always your choice"]),
        "finale_h": "СОСТАВ ГОТОВ К ВЫХОДУ" if ru else "THE CONSIST IS READY",
    }
    cards_lead = (("ПОЛЕ СБОРА // РУКИ ИГРОКА", "Ловить, а не целиться",
                   "Кристаллы падают с неба и должны быть пойманы до земли. Промахнулся — "
                   "реактор не зарядится, дерево не откроется.") if ru else
                  ("HARVEST FIELD // YOUR HANDS", "Catch, don't aim",
                   "Crystals fall from the sky and have to be caught before they hit the ground. "
                   "Miss them and the reactor stays cold, the tree stays shut."))
    cards3 = ([("ПРОКАЧКА // SYSTEM RESTORE", "Дерево узлов",
                "Вся сила рана — в контуре восстановления: 190+ узлов, платите кристаллами между волнами.", "tree"),
               ("МАРШРУТ // 10 БИОМОВ", "От Пустошей до Цитадели",
                "Десять биомов со своими врагами, боссами и погодой — полоса ниже.", "map"),
               ("СОСТАВ // ДЕПО", "Поезд-крепость",
                "Платформы, вагоны, орудия, модули и трофейные ядра — соберите собственный состав.", "depot")]
              if ru else
              [("PROGRESSION // SYSTEM RESTORE", "Node tree",
                "All in-run power lives in the restore circuit: 190+ nodes, paid in crystals between waves.", "tree"),
               ("ROUTE // 10 BIOMES", "Wastes to Citadel",
                "Ten biomes with their own enemies, bosses and weather — see the band below.", "map"),
               ("CONSIST // DEPOT", "Fortress on rails",
                "Platforms, wagons, guns, modules and trophy cores — build your own consist.", "depot")])
    shots = ([("shot_combat.jpg", "БОЙ // СЕКТОР 1"), ("shot_menu.jpg", "ГЛАВНОЕ МЕНЮ"),
              ("shot_tree.jpg", "ДЕРЕВО УЗЛОВ")] if ru else
             [("shot_combat.jpg", "COMBAT // SECTOR 1"), ("shot_menu.jpg", "MAIN MENU"),
              ("shot_tree.jpg", "NODE TREE")])
    biomes = BIOMES_RU if ru else BIOMES_EN
    title = ("%s — официальный сайт" % GAME_RU) if ru else ("%s — official site" % GAME_EN)

    mailto = ('mailto:%s?subject=%s&body=%s' % (EMAIL,
              L["cta_mail_subj"].replace(" ", "%20"), L["cta_mail_body"].replace(" ", "%20")))
    cta_block = ('<a class="cta" href="%s">%s</a>'
                 '<div class="cta-sub field-long">%s</div>' % (mailto, L["cta"], L["status"]))

    hero = (
        '<header class="hero">'
        '<div class="hero-wash" aria-hidden="true"><img src="%(d)sassets/img/hero_mobile.jpg" alt=""></div>'
        '<div class="hero-veil" aria-hidden="true"></div>'
        '<div class="grain" aria-hidden="true"></div>'
        '<div class="hero-grid">'
        '<div class="hero-copy"><div class="field">%(eye)s</div><h1 class="title">%(name)s</h1>'
        '<p class="tagline">%(tag)s</p><div class="microfacts field-long">%(facts)s</div>%(cta)s</div>'
        '<div class="hero-window braces">'
        '<picture><source media="(min-width:900px)" srcset="%(d)sassets/img/hero_portrait.jpg">'
        '<img src="%(d)sassets/img/hero_mobile.jpg" alt="%(name)s — key art"></picture></div>'
        '</div></header>'
        % {"d": d, "eye": L["eyebrow"], "name": L["name"], "tag": L["tag"],
           "facts": L["facts"], "cta": cta_block}
    )

    cards_html = (
        '<div class="card lead rv"><div class="recess"><img src="%(d)sassets/img/nav_battle.png" alt=""></div>'
        '<div><div class="field">%(f)s</div><h3>%(h)s</h3><p>%(p)s</p></div></div>'
        % {"d": d, "f": cards_lead[0], "h": cards_lead[1], "p": cards_lead[2]}
    ) + '<div class="cards3">' + "".join(
        '<div class="card rv" style="--i:%d"><div class="recess" style="margin-bottom:14px">'
        '<img src="%sassets/img/nav_%s.png" alt=""></div>'
        '<div class="field">%s</div><h3>%s</h3><p>%s</p></div>'
        % (i, d, icon, f, h, pt) for i, (f, h, pt, icon) in enumerate(cards3)) + '</div>'

    slats = "".join(
        '<div class="slat rv" style="--i:%d"><img src="%sassets/img/biome_%02d.jpg" alt="%s" loading="lazy">'
        '<div class="slat-cap"><div class="slat-num">%02d</div><div class="slat-name">%s</div></div></div>'
        % (i, d, i + 1, name, i + 1, name) for i, name in enumerate(biomes))

    what_rows = "".join('<li><b class="field" style="min-width:96px">%s</b> %s</li>' % r for r in L["what_rows"])
    anti_rows = "".join('<li>%s</li>' % a for a in L["anti"])
    duo = (
        '<section class="section" id="whatis"><div class="duo">'
        '<div class="rv"><div class="field">%(wf)s</div><div class="h1x">%(wh)s</div>'
        '<ul class="speclist" style="margin-bottom:28px">%(rows)s</ul>'
        '<div class="field" style="margin-bottom:6px">%(af)s</div>'
        '<div class="h1x" style="font-size:30px">%(ah)s</div><ul class="speclist">%(anti)s</ul></div>'
        '<div class="rv" style="--i:2; display:flex; justify-content:center">'
        '<div class="term braces" style="max-width:320px; transform:rotate(4deg)">'
        '<img src="%(d)sassets/img/shot_combat.jpg" alt="%(alt)s" loading="lazy"></div></div>'
        '</div></section>'
        % {"wf": L["what_field"], "wh": L["what_h"], "rows": what_rows,
           "af": "ФОРМУЛЯР // БЕЗ ЗВЁЗДОЧЕК" if ru else "FORM // NO ASTERISKS",
           "ah": L["anti_h"], "anti": anti_rows, "d": d,
           "alt": "Бой" if ru else "Combat"}
    )

    fan = '<div class="fan">' + "".join(
        '<figure class="fan-item rv" style="--i:%d"><div class="term">'
        '<img src="%sassets/img/%s" alt="%s" loading="lazy"><figcaption class="term-cap">%s</figcaption>'
        '</div></figure>' % (i, d, f, cap, cap) for i, (f, cap) in enumerate(shots)) + '</div>'

    body = (
        hero
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<div class="plate-b"><section class="section" id="svodka"><div class="section-head">'
           '<span class="field">%s</span><h2>%s</h2></div>%s</section></div>'
           % (L["svodka_field"], L["svodka"], cards_html))
        + ('<section class="biomes" id="marshrut"><div class="biomes-head"><div class="section-head" style="margin-bottom:0">'
           '<span class="field">%s</span><h2>%s</h2></div></div>'
           '<div class="biome-band">%s</div></section>'
           % (L["route_field"], L["route"], slats))
        + '<div class="perf" aria-hidden="true"></div>'
        + duo
        + ('<div class="plate-b"><section class="section" id="kadry"><div class="section-head">'
           '<span class="field">%s</span><h2>%s</h2></div>%s</section></div>'
           % (L["kadry_field"], L["kadry"], fan))
        + ('<div class="finale braces"><img src="%sassets/img/hero_mobile.jpg" alt="" loading="lazy">'
           '<div class="finale-inner rv"><div class="h1x" style="font-size:34px">%s</div><div>%s</div></div></div>'
           % (d, L["finale_h"], cta_block))
        + REVEAL_JS
    )
    return page(lang, title, body, rel=("en/index.html" if lang == "en" else "index.html"))


# ── ДОКУМЕНТЫ (тексты = LegalDocs.gd, 1:1 по сути) ───────────────────────────
def doc_page(lang, doc_field, doc_title, date, sections, intro, page_title, rel):
    secs = ""
    for h, body in sections:
        secs += "<h2>%s</h2>%s" % (h, body)
    back = '<p class="backlink"><a href="index.html">&larr; %s</a></p>' % (
        "НА ГЛАВНУЮ" if lang == "ru" else "BACK TO MAIN")
    body = (
        '<main class="doc">%s<div class="doc-head"><div class="field">%s</div><h1>%s</h1>'
        '<div class="date">%s</div></div><p>%s</p>%s%s</main>'
        % (back, doc_field, doc_title,
           ("Дата вступления в силу: %s" if lang == "ru" else "Effective date: %s") % date,
           intro, secs, back)
    )
    return page(lang, page_title, body, rel=rel)


def p(*ps):
    return "".join("<p>%s</p>" % x for x in ps)


def ul(*items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items)


TERMS_RU = [
    ("1. Лицензия", p("Разработчик предоставляет вам ограниченную, личную, неисключительную, непередаваемую и отзывную лицензию на использование Игры для личных некоммерческих целей на принадлежащих вам устройствах, в соответствии с настоящими Условиями и правилами магазина приложений, через который получена Игра.")),
    ("2. Правила поведения", p("Вы обязуетесь не: (а) модифицировать, декомпилировать, дизассемблировать или подвергать Игру обратной разработке; (б) использовать читы, боты, эксплойты, автоматизацию или стороннее ПО, дающее нечестное преимущество; (в) вмешиваться в работу Игры или серверов; (г) использовать Игру незаконно или для нарушения прав третьих лиц.")),
    ("3. Виртуальные предметы и валюта", p("Игра содержит виртуальную валюту и предметы (например, ресурсы, модули, ящики), которые не имеют денежной стоимости и не могут быть обменены на реальные деньги. Вы получаете ограниченную лицензию на их использование внутри Игры; вы не приобретаете на них право собственности. Разработчик вправе изменять, регулировать баланс или удалять виртуальные предметы. Неиспользованные виртуальные предметы, как правило, не подлежат возврату, кроме случаев, предусмотренных применимым правом или правилами магазина.")),
    ("4. Покупки", p("Покупки внутри приложения обрабатываются магазином приложений (Google Play или Apple App Store) в соответствии с их условиями. Все вопросы оплаты, возвратов и споров по платежам решаются согласно правилам соответствующего магазина. Разработчик не хранит данные вашей платёжной карты.")),
    ("5. Реклама", p("Игра может показывать рекламу с вознаграждением (rewarded), которую вы запускаете добровольно в обмен на внутриигровые бонусы. Реклама предоставляется сторонними сетями; см. <a href=\"privacy.html\">Политику конфиденциальности</a>.")),
    ("6. Интеллектуальная собственность", p("Игра, включая код, графику, звук, тексты и товарные знаки, принадлежит Разработчику или его лицензиарам и защищена законом. Никакие права, кроме прямо предоставленной лицензии, вам не передаются.")),
    ("7. Отказ от гарантий и ограничение ответственности", p("Игра предоставляется «как есть» и «как доступно», без каких-либо гарантий. В максимально допустимой законом степени Разработчик не несёт ответственности за косвенные, случайные или последующие убытки, связанные с использованием или невозможностью использования Игры. Ничто в настоящих Условиях не ограничивает права, которые не могут быть ограничены по применимому праву (в т. ч. права потребителей).")),
    ("8. Прекращение", p("Вы можете прекратить использование в любой момент, удалив Игру. Разработчик вправе приостановить или прекратить ваш доступ при нарушении настоящих Условий.")),
    ("9. Изменения", p("Условия могут обновляться. Существенные изменения будут отражены обновлением даты вступления в силу; продолжение использования Игры означает согласие с обновлёнными Условиями.")),
    ("10. Применимое право", p("Настоящие Условия регулируются %s, без учёта коллизионных норм." % LAW_RU)),
    ("11. Контакты", p("По вопросам об Условиях: %s (<a href=\"mailto:%s\">%s</a>)." % (DEV_RU, EMAIL, EMAIL))),
]

PRIVACY_RU = [
    ("1. Какие данные обрабатываются", p("Игра не требует регистрации и не запрашивает у вас имя, адрес или электронную почту. При использовании Игры могут обрабатываться:") + ul(
        "идентификаторы устройства, включая рекламный идентификатор (Google Advertising ID / Apple IDFA), — для рекламы и аналитики;",
        "данные об использовании и игровые события (например, прогресс, экономические события, показы рекламы, покупки) — для аналитики и улучшения Игры;",
        "диагностические данные и отчёты о сбоях — для стабильности;",
        "записи о покупках (идентификатор товара, факт покупки) — для выдачи товара; данные платёжной карты обрабатывает магазин приложений, а не Разработчик;",
        "игровой прогресс — хранится локально на устройстве и, при использовании облачного сохранения платформы, в вашем аккаунте платформы.")),
    ("2. Как используются данные", p("Данные используются, чтобы: обеспечивать работу Игры и сохранение прогресса; показывать рекламу; анализировать использование и исправлять ошибки; обрабатывать покупки; выполнять требования закона.")),
    ("3. Сторонние поставщики услуг", p("Игра использует сторонние сервисы, которые могут обрабатывать данные как самостоятельные операторы согласно своим политикам:") + ul(
        "Google AdMob — реклама (рекламный идентификатор);",
        "Google Firebase (Analytics, Crashlytics) / GameAnalytics — аналитика и отчёты о сбоях;",
        "Google Play Billing / Apple StoreKit — покупки;",
        "Google Play Games / Apple GameKit — достижения, таблицы лидеров, облачное сохранение.") + p("Ознакомьтесь с политиками конфиденциальности соответствующих поставщиков.")),
    ("4. Реклама и согласие", p("Реклама может быть персонализированной. Перед сбором данных для рекламы в применимых регионах (ЕЭЗ/Великобритания) запрашивается согласие через форму управления согласием (Google UMP/GDPR), а на устройствах Apple — разрешение App Tracking Transparency (ATT). Вы можете изменить выбор в настройках устройства (сброс рекламного идентификатора, ограничение отслеживания) или в меню согласия.")),
    ("5. Хранение и удаление", p("Игровой прогресс хранится локально в памяти приложения и удаляется при удалении Игры; при облачном сохранении — управляется в вашем аккаунте платформы. Данные, обрабатываемые сторонними сервисами, хранятся согласно их политикам.")),
    ("6. Ваши права", p("В зависимости от вашего региона (например, GDPR в ЕЭЗ, CCPA в Калифорнии) вы можете иметь право на доступ, исправление, удаление данных, ограничение обработки и отзыв согласия. Для реализации прав свяжитесь с нами по адресу <a href=\"mailto:%s\">%s</a>; часть запросов также реализуется через настройки устройства и магазина приложений." % (EMAIL, EMAIL))),
    ("7. Дети", p("Игра не предназначена для детей младше 13 лет (либо иного возраста, установленного вашим законодательством). Мы сознательно не собираем данные таких детей. Если вы считаете, что ребёнок предоставил данные, свяжитесь с нами для их удаления.")),
    ("8. Безопасность", p("Применяются разумные технические и организационные меры защиты данных. Абсолютная безопасность передачи и хранения данных не может быть гарантирована.")),
    ("9. Международная передача", p("Данные могут обрабатываться на серверах в других странах с иным уровнем защиты данных, с соблюдением применимых требований.")),
    ("10. Изменения", p("Политика может обновляться; существенные изменения отражаются обновлением даты вступления в силу.")),
    ("11. Контакты", p("Оператор: %s. По вопросам конфиденциальности: <a href=\"mailto:%s\">%s</a>." % (DEV_RU, EMAIL, EMAIL))),
]

TERMS_EN = [
    ("1. License", p("The Developer grants you a limited, personal, non-exclusive, non-transferable, revocable license to use the Game for personal, non-commercial purposes on devices you own, subject to these Terms and the rules of the app store you obtained the Game from.")),
    ("2. Code of Conduct", p("You agree not to: (a) modify, decompile, disassemble, or reverse-engineer the Game; (b) use cheats, bots, exploits, automation, or third-party software that grants an unfair advantage; (c) interfere with the Game or its servers; (d) use the Game unlawfully or to infringe the rights of others.")),
    ("3. Virtual Items and Currency", p("The Game includes virtual currency and items (e.g., resources, modules, crates) that have no monetary value and cannot be exchanged for real money. You receive a limited license to use them within the Game and do not acquire ownership of them. The Developer may modify, rebalance, or remove virtual items. Unused virtual items are generally non-refundable except where required by applicable law or store rules.")),
    ("4. Purchases", p("In-app purchases are processed by the app store (Google Play or Apple App Store) under their terms. All payment, refund, and billing-dispute matters are handled per that store's rules. The Developer does not store your payment card details.")),
    ("5. Advertising", p("The Game may show rewarded advertising that you start voluntarily in exchange for in-game bonuses. Ads are provided by third-party networks; see the <a href=\"privacy.html\">Privacy Policy</a>.")),
    ("6. Intellectual Property", p("The Game, including its code, graphics, audio, text, and trademarks, belongs to the Developer or its licensors and is protected by law. No rights are granted to you other than the license expressly stated.")),
    ("7. Disclaimer and Limitation of Liability", p("The Game is provided \"as is\" and \"as available\" without warranties of any kind. To the maximum extent permitted by law, the Developer is not liable for indirect, incidental, or consequential damages arising from use of or inability to use the Game. Nothing here limits rights that cannot be limited under applicable law (including consumer rights).")),
    ("8. Termination", p("You may stop using the Game at any time by deleting it. The Developer may suspend or terminate your access if you breach these Terms.")),
    ("9. Changes", p("These Terms may be updated. Material changes are reflected by updating the effective date; continued use of the Game means acceptance of the updated Terms.")),
    ("10. Governing Law", p("These Terms are governed by %s, without regard to conflict-of-law rules." % LAW_EN)),
    ("11. Contact", p("For questions about these Terms: %s (<a href=\"mailto:%s\">%s</a>)." % (DEV_EN, EMAIL, EMAIL))),
]

PRIVACY_EN = [
    ("1. Data We Process", p("The Game requires no registration and does not ask you for your name, address, or email. When you use the Game, the following may be processed:") + ul(
        "device identifiers, including the advertising identifier (Google Advertising ID / Apple IDFA), for advertising and analytics;",
        "usage data and game events (e.g., progress, economy events, ad impressions, purchases) for analytics and improving the Game;",
        "diagnostic data and crash reports for stability;",
        "purchase records (product id, purchase fact) to deliver goods; payment card data is handled by the app store, not the Developer;",
        "game progress, stored locally on your device and, if platform cloud save is used, in your platform account.")),
    ("2. How Data Is Used", p("Data is used to: operate the Game and save progress; serve advertising; analyze usage and fix bugs; process purchases; and comply with legal obligations.")),
    ("3. Third-Party Providers", p("The Game uses third-party services that may process data as independent controllers under their own policies:") + ul(
        "Google AdMob — advertising (advertising identifier);",
        "Google Firebase (Analytics, Crashlytics) / GameAnalytics — analytics and crash reports;",
        "Google Play Billing / Apple StoreKit — purchases;",
        "Google Play Games / Apple GameKit — achievements, leaderboards, cloud save.") + p("Please review those providers' privacy policies.")),
    ("4. Advertising and Consent", p("Advertising may be personalized. In applicable regions (EEA/UK), consent is requested before collecting data for ads via a consent-management form (Google UMP/GDPR), and on Apple devices via App Tracking Transparency (ATT). You can change your choice in your device settings (reset advertising id, limit tracking) or in the consent menu.")),
    ("5. Storage and Deletion", p("Game progress is stored locally in app storage and removed when you delete the Game; if cloud save is used, it is managed in your platform account. Data processed by third-party services is retained per their policies.")),
    ("6. Your Rights", p("Depending on your region (e.g., GDPR in the EEA, CCPA in California), you may have rights to access, correct, delete, or restrict processing of your data and to withdraw consent. To exercise these rights, contact us at <a href=\"mailto:%s\">%s</a>; some requests are also served through device and app-store settings." % (EMAIL, EMAIL))),
    ("7. Children", p("The Game is not directed to children under 13 (or the age set by your local law). We do not knowingly collect data from such children. If you believe a child provided data, contact us to have it deleted.")),
    ("8. Security", p("Reasonable technical and organizational safeguards are applied. No method of data transmission or storage can be guaranteed absolutely secure.")),
    ("9. International Transfers", p("Data may be processed on servers in other countries with different data-protection levels, subject to applicable requirements.")),
    ("10. Changes", p("This Policy may be updated; material changes are reflected by updating the effective date.")),
    ("11. Contact", p("Controller: %s. For privacy questions: <a href=\"mailto:%s\">%s</a>." % (DEV_EN, EMAIL, EMAIL))),
]


def support(lang):
    if lang == "ru":
        secs = [
            ("Связь", p("По любым вопросам об игре: <a href=\"mailto:%s\">%s</a>. Обычно отвечаем в течение нескольких рабочих дней." % (EMAIL, EMAIL))),
            ("Покупки и возвраты", p("Покупки обрабатывает магазин приложений. Возвраты — через Google Play или App Store по их правилам; при проблеме с неполученным товаром напишите нам, приложив идентификатор заказа из письма магазина.")),
            ("Прогресс и его удаление", p("Прогресс хранится локально на устройстве (и в облачном сохранении платформы, если оно включено). Чтобы удалить игровые данные — удалите приложение; облачное сохранение управляется в аккаунте Google Play Games / Game Center. Для запроса на удаление данных, обрабатываемых аналитикой/рекламой, напишите на почту выше (см. <a href=\"privacy.html\">Политику конфиденциальности</a>, раздел 6).")),
            ("Частые вопросы", ul(
                "<b>Игра не запускается / вылетает.</b> Перезапустите устройство, проверьте свободное место и обновление игры. Если не помогло — напишите нам с моделью устройства.",
                "<b>Пропала покупка.</b> В магазине откройте «Восстановить покупки» на вкладке «Ресурсы», затем перезапустите игру.",
                "<b>Можно ли играть без интернета?</b> Да, кампания играется офлайн; реклама и облачное сохранение требуют сети.")),
        ]
        return doc_page("ru", "СЛУЖБА ПОДДЕРЖКИ", "Поддержка", DATE_RU, secs,
                        "Мы — маленькая команда, и каждое письмо читает разработчик.",
                        "Поддержка — %s" % GAME_RU, "support.html")
    secs = [
        ("Contact", p("For any questions about the game: <a href=\"mailto:%s\">%s</a>. We usually reply within a few business days." % (EMAIL, EMAIL))),
        ("Purchases and Refunds", p("Purchases are processed by the app store. Refunds go through Google Play or the App Store under their rules; if a purchased item was not delivered, email us with the order id from the store receipt.")),
        ("Progress and Data Deletion", p("Progress is stored locally on your device (and in platform cloud save, if enabled). To delete game data, uninstall the app; cloud saves are managed in your Google Play Games / Game Center account. To request deletion of data processed by analytics/ads, email us (see the <a href=\"privacy.html\">Privacy Policy</a>, section 6).")),
        ("FAQ", ul(
            "<b>The game does not start / crashes.</b> Restart the device, check free space and updates. If it persists, email us your device model.",
            "<b>A purchase is missing.</b> Open \"Restore purchases\" on the Resources tab of the shop, then restart the game.",
            "<b>Can I play offline?</b> Yes, the campaign is playable offline; ads and cloud save need a connection.")),
    ]
    return doc_page("en", "SUPPORT DESK", "Support", DATE_EN, secs,
                    "We are a small team - the developer reads every email.",
                    "Support — %s" % GAME_EN, "en/support.html")


OUT = {
    "index.html": landing("ru"),
    "terms.html": doc_page("ru", "ФОРМУЛЯР // ДОКУМЕНТ 01", "Условия использования", DATE_RU, TERMS_RU,
                           "Настоящие Условия использования (далее — «Условия») регулируют доступ к игре «%s» (далее — «Игра») и её использование. Устанавливая, запуская или используя Игру, вы подтверждаете, что прочитали, поняли и принимаете настоящие Условия. Если вы не согласны с Условиями, не используйте Игру." % GAME_RU,
                           "Условия использования — %s" % GAME_RU, "terms.html"),
    "privacy.html": doc_page("ru", "ФОРМУЛЯР // ДОКУМЕНТ 02", "Политика конфиденциальности", DATE_RU, PRIVACY_RU,
                             "Настоящая Политика конфиденциальности описывает, какие данные обрабатываются при использовании игры «%s» (далее — «Игра») и как они используются. Используя Игру, вы соглашаетесь с настоящей Политикой." % GAME_RU,
                             "Политика конфиденциальности — %s" % GAME_RU, "privacy.html"),
    "support.html": support("ru"),
    "en/index.html": landing("en"),
    "en/terms.html": doc_page("en", "FORM // DOCUMENT 01", "Terms of Use", DATE_EN, TERMS_EN,
                              "These Terms of Use (the \"Terms\") govern your access to and use of the game \"%s\" (the \"Game\"). By installing, launching, or using the Game, you confirm that you have read, understood, and accept these Terms. If you do not agree, do not use the Game." % GAME_EN,
                              "Terms of Use — %s" % GAME_EN, "en/terms.html"),
    "en/privacy.html": doc_page("en", "FORM // DOCUMENT 02", "Privacy Policy", DATE_EN, PRIVACY_EN,
                                "This Privacy Policy describes what data is processed when you use the game \"%s\" (the \"Game\") and how it is used. By using the Game, you agree to this Policy." % GAME_EN,
                                "Privacy Policy — %s" % GAME_EN, "en/privacy.html"),
    "en/support.html": support("en"),
}

# ── SEO под домен: canonical + hreflang + OpenGraph + JSON-LD ────────────────
DESCS = {
    "index.html": "Аркадное ПВО-выживание: бронепоезд, зенитки, дерево узлов, 10 биомов. Без энергии и таймеров. Скоро в Google Play.",
    "terms.html": "Условия использования игры «%s»." % GAME_RU,
    "privacy.html": "Политика конфиденциальности игры «%s»." % GAME_RU,
    "support.html": "Поддержка игры «%s»: контакты, покупки, удаление данных." % GAME_RU,
    "en/index.html": "Arcade AA-survival: an armored train, anti-air turrets, a node tree, 10 biomes. No energy, no timers. Coming soon to Google Play.",
    "en/terms.html": "Terms of Use for \"%s\"." % GAME_EN,
    "en/privacy.html": "Privacy Policy for \"%s\"." % GAME_EN,
    "en/support.html": "Support for \"%s\": contact, purchases, data deletion." % GAME_EN,
}


def canon(rel):
    if rel == "index.html":
        return BASE + "/"
    if rel == "en/index.html":
        return BASE + "/en/"
    return BASE + "/" + rel


def head_extra(rel, title):
    ru_rel = rel[3:] if rel.startswith("en/") else rel
    en_rel = rel if rel.startswith("en/") else "en/" + rel
    ex = (
        '<meta name="description" content="%s">'
        '<link rel="canonical" href="%s">'
        '<link rel="alternate" hreflang="ru" href="%s">'
        '<link rel="alternate" hreflang="en" href="%s">'
        '<link rel="alternate" hreflang="x-default" href="%s">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="Dido Games">'
        '<meta property="og:title" content="%s">'
        '<meta property="og:description" content="%s">'
        '<meta property="og:image" content="%s/assets/img/og.jpg">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta property="og:url" content="%s">'
        '<meta property="og:locale" content="%s">'
        '<meta property="og:locale:alternate" content="%s">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:image" content="%s/assets/img/og.jpg">'
        '<meta name="theme-color" content="#05070a">'
        % (DESCS[rel], canon(rel), canon(ru_rel), canon(en_rel), canon(ru_rel),
           title, DESCS[rel], BASE, canon(rel),
           ("en_US" if rel.startswith("en/") else "ru_RU"),
           ("ru_RU" if rel.startswith("en/") else "en_US"), BASE)
    )
    if rel in ("index.html", "en/index.html"):
        name = GAME_EN if rel.startswith("en/") else GAME_RU
        ex += ('<script type="application/ld+json">{"@context":"https://schema.org",'
               '"@type":"VideoGame","name":"%s","genre":["Arcade","Survival","Tower Defense"],'
               '"gamePlatform":["Android","iOS"],"applicationCategory":"Game",'
               '"author":{"@type":"Organization","name":"Dido Games","url":"%s"},'
               '"image":"%s/assets/img/og.jpg","url":"%s",'
               '"inLanguage":["ru","en","de","es","fr","it","pl","pt-BR","tr","id"]}'
               '</script>' % (name, BASE, BASE, canon(rel)))
    return ex


for rel, html in OUT.items():
    t0 = html.index("<title>") + 7
    t1 = html.index("</title>")
    html = html[: t1 + 8] + head_extra(rel, html[t0:t1]) + html[t1 + 8:]
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("written", rel, len(html), "bytes")

# ── служебные файлы хостинга ──
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE)
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    urls = "".join("<url><loc>%s</loc></url>" % canon(r) for r in OUT)
    f.write('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
with open(os.path.join(ROOT, "CNAME"), "w", encoding="utf-8", newline="\n") as f:
    f.write("didogames.net\n")   # кастом-домен GitHub Pages
nf = page("ru", "404 — %s" % GAME_RU,
          '<main class="doc"><div class="doc-head"><div class="field">ФОРМУЛЯР // 404</div>'
          '<h1>Страница не найдена</h1><div class="date">Сигнал потерян в пустоши</div></div>'
          '<p class="backlink"><a href="/">&larr; НА ГЛАВНУЮ</a></p></main>', "404.html")
with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(nf)
print("written robots.txt / sitemap.xml / CNAME / 404.html")
