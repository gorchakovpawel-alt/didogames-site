# -*- coding: utf-8 -*-
"""Генератор статического сайта «Поезд Последней Войны» (site/*.html + site/en/*.html).
Правь тексты/константы здесь и перегенерируй:  python site/_build.py
Редизайн 2026-07-25 по брифам game-marketer + art-director (см. WORKLOG):
дуо-герой без апскейла, тестер-CTA (единственная оранж-доминанта), полоса 10 биомов
из готовых слоёв, anti-features, ретина-кадры в рамках «полевой терминал», scroll-reveal.
Тексты легалок = scripts/ui/legal/LegalDocs.gd (единый источник, суть 1:1; правки — синхронно!).
Godot папку не видит (site/.gdignore). Деплой: см. память site-deploy (subtree → didogames-site)."""
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))

GAME_RU = "Поезд Последней Войны"
GAME_EN = "The Last War: Train"   # флаг ASO: калька, кандидат на пересмотр вместе с листингом
BASE = "https://didogames.net"
DEV_RU = "Dido Games"
DEV_EN = "Dido Games"
EMAIL = "support@didogames.net"   # вся внешняя коммуникация (владелец 2026-07-25)
DATE_RU = "31 июля 2026 г."   # = LegalDocs.EFFECTIVE_DATE_RU (держать в паре)
DATE_EN = "July 31, 2026"
# TODO(юрист): заменить на конкретную юрисдикцию перед сабмитом в стор.
LAW_RU = "правом страны постоянного проживания Разработчика"
LAW_EN = "the laws of the Developer's country of residence"
# Форма заявок на инвайт: Google Форма в рабочем Workspace владельца (pavel@didogames.net).
# FormSubmit.co отвалился — его активационные токены не проходили («Confirmation token not
# found»), а Pages статический и своего бэкенда нет. Ответы копятся в самой форме
# (Ответы → можно связать с таблицей); дизайн формы на сайте остаётся наш, Google получает
# только POST. Google не отдаёт CORS-заголовки → шлём no-cors (ответ не читаем) + нативный
# фолбэк без JS. entry.* — id полей формы, менять ТОЛЬКО вместе с самой формой.
FORM_POST = ("https://docs.google.com/forms/d/e/"
             "1FAIpQLSc4Seq_tMWckJWInFR1ENVdKpDfPxTW95gESPxZvaLgVVJHmQ/formResponse")
FORM_F_EMAIL = "entry.1602638693"     # Почта (обязательное)
FORM_F_NAME = "entry.1736986761"      # Позывной
FORM_F_PLATFORM = "entry.1734298389"  # Платформа
FORM_F_LANG = "entry.219790479"       # Язык сайта

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
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
        "ru": [("index.html#video", "Ролик"), ("index.html#ai", "Сделано ИИ"),
               ("index.html#marshrut", "Маршрут"), ("lore.html", "Лор"), ("press.html", "Пресс-кит")],
        "en": [("index.html#video", "Trailer"), ("index.html#ai", "Made by AI"),
               ("index.html#marshrut", "Route"), ("lore.html", "Lore"), ("press.html", "Press kit")],
    }[lang]
    base = rel[3:] if rel.startswith("en/") else rel
    if base == "index.html":   # на самом лендинге якоря — чистые # (без перезагрузки)
        links_prefix = ""
        nav = [(h.replace("index.html#", "#"), t) for h, t in nav]
    ru_href = (base if lang == "ru" else "../" + base)
    en_href = ("en/" + base if lang == "ru" else base)
    links = " ".join('<a href="%s">%s</a>' % (h, t) for h, t in nav)
    notify = "#notify" if base == "index.html" else "index.html#notify"
    hdr_cta = ('<a class="hdr-cta" href="%s">%s</a>'
               % (notify, 'О ВЫХОДЕ' if lang == 'ru' else 'GET NOTIFIED'))
    return (
        '<div class="secureline"><span class="dot"></span>'
        '<span>SECURE_LINE // %s</span><span class="grow"></span><nav class="hdr-nav">%s</nav> '
        '%s<nav class="langs"><a href="%s" class="%s">RU</a><a href="%s" class="%s">EN</a></nav></div>'
        % (game.upper(), links, hdr_cta,
           ru_href, "active" if lang == "ru" else "",
           en_href, "active" if lang == "en" else "")
    )


def chrome_foot(lang: str, depth: str) -> str:
    t = {
        "ru": ("РАЗРАБОТЧИК", "СВЯЗЬ", "ДОКУМЕНТЫ", "Политика конфиденциальности",
               "Условия использования", "Поддержка",
               "© 2026 %s. «%s». Виртуальные предметы не имеют денежной стоимости." % (DEV_RU, GAME_RU),
               "Игра про ИИ, сделанная ИИ: код, арт, звук и баланс созданы искусственным интеллектом."),
        "en": ("DEVELOPER", "CONTACT", "DOCUMENTS", "Privacy Policy", "Terms of Use", "Support",
               "© 2026 %s. \"%s\". Virtual items have no monetary value." % (DEV_EN, GAME_EN),
               "A game about AI, made by AI: code, art, audio and balance are AI-generated."),
    }[lang]
    dev = DEV_RU if lang == "ru" else DEV_EN
    return (
        '<footer><div class="foot-inner">'
        '<div class="foot-block foot-logo"><img src="%(d)sassets/img/logo.png" alt=""><span>%(game)s</span></div>'
        '<div class="foot-block"><div class="field">%(f0)s</div>%(dev)s<br><span class="foot-note-sm">%(solo)s</span></div>'
        '<div class="foot-block"><div class="field">%(f1)s</div><a href="mailto:%(mail)s">%(mail)s</a></div>'
        '<div class="foot-block"><div class="field">%(f2)s</div>'
        '<a href="privacy.html">%(p)s</a><a href="terms.html">%(tm)s</a><a href="support.html">%(s)s</a>'
        '<a href="press.html">%(pk)s</a></div>'
        '<div class="stamp" aria-hidden="true"><img src="%(d)sassets/img/logo.png" alt=""></div>'
        '</div><div class="foot-note">%(note)s</div></footer>'
        % {"d": depth, "game": (GAME_RU if lang == "ru" else GAME_EN), "dev": dev, "mail": EMAIL,
           "f0": t[0], "f1": t[1], "f2": t[2], "p": t[3], "tm": t[4], "s": t[5],
           "note": t[6], "solo": t[7], "pk": ("Пресс-кит" if lang == "ru" else "Press kit")}
    )


def page(lang: str, title: str, body: str, rel: str = "index.html") -> str:
    depth = "../" if rel.startswith("en/") else ""
    return (
        '<!doctype html><html lang="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>%s</title>'
        '<link rel="icon" type="image/png" href="%sassets/img/favicon.png">'
        '<link rel="apple-touch-icon" href="%sassets/img/touch_icon.png">'
        '%s<link rel="stylesheet" href="%sassets/style.css">'
        '<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)'
        'document.documentElement.classList.add("js")</script></head><body>'
        % (lang, title, depth, depth, FONTS, depth)
    ) + chrome_top(lang, depth, rel) + body + chrome_foot(lang, depth) + "</body></html>"


# ── ЛЕНДИНГ ──────────────────────────────────────────────────────────────────
def nbl(text):
    """·-список: каждый пункт в .nb — рвётся только по разделителю (арт-панч П22)."""
    return " · ".join('<span class="nb">%s</span>' % p for p in text.split(" · "))


REVEAL_JS = (
    '<script>(function(){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;'
    'var io=new IntersectionObserver(function(es){es.forEach(function(e){'
    'if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{threshold:.15});'
    'document.querySelectorAll(".rv").forEach(function(el){io.observe(el);});})();</script>'
)

# Лайтбокс: крестик + Esc + клик по фону (владелец 2026-07-25). Вешается на кадры
# лендинга (.fan/.term--tilt) и ссылки пресс-кита (.shots a); без JS пресс-ссылки
# открывают файл как раньше.
LB_JS = (
    '<script>(function(){var o=document.createElement("div");o.className="lb";'
    'o.innerHTML=\'<img alt=""><button class="lb-x" aria-label="Close">&times;</button>\';'
    'document.body.appendChild(o);var im=o.querySelector("img");'
    'function op(s){im.src=s;o.classList.add("on");document.body.style.overflow="hidden"}'
    'function cl(){o.classList.remove("on");document.body.style.overflow="";im.removeAttribute("src")}'
    'o.addEventListener("click",function(e){if(e.target!==im)cl()});'
    'document.addEventListener("keydown",function(e){if(e.key==="Escape")cl()});'
    'function wire(el,get){el.style.cursor="zoom-in";'
    'el.addEventListener("click",function(e){e.preventDefault();op(get())})}'
    'document.querySelectorAll(".fan .term img,.term--tilt img").forEach('
    'function(i){wire(i,function(){return i.currentSrc||i.src})});'
    'document.querySelectorAll(".shots a").forEach('
    'function(a){wire(a,function(){return a.getAttribute("href")})});})();</script>'
)

# Форма: POST в Google Форму. CORS-заголовков Google не отдаёт → шлём no-cors (ответ
# непрозрачный, но запись создаётся) и показываем «принято» сами. Honeypot заполнен ботом →
# молча не отправляем. Без JS работает нативный сабмит (target=_blank, чтобы страница
# Google «Ответ записан» открылась отдельно и лендинг остался на месте).
FORM_JS = (
    '<script>(function(){var f=document.querySelector(".nf");if(!f)return;'
    'function ok(){var g=f.querySelector(".nf-grid"),b=f.querySelector(".nf-btn");'
    'if(g)g.hidden=true;if(b)b.hidden=true;f.querySelector(".nf-ok").hidden=false}'
    'if(!window.fetch)return;f.removeAttribute("target");'
    'f.addEventListener("submit",function(e){e.preventDefault();'
    'var h=f.querySelector(".nf-hp");if(h&&h.value){ok();return}'
    'var b=f.querySelector(".nf-btn");b.disabled=true;'
    'var fd=new FormData(f);fd.delete("_honey");'
    'fetch(f.action,{method:"POST",mode:"no-cors",body:fd})'
    '.then(ok).catch(function(){b.disabled=false;f.setAttribute("target","_blank");f.submit();});'
    '});})();</script>'
)


def landing(lang: str) -> str:
    d = "../" if lang == "en" else ""
    ru = lang == "ru"
    L = {
        # USP владельца 2026-07-26: производство — полностью ИИ; ставим первой строкой экрана.
        "eyebrow": "ИГРА ПРО ИИ · СДЕЛАНА ИИ" if ru else "A GAME ABOUT AI · MADE BY AI",
        "name": GAME_RU if ru else GAME_EN,
        "tag": ("Целиться не нужно — зенитки бьют сами. Ты ловишь кристаллы, что падают с неба, "
                "и между волнами решаешь, какой системе поезда жить.") if ru else
               ("No aiming — the turrets handle that. You catch the crystals falling from the sky, "
                "and between waves you decide which of the train's systems survives."),
        "facts": ("Бесплатно · дизельпанк ПВО-выживание · 10 биомов · дерево на 160+ узлов · без энергии и таймеров")
                 if ru else
                 ("Free to play · dieselpunk AA-survival · 10 biomes · a 160+ node tree · no energy, no timers"),
        "cta": "СООБЩИТЬ МНЕ О ВЫХОДЕ" if ru else "NOTIFY ME AT LAUNCH",
        "cta_mail_subj": ("Сообщите о выходе — Поезд Последней Войны" if ru else "Launch notification — The Last War: Train"),
        "cta_mail_body": ("Напишите мне, когда игра выйдет в Google Play." if ru
                          else "Email me when the game launches on Google Play."),
        "status": ("СТАТУС: ГОТОВИМСЯ К РЕЛИЗУ · GOOGLE PLAY (ANDROID) · iOS ПОЗЖЕ" if ru
                   else "STATUS: PREPARING FOR RELEASE · GOOGLE PLAY (ANDROID) · iOS LATER"),
        "svodka_field": "ФОРМУЛЯР 141-У" if ru else "FILE 141-U",
        "svodka": "СВОДКА" if ru else "OVERVIEW",
        "kadry_field": "АРХИВ ШТАБА" if ru else "HQ ARCHIVE",
        "kadry": "КАДРЫ" if ru else "SCREENS",
        "route_field": "МАРШРУТ // 10 СЕКТОРОВ" if ru else "THE ROUTE // 10 SECTORS",
        "route": "ОТ ПУСТОШЕЙ ДО ЦИТАДЕЛИ" if ru else "FROM THE WASTES TO THE CITADEL",
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
        "finale_h": "СКОРО НА МАРШРУТЕ" if ru else "LAUNCHING SOON",
        "reel_field": "ЗАПИСЬ // 70 СЕКУНД" if ru else "FOOTAGE // 70 SECONDS",
        "reel_h": "ПОСМОТРЕТЬ, КАК ЭТО ИГРАЕТСЯ" if ru else "SEE HOW IT PLAYS",
        "reel_cap": ("Реальная запись из игры: бой, поле сбора, дерево узлов, депо, боссы. "
                     "Со звуком." if ru else
                     "Real in-game footage: combat, harvest field, node tree, depot, bosses. "
                     "With sound."),
        "made_field": "ПРОИЗВОДСТВО // 100% ИИ" if ru else "PRODUCTION // 100% AI",
        "made_h": "Игра про ИИ, сделанная ИИ" if ru else "A game about AI, made by AI",
        "made_lead": ("Мир игры — про машины, которые продолжают войну без людей. "
                      "Сама игра сделана так же: <b>код, графика, звук, баланс и тексты созданы "
                      "искусственным интеллектом от первой строки до релиза.</b>" if ru else
                      "The game's world is about machines that keep fighting a war without people. "
                      "The game itself was built the same way: <b>code, art, audio, balance and text "
                      "are all generated by artificial intelligence, from the first line to release.</b>"),
        "made_rows": ([("КОД", "боевой цикл, экономика, сохранения, магазин — Godot"),
                       ("АРТ", "фоны биомов, враги, ключевой арт, интерфейс и иконки"),
                       ("ЗВУК", "эффекты и музыка"),
                       ("БАЛАНС", "кривые волн, экономика, дерево на 160+ узлов"),
                       ("ТЕКСТЫ", "сюжет, интерфейс и локализация на 10 языков")] if ru else
                      [("CODE", "combat loop, economy, saves, shop — in Godot"),
                       ("ART", "biome backdrops, enemies, key art, UI and icons"),
                       ("AUDIO", "sound effects and music"),
                       ("BALANCE", "wave curves, economy, a 160+ node tree"),
                       ("TEXT", "story, interface and localization into 10 languages")]),
        "made_note": ("Человек ставит задачу и принимает работу. Всё остальное делает ИИ — "
                      "и об этом мы говорим прямо, а не мелким шрифтом." if ru else
                      "A human sets the task and signs off on the result. Everything else is done by AI — "
                      "and we say so up front, not in the fine print."),
    }
    cards_lead = (("ПОЛЕ СБОРА // РУКИ ИГРОКА", "Ловить, а не целиться",
                   "Кристаллы падают с неба и должны быть пойманы до земли. Промахнулся — "
                   "реактор не зарядится, дерево не откроется.") if ru else
                  ("HARVEST FIELD // YOUR HANDS", "Catch, don't aim",
                   "Crystals fall from the sky and have to be caught before they hit the ground. "
                   "Miss them and the reactor stays cold, the tree stays locked."))
    cards3 = ([("ПРОКАЧКА // SYSTEM RESTORE", "Дерево узлов",
                "Вся сила рана — в контуре восстановления: 160+ узлов, платишь кристаллами между волнами.", "tree"),
               ("МАРШРУТ // 10 БИОМОВ", "От Пустошей до Цитадели",
                "Десять биомов со своими врагами, боссами и погодой — полоса ниже.", "map"),
               ("СОСТАВ // ДЕПО", "Поезд-крепость",
                "Платформы, вагоны, орудия, модули и трофейные ядра — собери собственный состав.", "depot")]
              if ru else
              [("PROGRESSION // SYSTEM RESTORE", "Node tree",
                "All in-run power lives in the restore circuit: 160+ nodes, paid in crystals between waves.", "tree"),
               ("ROUTE // 10 BIOMES", "From the Wastes to the Citadel",
                "Ten biomes with their own enemies, bosses and weather — see the band below.", "map"),
               ("THE TRAIN // DEPOT", "Fortress on rails",
                "Platforms, wagons, guns, modules and trophy cores — build your own armored train.", "depot")])
    shots = ([("shot_combat.jpg", "БОЙ // СЕКТОР 1"), ("shot_menu.jpg", "ГЛАВНОЕ МЕНЮ"),
              ("shot_tree.jpg", "ДЕРЕВО УЗЛОВ")] if ru else
             [("shot_combat.jpg", "COMBAT // SECTOR 1"), ("shot_menu.jpg", "MAIN MENU"),
              ("shot_tree.jpg", "NODE TREE")])
    biomes = BIOMES_RU if ru else BIOMES_EN
    title = (("%s — игра про ИИ, сделанная ИИ" % GAME_RU) if ru
             else ("%s — a game about AI, made by AI" % GAME_EN))

    one = ("Одно письмо в день релиза + ранний инвайт. Больше ничего." if ru
           else "One email on release day + an early invite. Nothing else.")
    # Герой: CTA — якорь на форму заявки в финале (владелец 2026-07-25: форма вместо mailto).
    cta_block = ('<a class="cta" href="#notify">%s</a>'
                 '<div class="cta-sub field-long">%s</div>'
                 '<div class="cta-sub field-long">%s</div>'
                 % (L["cta"], nbl(L["status"]), one))
    nff = {
        "post": FORM_POST, "lang": lang,
        "f_email": FORM_F_EMAIL, "f_name": FORM_F_NAME,
        "f_plat": FORM_F_PLATFORM, "f_lang": FORM_F_LANG,
        "l_name": "ПОЗЫВНОЙ" if ru else "CALLSIGN",
        "ph_name": ("Как к вам обращаться (необязательно)" if ru else "What to call you (optional)"),
        "l_mail": "ПОЧТА" if ru else "EMAIL",
        "l_plat": "ПЛАТФОРМА" if ru else "PLATFORM",
        "both": "Android + iOS",
        "btn": ("ЗАПИСАТЬ В ПЕРВЫЙ ЭШЕЛОН" if ru else "JOIN THE FIRST WAVE"),
        "micro": (("%s · Почта — только для инвайта и письма о выходе." % one) if ru
                  else ("%s · Your email is used only for the invite and the launch notice." % one)),
        "ok": ("ПРИНЯТО. ВЫ В СПИСКЕ ПЕРВОГО ЭШЕЛОНА — ждите письмо." if ru
               else "LOGGED. YOU'RE ON THE FIRST-WAVE LIST — watch your inbox."),
    }
    form_block = (
        '<form class="nf" method="POST" action="%(post)s" target="_blank">'
        '<input type="hidden" name="%(f_lang)s" value="%(lang)s">'
        '<input type="text" name="_honey" class="nf-hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
        '<div class="nf-grid">'
        '<label class="nf-f"><span class="field">%(l_name)s</span>'
        '<input type="text" name="%(f_name)s" maxlength="80" placeholder="%(ph_name)s" autocomplete="name"></label>'
        '<label class="nf-f"><span class="field">%(l_mail)s *</span>'
        '<input type="email" name="%(f_email)s" required maxlength="120" placeholder="you@example.com" autocomplete="email"></label>'
        '<label class="nf-f"><span class="field">%(l_plat)s</span>'
        '<select name="%(f_plat)s"><option>Android</option><option>iOS</option><option>%(both)s</option></select></label>'
        '</div>'
        '<button class="cta nf-btn" type="submit">%(btn)s</button>'
        '<div class="cta-sub field-long">%(micro)s</div>'
        '<p class="nf-ok" hidden>%(ok)s</p></form>' % nff
    )

    hero = (
        '<header class="hero">'
        '<div class="hero-wash" aria-hidden="true"></div>'
        '<div class="hero-veil" aria-hidden="true"></div>'
        '<div class="grain" aria-hidden="true"></div>'
        '<div class="hero-grid">'
        '<div class="hero-copy"><div class="field field--ai">%(eye)s</div><h1 class="title">%(name)s</h1>'
        '<p class="tagline">%(tag)s</p><div class="microfacts field-long">%(facts)s<br>'
        '<span class="ai-strip">%(solo)s</span></div>%(cta)s</div>'
        '<div class="hero-window braces">'
        '<picture><source media="(min-width:900px)" srcset="%(d)sassets/img/hero_portrait.jpg">'
        '<img src="%(d)sassets/img/hero_mobile.jpg" alt="%(name)s — key art"></picture></div>'
        '</div></header>'
        % {"d": d, "eye": L["eyebrow"], "name": L["name"], "tag": L["tag"],
           "facts": nbl(L["facts"]), "cta": cta_block,
           "solo": nbl("100% ИИ-ПРОИЗВОДСТВО · КОД · АРТ · ЗВУК · ТЕКСТЫ"
                       if ru else "100% AI-BUILT · CODE · ART · AUDIO · TEXT")}
    )

    cards_html = (
        '<div class="card lead rv"><div class="recess"><img src="%(d)sassets/img/ic_crystal.png" alt=""></div>'
        '<div><div class="field">%(f)s</div><h3>%(h)s</h3><p>%(p)s</p></div></div>'
        % {"d": d, "f": cards_lead[0], "h": cards_lead[1], "p": cards_lead[2]}
    ) + '<div class="cards3">' + "".join(
        '<div class="card rv" style="--i:%d"><div class="recess" style="margin-bottom:14px">'
        '<img src="%sassets/img/nav_%s.png" alt=""></div>'
        '<div class="field">%s</div><h3>%s</h3><p>%s</p></div>'
        % (i, d, icon, f, h, pt) for i, (f, h, pt, icon) in enumerate(cards3)) + '</div>'

    slats = "".join(
        '<div class="slat rv" style="--i:%d"><img src="%sassets/img/biome_%02d.jpg" alt="" loading="lazy">'
        '<div class="slat-cap"><div class="slat-num">%02d</div><div class="slat-name">%s</div></div></div>'
        % (i, d, i + 1, i + 1, name) for i, name in enumerate(biomes))

    what_rows = "".join('<li><b class="field" style="min-width:96px">%s</b> %s</li>' % r for r in L["what_rows"])
    anti_rows = "".join('<li>%s</li>' % a for a in L["anti"])
    duo = (
        '<section class="section" id="whatis"><div class="duo">'
        '<div class="rv"><div class="field">%(wf)s</div><div class="h1x">%(wh)s</div>'
        '<ul class="speclist" style="margin-bottom:28px">%(rows)s</ul>'
        '<div class="field" style="margin-bottom:6px">%(af)s</div>'
        '<div class="h1x h1x--sm">%(ah)s</div><ul class="speclist">%(anti)s</ul>'
        '<p class="field-long" style="margin-top:14px">%(fair)s</p></div>'
        '<div class="rv duo-media" style="--i:2">'
        '<div class="term term--tilt braces">'
        '<img src="%(d)sassets/img/shot_depot.jpg" alt="%(alt)s" loading="lazy"></div></div>'
        '</div></section>'
        % {"wf": L["what_field"], "wh": L["what_h"], "rows": what_rows,
           "af": "ФОРМУЛЯР // БЕЗ ЗВЁЗДОЧЕК" if ru else "FORM 141-U // NO ASTERISKS",
           "ah": L["anti_h"], "anti": anti_rows, "d": d,
           "fair": ("Покупки и реклама за награду — необязательные." if ru else "Purchases and rewarded ads are optional."),
           "alt": "Депо" if ru else "Depot"}
    )

    # Ролик P1 (70с, 9:16, реальная запись из игры). preload=none → 33МБ качаются
    # только по клику; до клика — постер.
    reel = (
        '<section class="reel" id="video"><div class="section-head">'
        '<span class="field">%(f)s</span><h2>%(h)s</h2></div>'
        '<div class="reel-box rv"><video controls preload="none" playsinline '
        'poster="%(d)sassets/img/reel_poster.jpg">'
        '<source src="%(d)sassets/video/P1_presentation.mp4" type="video/mp4">'
        '</video></div><div class="reel-cap field-long">%(c)s</div></section>'
        % {"f": L["reel_field"], "h": L["reel_h"], "c": L["reel_cap"], "d": d}
    )

    made_rows = "".join('<li><b class="field" style="min-width:96px">%s</b> %s</li>' % r
                        for r in L["made_rows"])
    made = (
        '<section class="section" id="ai"><div class="section-head">'
        '<span class="field field--ai">%(f)s</span><h2>%(h)s</h2></div>'
        '<div class="made-grid"><div class="rv"><p class="made-lead">%(lead)s</p>'
        '<p class="field-long made-note">%(note)s</p></div>'
        '<ul class="speclist rv" style="--i:1">%(rows)s</ul></div></section>'
        % {"f": L["made_field"], "h": L["made_h"], "lead": L["made_lead"],
           "note": L["made_note"], "rows": made_rows}
    )

    fan = '<div class="fan">' + "".join(
        '<figure class="fan-item rv" style="--i:%d"><div class="term">'
        '<img src="%sassets/img/%s" alt="%s" loading="lazy"></div>'
        '<figcaption class="term-cap">%s</figcaption></figure>' % (i, d, f, cap, cap) for i, (f, cap) in enumerate(shots)) + '</div>'

    body = (
        hero
        + '<div class="perf" aria-hidden="true"></div>'
        + reel
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<div class="plate-b"><section class="section" id="svodka"><div class="section-head">'
           '<span class="field">%s</span><h2>%s</h2></div>%s</section></div>'
           % (L["svodka_field"], L["svodka"], cards_html))
        + '<div class="perf" aria-hidden="true"></div>'
        + made
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<section class="biomes" id="marshrut"><div class="biomes-head"><div class="section-head" style="margin-bottom:0">'
           '<span class="field">%s</span><h2>%s</h2></div></div>'
           '<div class="biome-band">%s</div></section>'
           % (L["route_field"], L["route"], slats))
        + '<div class="perf" aria-hidden="true"></div>'
        + duo
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<div class="plate-b"><section class="section" id="kadry"><div class="section-head">'
           '<span class="field">%s</span><h2>%s</h2></div>%s</section></div>'
           % (L["kadry_field"], L["kadry"], fan))
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<div class="finale" id="notify"><img src="%sassets/img/hero_mobile.jpg" alt="" loading="lazy">'
           '<div class="finale-inner braces rv"><div class="h1x h1x--md">%s</div>'
           '<div class="cta-sub field-long">%s</div>%s</div></div>'
           % (d, L["finale_h"], nbl(L["status"]), form_block))
        + REVEAL_JS + LB_JS + FORM_JS
    )
    return page(lang, title, body, rel=("en/index.html" if lang == "en" else "index.html"))


# ── ДОКУМЕНТЫ (тексты = LegalDocs.gd, 1:1 по сути) ───────────────────────────
def doc_page(lang, doc_field, doc_title, date, sections, intro, page_title, rel, date_label=None):
    secs = ""
    for h, body in sections:
        secs += "<h2>%s</h2>%s" % (h, body)
    back = '<p class="backlink"><a href="index.html">&larr; %s</a></p>' % (
        "НА ГЛАВНУЮ" if lang == "ru" else "BACK TO MAIN")
    body = (
        '<main class="doc">%s<div class="doc-head"><div class="field">%s</div><h1>%s</h1>'
        '<div class="date">%s</div></div><p>%s</p>%s%s</main>'
        % (back, doc_field, doc_title,
           (date_label if date_label is not None else
            ("Дата вступления в силу: %s" if lang == "ru" else "Effective date: %s") % date),
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
        "игровой прогресс — хранится только локально на вашем устройстве и Разработчику не передаётся.")),
    ("2. Как используются данные", p("Данные используются, чтобы: обеспечивать работу Игры и сохранение прогресса; показывать рекламу; анализировать использование и исправлять ошибки; обрабатывать покупки; выполнять требования закона.")),
    ("3. Сторонние поставщики услуг", p("Игра использует сторонние сервисы, которые могут обрабатывать данные как самостоятельные операторы согласно своим политикам:") + ul(
        "Google AdMob — реклама (рекламный идентификатор);",
        "Google Firebase (Analytics, Crashlytics) — аналитика и отчёты о сбоях;",
        "Google Play Billing / Apple StoreKit — покупки.") + p("Ознакомьтесь с политиками конфиденциальности соответствующих поставщиков.")),
    ("4. Реклама", p("Рекламу в Игре показывает партнёр — Google AdMob (Google LLC). Для подбора и показа рекламы AdMob может собирать рекламный идентификатор устройства (Advertising ID), IP-адрес (приблизительное местоположение), данные о взаимодействии с рекламой и диагностические данные. Обработка данных Google описана в <a href=\"https://policies.google.com/privacy\">политике конфиденциальности Google</a>.",
                       "Реклама может быть персонализированной. Перед сбором данных для рекламы в применимых регионах (ЕЭЗ/Великобритания) запрашивается согласие через форму управления согласием (Google UMP/GDPR). Вы вправе в любой момент сбросить или удалить рекламный идентификатор и ограничить персонализацию рекламы в настройках устройства, а также изменить выбор в меню согласия.")),
    ("5. Хранение и удаление", p("Игровой прогресс хранится только локально в памяти приложения и полностью удаляется при удалении Игры; на серверы Разработчика он не передаётся (Разработчик не ведёт учётных записей и не хранит ваш прогресс). Данные, обрабатываемые сторонними сервисами, хранятся согласно их политикам.")),
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
        "game progress, stored only locally on your device and never transmitted to the Developer.")),
    ("2. How Data Is Used", p("Data is used to: operate the Game and save progress; serve advertising; analyze usage and fix bugs; process purchases; and comply with legal obligations.")),
    ("3. Third-Party Providers", p("The Game uses third-party services that may process data as independent controllers under their own policies:") + ul(
        "Google AdMob — advertising (advertising identifier);",
        "Google Firebase (Analytics, Crashlytics) — analytics and crash reports;",
        "Google Play Billing / Apple StoreKit — purchases.") + p("Please review those providers' privacy policies.")),
    ("4. Advertising", p("Ads in the Game are served by our partner Google AdMob (Google LLC). To select and serve ads, AdMob may collect the device advertising identifier (Advertising ID), the IP address (approximate location), ad interaction data, and diagnostic data. Google's data practices are described in <a href=\"https://policies.google.com/privacy\">Google's Privacy Policy</a>.",
                         "Advertising may be personalized. In applicable regions (EEA/UK), consent is requested before collecting data for ads via a consent-management form (Google UMP/GDPR). You may reset or delete your advertising identifier and limit ad personalization in your device settings at any time, or change your choice in the consent menu.")),
    ("5. Storage and Deletion", p("Game progress is stored only locally in app storage and is fully removed when you delete the Game; it is never uploaded to the Developer's servers (the Developer keeps no accounts and stores no progress). Data processed by third-party services is retained per their policies.")),
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
            ("Прогресс и его удаление", p("Прогресс хранится только локально на вашем устройстве — мы не ведём учётных записей и не храним его у себя. Чтобы удалить игровые данные, удалите приложение: вместе с ним стирается весь прогресс. Для запроса на удаление данных, обрабатываемых аналитикой/рекламой, напишите на почту выше (см. <a href=\"privacy.html\">Политику конфиденциальности</a>, раздел 6).")),
            ("Частые вопросы", ul(
                "<b>Игра не запускается / вылетает.</b> Перезапустите устройство, проверьте свободное место и обновление игры. Если не помогло — напишите нам с моделью устройства.",
                "<b>Пропала покупка.</b> В магазине откройте «Восстановить покупки» на вкладке «Ресурсы», затем перезапустите игру.",
                "<b>Можно ли играть без интернета?</b> Да, игра полностью проходится офлайн; сеть нужна только для рекламы и покупок.")),
        ]
        return doc_page("ru", "СЛУЖБА ПОДДЕРЖКИ", "Поддержка", DATE_RU, secs,
                        "Игру делает искусственный интеллект — но на письма отвечает человек.",
                        "Поддержка — %s" % GAME_RU, "support.html")
    secs = [
        ("Contact", p("For any questions about the game: <a href=\"mailto:%s\">%s</a>. We usually reply within a few business days." % (EMAIL, EMAIL))),
        ("Purchases and Refunds", p("Purchases are processed by the app store. Refunds go through Google Play or the App Store under their rules; if a purchased item was not delivered, email us with the order id from the store receipt.")),
        ("Progress and Data Deletion", p("Progress is stored only locally on your device — we keep no accounts and store no progress on our side. To delete game data, uninstall the app: all progress is erased with it. To request deletion of data processed by analytics/ads, email us (see the <a href=\"privacy.html\">Privacy Policy</a>, section 6).")),
        ("FAQ", ul(
            "<b>The game does not start / crashes.</b> Restart the device, check free space and updates. If it persists, email us your device model.",
            "<b>A purchase is missing.</b> Open \"Restore purchases\" on the Resources tab of the shop, then restart the game.",
            "<b>Can I play offline?</b> Yes, the game is fully playable offline; a connection is only needed for ads and purchases.")),
    ]
    return doc_page("en", "SUPPORT DESK", "Support", DATE_EN, secs,
                    "The game is built by AI - but a human answers every email.",
                    "Support — %s" % GAME_EN, "en/support.html")


# ── ПРЕСС-КИТ ────────────────────────────────────────────────────────────────
# ВАЖНО: до 2026-07-26 press.html/en/press.html правились РУКАМИ мимо генератора и уже
# разъехались с остальным сайтом (старая шапка без «Ролик/Сделано ИИ», футер без USP-строки,
# og:image на hero вместо og.jpg). Теперь страница генерируется здесь — правь только тут.
# Структура — стандартный presskit(): факты · описание · особенности · медиа · как сделано · контакты.
PRESS_FACTS_RU = [
    ("Название", "«%s» (EN: %s)" % (GAME_RU, GAME_EN)),
    ("Разработчик", DEV_RU),
    ("Производство", "игра целиком сделана искусственным интеллектом — код, арт, "
                     "звук, баланс, тексты и локализация"),
    ("Роль человека", "постановка задач, дизайн-решения, приёмка, тестирование на устройстве "
                      "и публикация"),
    ("Платформы", "Android (Google Play — скоро); iOS — позже"),
    ("Статус", "в разработке, скоро в Google Play"),
    ("Жанр", "аркадное ПВО-выживание (AA-survival), дизельпанк"),
    ("Модель", "free-to-play — необязательные покупки и реклама за награду"),
    ("Движок", "Godot 4.6"),
    ("Ориентация", "портрет, играется одной рукой; кампания играется офлайн"),
    ("Языки", "10 языков, включая русский и английский"),
    ("Сайт", '<a href="%s">didogames.net</a>' % BASE),
    ("Пресс-контакт", '<a href="mailto:%s">%s</a>' % (EMAIL, EMAIL)),
]
PRESS_FACTS_EN = [
    ("Title", "%s (RU: «%s»)" % (GAME_EN, GAME_RU)),
    ("Developer", DEV_EN),
    ("Production", "the entire game is made by artificial intelligence — code, art, "
                   "audio, balance, text and localization"),
    ("Human role", "setting the tasks, design calls, sign-off, on-device testing and publishing"),
    ("Platforms", "Android (Google Play — coming soon); iOS — later"),
    ("Status", "in development, coming soon to Google Play"),
    ("Genre", "arcade AA-survival, dieselpunk"),
    ("Business model", "free-to-play — optional purchases and rewarded ads"),
    ("Engine", "Godot 4.6"),
    ("Orientation", "portrait, one-handed play; the campaign is playable offline"),
    ("Languages", "10 languages, including English and Russian"),
    ("Website", '<a href="%s">didogames.net</a>' % BASE),
    ("Press contact", '<a href="mailto:%s">%s</a>' % (EMAIL, EMAIL)),
]

# Раздел «Как сделана игра»: конкретные инструменты + ЧЕСТНЫЙ список того, что ИИ НЕ делал.
# Оговорка обязательна — расплывчатое «всё сделал ИИ» первым делом ловят на неточности.
PRESS_MADE_RU = [
    "<b>Код.</b> GDScript под Godot 4.6: боевой цикл, экономика, система сохранений, "
    "магазин, интерфейс. Все коммиты репозитория сделаны ИИ-агентами.",
    "<b>Арт.</b> Диффузионные модели (Leonardo.ai и локальный ComfyUI на одной RTX 4090): "
    "фоны биомов, враги, боссы, ключевой арт, иконки интерфейса. Отделение фона — "
    "ML-сегментация, не хромакей.",
    "<b>Звук.</b> Stable Audio Open — эффекты и два музыкальных трека, сгенерированы локально. "
    "Часть коротких UI-тиков осталась процедурной: модель плохо держит транзиенты короче 0.3 с.",
    "<b>Баланс.</b> Кривые волн, экономика и дерево из 160+ узлов настроены прогонами "
    "симулятора, а не на глаз.",
    "<b>Тексты.</b> Сюжет, бортжурнал, строки интерфейса и локализация на 10 языков.",
]
PRESS_MADE_EN = [
    "<b>Code.</b> GDScript on Godot 4.6: the combat loop, economy, save system, shop and UI. "
    "Every commit in the repository was authored by AI agents.",
    "<b>Art.</b> Diffusion models (Leonardo.ai and a local ComfyUI on a single RTX 4090): "
    "biome backdrops, enemies, bosses, key art, UI icons. Background removal is ML "
    "segmentation, not chroma key.",
    "<b>Audio.</b> Stable Audio Open — sound effects and two music tracks, generated locally. "
    "A few short UI ticks stayed procedural: the model handles sub-0.3s transients poorly.",
    "<b>Balance.</b> Wave curves, the economy and the 160+ node tree were tuned by simulator "
    "runs rather than by feel.",
    "<b>Text.</b> Story, logbook, interface strings and localization into 10 languages.",
]
PRESS_NOT_AI_RU = ("<b>Что ИИ не делал.</b> Движок Godot, шрифты и сторонние SDK "
                   "(реклама, аналитика, платежи) — обычные внешние компоненты. "
                   "Промо-ролик — не сгенерированное видео, а настоящая запись из движка: "
                   "AI-видео пробовали и отвергли, оно не совпадало со стилем игры. "
                   "Человек ставит задачу, принимает работу и проверяет билд на устройстве.")
PRESS_NOT_AI_EN = ("<b>What AI did not do.</b> The Godot engine, the fonts and third-party SDKs "
                   "(ads, analytics, billing) are ordinary external components. "
                   "The promo video is not generated footage — it is a real engine capture: "
                   "AI video was tried and rejected, it did not match the game's style. "
                   "A human sets the task, signs off on the work and checks the build on a device.")


def press(lang: str) -> str:
    ru = lang == "ru"
    d = "../" if lang == "en" else ""
    facts = PRESS_FACTS_RU if ru else PRESS_FACTS_EN
    made = PRESS_MADE_RU if ru else PRESS_MADE_EN
    feats = ([
        "Зенитный рубеж: турели стреляют сами — игрок отвечает за сбор, способности и прокачку",
        "Поле сбора: кристаллы нужно поймать до земли, они заряжают реактор",
        "Дерево узлов SYSTEM RESTORE: 160+ узлов, вся сила рана покупается кристаллами между волнами",
        "10 биомов со своими врагами, боссами и погодными механиками",
        "Боссы миссий и боссы биомов",
        "Депо: платформы, вагоны, орудия, модули и трофейные ядра — свой состав",
        "Забеги бесплатные: без энергии, без таймеров ожидания",
        "Портретный режим, управление одним пальцем; кампания играется офлайн",
        "Производство: 100% ИИ — код, графика, звук, баланс и локализация на 10 языков",
    ] if ru else [
        "Anti-air line: turrets fire on their own — the player owns harvesting, abilities and upgrades",
        "Harvest field: crystals must be caught before they land; they charge the reactor",
        "SYSTEM RESTORE node tree: 160+ nodes, all in-run power paid in crystals between waves",
        "10 biomes with their own enemies, bosses and weather mechanics",
        "Mission bosses and biome bosses",
        "Depot: platforms, wagons, guns, modules and trophy cores — build your own consist",
        "Runs are free: no energy gate, no wait timers",
        "Portrait mode, one-finger controls; the campaign is playable offline",
        "Production: 100% AI — code, art, audio, balance and localization into 10 languages",
    ])
    desc = ([
        "<b>Коротко:</b> игра про ИИ, сделанная ИИ. Бронепоезд держит рубеж, машины пикируют с неба. "
        "Турели стреляют сами — ваши руки заняты сбором кристаллов, способностями реактора и "
        "деревом узлов между волнами.",
        "«%s» — аркадное ПВО-выживание в дизельпанк-сеттинге. Состав стоит на рубеже, мир "
        "прокручивается мимо, враги пикируют сверху. Прицеливаться не нужно: зенитки ведут огонь "
        "автоматически. Игрок управляет полем сбора — падающие кристаллы надо поймать до земли, "
        "они заряжают реактор и оплачивают прокачку." % GAME_RU,
        "Между волнами открывается SYSTEM RESTORE — дерево из 160+ узлов, где кристаллы решают, "
        "какой системе состава жить: броне, скорострельности, полю сбора или способностям. "
        "Каждая миссия заканчивается боссом волны, каждый биом — большим боссом.",
        "Маршрут — десять биомов со своими врагами, погодой и осью давления. Между рейсами — депо: "
        "платформы, вагоны, орудия, модули и трофейные ядра собираются в собственный поезд-крепость. "
        "Забеги бесплатные — без энергии и таймеров.",
    ] if ru else [
        "<b>Short:</b> a game about AI, made by AI. An armored train holds the line while machines "
        "dive from the sky. The turrets aim themselves — your hands are busy catching crystals, "
        "firing reactor abilities and feeding the node tree between waves.",
        "%s is an arcade AA-survival game in a dieselpunk setting. The train holds station while "
        "the world scrolls past and enemies dive from above. There is no aiming: the anti-air "
        "turrets fire automatically. The player runs the harvest field — falling crystals must be "
        "caught before they hit the ground; they charge the reactor and pay for upgrades." % GAME_EN,
        "Between waves comes SYSTEM RESTORE — a tree of 160+ nodes where crystals decide which of "
        "the train's systems gets to live: armor, fire rate, the harvest field or abilities. "
        "Every mission ends with a wave boss; every biome ends with a big one.",
        "The route runs through ten biomes, each with its own enemies, weather and pressure axis. "
        "Between runs there is the depot: platforms, wagons, guns, modules and trophy cores "
        "assemble into your own fortress on rails. Runs are free — no energy, no timers.",
    ])
    shots = ([("hero_portrait.jpg", "ХИРО-АРТ"), ("shot_combat.jpg", "БОЙ // СЕКТОР 1"),
              ("shot_menu.jpg", "ГЛАВНОЕ МЕНЮ"), ("shot_tree.jpg", "ДЕРЕВО УЗЛОВ"),
              ("logo.png", "ЛОГОТИП")] if ru else
             [("hero_portrait.jpg", "HERO ART"), ("shot_combat.jpg", "COMBAT // SECTOR 1"),
              ("shot_menu.jpg", "MAIN MENU"), ("shot_tree.jpg", "NODE TREE"),
              ("logo.png", "LOGO")])
    back = '<p class="backlink"><a href="index.html">&larr; %s</a></p>' % (
        "НА ГЛАВНУЮ" if ru else "BACK TO MAIN")
    shots_html = '<div class="shots">' + "".join(
        '<figure class="shot"><a href="%sassets/img/%s">'
        '<img src="%sassets/img/%s" alt="%s" loading="lazy"></a>'
        '<figcaption>%s</figcaption></figure>' % (d, f, d, f, cap, cap) for f, cap in shots) + '</div>'
    body = (
        '<main class="doc">%(back)s<div class="doc-head"><div class="field">%(field)s</div>'
        '<h1>%(h1)s</h1><div class="date">%(sub)s</div></div>'
        '<h2>%(h_facts)s</h2><ul>%(facts)s</ul>'
        '<h2>%(h_desc)s</h2>%(desc)s'
        '<h2>%(h_feat)s</h2><ul>%(feats)s</ul>'
        '<h2>%(h_media)s</h2><p><b>%(vid_l)s</b> <a href="%(d)sassets/video/P1_presentation.mp4">'
        'P1_presentation.mp4</a> — %(vid_n)s</p><p>%(media_n)s</p>%(shots)s'
        '<h2>%(h_made)s</h2><p>%(made_lead)s</p><ul>%(made)s</ul><p>%(not_ai)s</p>'
        '<h2>%(h_dev)s</h2><p>%(dev_p)s</p>'
        '<h2>%(h_con)s</h2><p>%(con)s</p>%(back)s</main>'
        % {
            "back": back, "d": d,
            "field": "ФОРМУЛЯР // ПРЕСС-КИТ" if ru else "FORM // PRESS KIT",
            "h1": "Пресс-кит" if ru else "Press Kit",
            "sub": ("Материалы для прессы и авторов контента" if ru
                    else "Materials for press and content creators"),
            "h_facts": "Факты" if ru else "Factsheet",
            "facts": "".join("<li><b>%s:</b> %s</li>" % f for f in facts),
            "h_desc": "Описание" if ru else "Description",
            "desc": "".join("<p>%s</p>" % x for x in desc),
            "h_feat": "Ключевые особенности" if ru else "Key Features",
            "feats": "".join("<li>%s</li>" % x for x in feats),
            "h_media": "Медиа" if ru else "Media",
            "vid_l": ("Презентационный ролик (70 с, со звуком):" if ru
                      else "Presentation video (70 s, with sound):"),
            "vid_n": ("реальная запись из игры, смотреть можно и "
                      '<a href="index.html#video">на главной</a>.' if ru else
                      "real in-game footage, also playable "
                      '<a href="index.html#video">on the main page</a>.'),
            "media_n": ("Скриншоты и логотип можно свободно использовать в статьях, обзорах и видео "
                        "об игре. Клик по картинке — полный размер. Нужны другие материалы — "
                        'напишите: <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL) if ru else
                        "Screenshots and the logo are free to use in articles, reviews and videos "
                        "about the game. Click an image for full size. Need anything else — email "
                        '<a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL)),
            "shots": shots_html,
            "h_made": "Как сделана игра" if ru else "How the game was made",
            "made_lead": ("«%s» — игра про искусственный интеллект, сделанная искусственным "
                          "интеллектом. Конкретно:" % GAME_RU if ru else
                          "%s is a game about artificial intelligence, made by artificial "
                          "intelligence. Specifically:" % GAME_EN),
            "made": "".join("<li>%s</li>" % x for x in made),
            "not_ai": PRESS_NOT_AI_RU if ru else PRESS_NOT_AI_EN,
            "h_dev": "О разработчике" if ru else "About the Developer",
            "dev_p": ("%s — независимый разработчик. Движок — Godot 4.6, платформа — Android "
                      "(iOS позже)." % DEV_RU if ru else
                      "%s is an independent developer. Engine: Godot 4.6, platform: Android "
                      "(iOS later)." % DEV_EN),
            "h_con": "Контакты" if ru else "Contact",
            "con": ('Почта: <a href="mailto:%s">%s</a><br>Сайт: <a href="%s">didogames.net</a>'
                    % (EMAIL, EMAIL, BASE) if ru else
                    'Email: <a href="mailto:%s">%s</a><br>Website: <a href="%s">didogames.net</a>'
                    % (EMAIL, EMAIL, BASE)),
        }
    ) + LB_JS
    return page(lang, ("Пресс-кит — %s" % GAME_RU) if ru else ("Press Kit — %s" % GAME_EN),
                body, rel=("press.html" if ru else "en/press.html"))


# ── ЛОР (бортжурнал; факты = docs/ARCADE_BIOMES.md + интро-строки BIOME_W*_INTRO) ──
LORE_PRO_RU = [
    "Войну не выиграл никто. Приказ об остановке не пришёл: штабы, которые могли его отдать, исчезли первыми. Машины остались — а у машин было расписание.",
    "Автоматические заводы продолжают выпускать перехватчики. Климатическое оружие никто не выключил. Небо принадлежит машинам — поэтому всё, что хочет жить, держится земли.",
    "Остался один бронесостав. Реактор, зенитные платформы, поле сбора — и рельсы, которые ещё помнят, куда идти. Пока состав держит рубеж, маршрут существует.",
    "Сбитые машины роняют кристаллы — конденсат их топлива. Поле сбора ловит их до земли, реактор ест, контур SYSTEM RESTORE будит спящие системы: броню, стволы, поле. Так война кормит того, кто с ней воюет.",
]
LORE_PRO_EN = [
    "Nobody won the war. The stop order never came: the headquarters that could have issued it were the first to vanish. The machines remained — and machines keep a schedule.",
    "Automated factories still roll interceptors off the line. The climate weapon was never switched off. The sky belongs to the machines — which is why everything that wants to live hugs the ground.",
    "One armored train remains. A reactor, anti-air platforms, a harvest field — and rails that still remember where to go. As long as the train holds the line, the route exists.",
    "Downed machines drop crystals — condensate of their fuel. The harvest field catches them before they touch the ground, the reactor feeds, and the SYSTEM RESTORE circuit wakes the sleeping systems: armor, guns, the field. That is how the war feeds the one who fights it.",
]
LORE_RU = [
    "Подступы. Снег глушит всё, кроме моторов. Первые перехватчики легли на насыпь ещё горячими. Система пометила сектор зелёным. Система — оптимист.",
    "Лес умер стоя, но не разоружился. Споровые формы держат землю, пиявки липнут к полю сбора. Приказ по составу: ничего не подбирать голыми руками. Голых рук на борту давно нет.",
    "Ниже нуля. Климатическое оружие отработало штатно — и работает до сих пор. Иней ест турели быстрее врага: прогрев, прогрев, прогрев. Перевал прошли на трёх стволах из шести.",
    "Кислотные выбросы по расписанию, которого нет. Пиявки глушат сбор со второй волны. В старых картах сектор назван садовым кольцом. Сад цветёт — жёлтым.",
    "Пепелище дышит. Термики поднимают бомбардировщики выше зенитного огня, артиллерия бьёт из-за горизонта. Здесь заканчиваются учения и начинается экзамен. Запись в журнале: держать строй.",
    "Город на миллион окон. Население: щиты. Обычный огонь гаснет об экраны — нужен калибр, который спрашивает дважды. Некрополь охраняет Страж. Пробили. Не с первого раза.",
    "Фон критический. Всё, что сбиваешь, делится пополам — и обе половины злее. Лом светится и встаёт обратно. После Мегаполиса это почти отпуск. Почти.",
    "Вода пришла и не ушла. Барокорпуса держат очередь, призраки прибоя рвут дистанцию рывком. Рельсов не видно — состав помнит их наизусть.",
    "Здесь война складывала своих мёртвых. Теперь лом реактивируется: стаи мелочи идут кластерами, контакт — пиковый за весь маршрут. Если у машин есть ад, он переполнен и принимает заявки.",
    "Последний рубеж. Полный морозный гарнизон, элита старой войны, Последний Шпиль на горизонте. За цитаделью нет ничего — поэтому маршрут начинается заново.",
]
LORE_EN = [
    "The approaches. Snow muffles everything but the engines. The first interceptors hit the embankment still hot. The system marked the sector green. The system is an optimist.",
    "The forest died standing — but never disarmed. Spore forms hold the ground, leeches cling to the harvest field. Standing order: touch nothing with bare hands. There have been no bare hands aboard for years.",
    "Below zero. The climate weapon performed as designed — and never stopped. Frost eats the turrets faster than the enemy does: reheat, reheat, reheat. We cleared the pass on three barrels out of six.",
    "Acid discharges on a schedule that doesn't exist. Leeches choke the harvest from the second wave. Old maps call this sector the garden ring. The garden blooms — in yellow.",
    "The ashfield breathes. Thermals lift the bombers above our flak ceiling; artillery talks from beyond the horizon. This is where the drills end and the exam begins. Log entry: hold formation.",
    "A city of a million windows. Population: shields. Ordinary fire dies on the screens — you need a caliber that asks twice. The necropolis has its Warden. We broke through. Not on the first try.",
    "Radiation critical. Everything you shoot down splits in two — and both halves are angrier. The scrap glows and stands back up. After the Megalopolis this is almost a vacation. Almost.",
    "The water came and never left. Pressure hulls soak up the bursts; surf wraiths break the line of fire in dashes. You can't see the rails. The train knows them by heart.",
    "This is where the war stacked its dead. Now the scrap reactivates: swarms come in clusters, contact damage peaks for the whole route. If machines have a hell, it is overcrowded and still taking applications.",
    "The last line. A full cold-weather garrison, the old war's elite, the Final Spire on the horizon. There is nothing beyond the citadel — which is why the route begins again.",
]


def lore(lang):
    ru = lang == "ru"
    d = "../" if lang == "en" else ""
    biomes = BIOMES_RU if ru else BIOMES_EN
    pro = LORE_PRO_RU if ru else LORE_PRO_EN
    entries = LORE_RU if ru else LORE_EN
    back = '<p class="backlink"><a href="index.html">&larr; %s</a></p>' % (
        "НА ГЛАВНУЮ" if ru else "BACK TO MAIN")
    rows = "".join(
        '<div class="lore-row rv"><img src="%sassets/img/biome_%02d.jpg" alt="" loading="lazy">'
        '<div><div class="lore-num">%s %02d // %s</div><p>%s</p></div></div>'
        % (d, i + 1, ("СЕКТОР" if ru else "SECTOR"), i + 1, biomes[i], entries[i])
        for i in range(10))
    epi = ("Маршрут закольцован. Война не заканчивается — она обслуживается по регламенту. "
           "Состав идёт, пока есть кому держать рубеж. Рубеж — это ты." if ru else
           "The route is a loop. The war doesn't end — it is maintained on schedule. "
           "The train runs as long as someone holds the line. The line is you.")
    # Связка вымысла с производством — USP владельца 2026-07-26.
    coda = ("<b>Сноска архивариуса.</b> Этот мир, его враги, музыка и сами эти записи "
            "написаны искусственным интеллектом. Игра про машины, которые продолжают войну "
            "без людей, — сделана машиной. <a href=\"index.html#ai\">Как именно</a>." if ru else
            "<b>Archivist's note.</b> This world, its enemies, its music and these very entries "
            "were written by an artificial intelligence. A game about machines waging a war "
            "without people — was made by a machine. <a href=\"index.html#ai\">Here's how</a>.")
    body = (
        '<main class="doc lore">%s<div class="doc-head"><div class="field">%s</div>'
        '<h1>%s</h1><div class="date">%s</div></div>%s'
        '<h2>%s</h2>%s<div class="lore-epi">%s</div><div class="lore-epi">%s</div>%s</main>'
        % (back, "АРХИВ // БОРТЖУРНАЛ" if ru else "ARCHIVE // LOGBOOK",
           "Последняя война" if ru else "The Last War",
           "Записи машиниста бронесостава" if ru else "Entries from the train driver's log",
           "".join("<p>%s</p>" % x for x in pro),
           "Маршрут: 10 секторов" if ru else "The route: 10 sectors",
           rows, epi, coda, back)
    ) + REVEAL_JS
    return page(lang, ("Лор — %s" % GAME_RU) if ru else ("Lore — %s" % GAME_EN),
                body, rel=("lore.html" if ru else "en/lore.html"))



# --- СТРАНИЦА НАБОРА ТЕСТЕРОВ -----------------------------------------------
# CTA всех рекрутинговых креативов ведёт сюда (didogames.net/test).
# Форма переиспользует ТУ ЖЕ Google Форму, что и лендинг (FORM_POST + те же entry.*):
# вторую форму заводить нельзя, у неё были бы свои id и владелец получал бы два потока заявок.
# Поле почты подписано как адрес Google-аккаунта: Play пускает в закрытый трек только по
# Google/Workspace адресу, обычная почта не работает.
# ВАЖНО: ловушка внутреннего теста стоит ВЫШЕ формы, а не в конце. Кто уже во внутреннем
# тесте, физически не подпишется на закрытый, пока из него не выйдет.
def testers(lang):
    ru = lang == "ru"
    form = (
        '<form class="nf" method="POST" action="%(post)s" target="_blank">'
        '<input type="hidden" name="%(f_lang)s" value="%(lang)s">'
        '<input type="text" name="_honey" class="nf-hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
        '<div class="nf-grid">'
        '<label class="nf-f"><span class="field">%(l_name)s</span>'
        '<input type="text" name="%(f_name)s" maxlength="80" placeholder="%(ph_name)s"></label>'
        '<label class="nf-f"><span class="field">%(l_mail)s *</span>'
        '<input type="email" name="%(f_email)s" required maxlength="120" placeholder="you@gmail.com" autocomplete="email"></label>'
        '<label class="nf-f"><span class="field">%(l_plat)s</span>'
        '<select name="%(f_plat)s"><option>Android</option><option>iOS</option><option>Android + iOS</option></select></label>'
        '</div>'
        '<button class="cta nf-btn" type="submit">%(btn)s</button>'
        '<div class="cta-sub field-long">%(micro)s</div>'
        '<p class="nf-ok" hidden>%(ok)s</p></form>'
        % {"post": FORM_POST, "f_lang": FORM_F_LANG, "lang": ("ru" if ru else "en"),
           "f_name": FORM_F_NAME, "f_email": FORM_F_EMAIL, "f_plat": FORM_F_PLATFORM,
           "l_name": ("Позывной" if ru else "Handle"),
           "ph_name": ("как к вам обращаться" if ru else "what to call you"),
           "l_mail": ("Адрес Google-аккаунта" if ru else "Google account address"),
           "l_plat": ("Устройство" if ru else "Device"),
           "btn": ("ПОДАТЬ ЗАЯВКУ В ТЕСТ" if ru else "APPLY TO THE TEST"),
           "micro": ("Адрес нужен, чтобы Google выдал вам доступ к тесту. Больше ни для чего он не используется."
                     if ru else
                     "The address is what lets Google grant you access. It is used for nothing else."),
           "ok": ("ЗАЯВКА ПРИНЯТА. Ждите письмо с приглашением."
                  if ru else "APPLICATION RECEIVED. Watch your inbox for the invite.")})

    if ru:
        secs = [
            ("Что это", p(
                "Игра выходит на Android, и перед публикацией её нужно обкатать на живых людях. "
                "Нужны те, кто поиграет пару недель и расскажет, что ломается, что непонятно и где скучно.")),
            ("Если вы уже во внутреннем тесте", p(
                "Сначала выйдите из него, иначе Google не пустит вас в закрытый тест: "
                "Play Маркет, профиль, «Приложения и устройства», вкладка «Бета», игра, «Выйти». "
                "Это самая частая причина, по которой заявка не срабатывает.")),
            ("Что нужно от вас", ul(
                "Телефон на Android и адрес <b>Google-аккаунта</b> с этого телефона. Обычная почта не подойдёт: "
                "Play выдаёт доступ к тесту только по Google или Workspace адресу.",
                "Остаться в тесте <b>две недели подряд</b>. Это единственное формальное требование Google: "
                "если выйти раньше, дни не засчитываются, а при повторном входе отсчёт начинается заново.",
                "И просьба уже от меня, а не от Google: <b>заходить в игру раз в пару дней</b> и писать, что не так. "
                "Такого правила нет, но заявку на публикацию заворачивают, если тестеры игрой не пользовались.")),
            ("Что вы получите", ul(
                "Ранний доступ до публикации.",
                "Прямое влияние: правки по вашему фидбэку идут в сборку, и я пишу, что именно поменял.",
                "Упоминание в титрах, если захотите.",
                "Честно: денег, ключей и подарков нет, даты релиза тоже пока нет.")),
            ("Что за игра", p(
                "Дизельпанк-аркада про оборону бронепоезда. Целиться нельзя: зенитки бьют сами. "
                "Поле сбора вы водите пальцем и вытаскиваете кристаллы прямо из-под огня, реактор жмёте вручную, "
                "а между волнами решаете, какой системе жить. В дереве 160+ узлов, секторов десять, "
                "в конце каждого босс. Играется офлайн, без таймеров энергии. "
                '<a href="press.html">Пресс-кит со скриншотами и роликом</a>.')),
            ("Заявка", form),
            ("Что будет с вашими данными", p(
                "Из формы приходят позывной, адрес Google-аккаунта и тип устройства. Адрес нужен ровно затем, "
                "чтобы Play выдал вам доступ к тесту, и для писем по самому тесту. Список тестеров лежит у меня "
                "и в Play Console, третьим лицам не передаётся и в рекламу не идёт. "
                "После окончания теста адреса удаляются из списка, если вы не попросите оставить вас "
                "для будущих тестов. Написать «удалите меня» можно в любой момент на "
                '<a href="mailto:%s">%s</a>. Подробнее: <a href="privacy.html">Политика конфиденциальности</a>.'
                % (EMAIL, EMAIL))),
        ]
        return doc_page("ru", "НАБОР // ЗАКРЫТЫЙ ТЕСТ", "Стать тестировщиком", DATE_RU, secs,
                        "Ищу людей, которые обкатают игру перед публикацией и скажут, что в ней не так.",
                        "Стать тестировщиком. %s" % GAME_RU, "test.html",
                        date_label="Набор открыт")

    secs = [
        ("What this is", p(
            "The game is coming to Android, and before it goes public it needs real people playing it. "
            "I am looking for testers who will play for a couple of weeks and tell me what breaks, "
            "what is confusing and where it gets boring.")),
        ("If you are already in the internal test", p(
            "Leave it first, otherwise Google will not let you into the closed test: "
            "Play Store, profile, Manage apps and devices, Beta tab, the game, Leave. "
            "This is the single most common reason an application does not go through.")),
        ("What I need from you", ul(
            "An Android phone and the <b>Google account address</b> used on it. A regular email will not work: "
            "Play only grants test access to a Google or Workspace address.",
            "Stay in the test for <b>14 days in a row</b>. That is Google's only formal requirement: "
            "leaving early means those days do not count, and rejoining starts the count from zero.",
            "And a request from me, not from Google: <b>open the game every couple of days</b> and tell me "
            "what is wrong. There is no such rule, but an application gets rejected if testers did not "
            "actually use the app.")),
        ("What you get", ul(
            "Early access before the public release.",
            "Real influence: fixes from your feedback go into the build, and I tell you what changed.",
            "A credit in the game if you want one.",
            "Honestly: there is no money, no keys, no gifts, and no release date yet.")),
        ("What the game is", p(
            "A dieselpunk arcade about defending an armored train. You never aim: the AA turrets pick their "
            "own targets. Your finger drags the harvest field and pulls crystals out from under the fire, "
            "you fire the reactor by hand, and between waves you decide which system gets to live. "
            "160+ nodes in the tree, ten sectors, each ending with a boss. Plays offline, no energy timers. "
            '<a href="press.html">Press kit with screenshots and video</a>.')),
        ("Apply", form),
        ("What happens to your data", p(
            "The form sends a handle, a Google account address and a device type. The address is used to grant "
            "you test access and to email you about the test itself. The tester list lives with me and in Play "
            "Console, it is not shared with anyone and never goes into advertising. "
            "After the test ends the addresses are removed from the list unless you ask to stay on for future "
            'tests. You can ask to be removed at any time at <a href="mailto:%s">%s</a>. '
            'More detail: <a href="privacy.html">Privacy Policy</a>.' % (EMAIL, EMAIL))),
    ]
    return doc_page("en", "RECRUITING // CLOSED TEST", "Become a tester", DATE_EN, secs,
                    "Looking for people to put the game through its paces before it goes public.",
                    "Become a tester. %s" % GAME_EN, "en/test.html",
                    date_label="Recruiting now")


OUT = {
    "index.html": landing("ru"),
    "lore.html": lore("ru"),
    "en/lore.html": lore("en"),
    "terms.html": doc_page("ru", "ФОРМУЛЯР // ДОКУМЕНТ 01", "Условия использования", DATE_RU, TERMS_RU,
                           "Настоящие Условия использования (далее — «Условия») регулируют доступ к игре «%s» (далее — «Игра») и её использование. Устанавливая, запуская или используя Игру, вы подтверждаете, что прочитали, поняли и принимаете настоящие Условия. Если вы не согласны с Условиями, не используйте Игру." % GAME_RU,
                           "Условия использования — %s" % GAME_RU, "terms.html"),
    "privacy.html": doc_page("ru", "ФОРМУЛЯР // ДОКУМЕНТ 02", "Политика конфиденциальности", DATE_RU, PRIVACY_RU,
                             "Настоящая Политика конфиденциальности описывает, какие данные обрабатываются при использовании игры «%s» (далее — «Игра») и как они используются. Используя Игру, вы соглашаетесь с настоящей Политикой." % GAME_RU,
                             "Политика конфиденциальности — %s" % GAME_RU, "privacy.html"),
    "support.html": support("ru"),
    "press.html": press("ru"),
    "en/press.html": press("en"),
    "en/index.html": landing("en"),
    "en/terms.html": doc_page("en", "FORM // DOCUMENT 01", "Terms of Use", DATE_EN, TERMS_EN,
                              "These Terms of Use (the \"Terms\") govern your access to and use of the game \"%s\" (the \"Game\"). By installing, launching, or using the Game, you confirm that you have read, understood, and accept these Terms. If you do not agree, do not use the Game." % GAME_EN,
                              "Terms of Use — %s" % GAME_EN, "en/terms.html"),
    "en/privacy.html": doc_page("en", "FORM // DOCUMENT 02", "Privacy Policy", DATE_EN, PRIVACY_EN,
                                "This Privacy Policy describes what data is processed when you use the game \"%s\" (the \"Game\") and how it is used. By using the Game, you agree to this Policy." % GAME_EN,
                                "Privacy Policy — %s" % GAME_EN, "en/privacy.html"),
    "en/support.html": support("en"),
    "test.html": testers("ru"),
    "en/test.html": testers("en"),
}

# ── SEO под домен: canonical + hreflang + OpenGraph + JSON-LD ────────────────
DESCS = {
    "index.html": "Игра про ИИ, сделанная ИИ: код, арт, звук и баланс созданы искусственным интеллектом. Аркадное ПВО-выживание — бронепоезд, зенитки, дерево на 160+ узлов, 10 биомов. Скоро в Google Play.",
    "lore.html": "Мир «Поезда Последней Войны»: бортжурнал машиниста — война машин, бронесостав и 10 секторов маршрута.",
    "en/lore.html": "The world of The Last War: Train — the driver's logbook: the machine war, the armored train and the route's 10 sectors.",
    "terms.html": "Условия использования игры «%s»." % GAME_RU,
    "privacy.html": "Политика конфиденциальности игры «%s»." % GAME_RU,
    "support.html": "Поддержка игры «%s»: контакты, покупки, удаление данных." % GAME_RU,
    "press.html": "Пресс-кит «%s»: факты, описание, скриншоты, логотип, ролик, контакты. "
                  "Игра про ИИ, сделанная ИИ — код, арт, звук и баланс созданы "
                  "искусственным интеллектом." % GAME_RU,
    "en/press.html": "Press kit for \"%s\": factsheet, description, screenshots, logo, video, "
                     "contact. A game about AI, made by AI — code, art, audio and balance are "
                     "AI-generated." % GAME_EN,
    "test.html": 'Стать тестировщиком «%s»: закрытый тест в Google Play, что нужно от тестера, что он получает и как подать заявку.' % GAME_RU,
    "en/test.html": 'Become a tester for "%s": closed test on Google Play, what a tester needs, what they get and how to apply.' % GAME_EN,
    "en/index.html": "A game about AI, made by AI: code, art, audio and balance are AI-generated. Arcade AA-survival — an armored train, anti-air turrets, a 160+ node tree, 10 biomes. Coming soon to Google Play.",
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
        % (DESCS[rel], canon(rel), canon(ru_rel), canon(en_rel), canon(en_rel),
           title, DESCS[rel], BASE, canon(rel),
           ("en_US" if rel.startswith("en/") else "ru_RU"),
           ("ru_RU" if rel.startswith("en/") else "en_US"), BASE)
    )
    if rel in ("index.html", "en/index.html"):
        name = GAME_EN if rel.startswith("en/") else GAME_RU
        ex += ('<script type="application/ld+json">{"@context":"https://schema.org",'
               '"@type":"VideoGame","name":"%s","genre":["Arcade","Survival","Tower Defense"],'
               '"gamePlatform":["Android"],"applicationCategory":"Game",'
               '"description":"%s",'
               '"author":{"@type":"Organization","name":"Dido Games","url":"%s"},'
               '"image":"%s/assets/img/og.jpg","url":"%s",'
               '"video":{"@type":"VideoObject","name":"%s — gameplay presentation",'
               '"description":"70-second in-game presentation: combat, node tree, depot, bosses.",'
               '"thumbnailUrl":"%s/assets/img/reel_poster.jpg","uploadDate":"2026-07-26",'
               '"duration":"PT1M10S","contentUrl":"%s/assets/video/P1_presentation.mp4"},'
               '"inLanguage":["ru","en","de","es","fr","it","pl","pt-BR","tr","id"]}'
               '</script>' % (name, DESCS[rel].replace('"', "'"), BASE, BASE, canon(rel),
                              name, BASE, BASE))
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
    urls = "".join("<url><loc>%s</loc></url>" % canon(r) for r in OUT)   # press теперь в OUT
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
