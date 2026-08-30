# -*- coding: utf-8 -*-
"""Генератор статического сайта «Поезд Последней Войны» (site/*.html + site/en/*.html).
Правь тексты/константы здесь и перегенерируй:  python site/_build.py
Редизайн 2026-07-25 по брифам game-marketer + art-director (см. WORKLOG):
дуо-герой без апскейла, тестер-CTA (единственная оранж-доминанта), полоса 10 биомов
из готовых слоёв, anti-features, ретина-кадры в рамках «полевой терминал», scroll-reveal.
Тексты легалок = scripts/ui/legal/LegalDocs.gd (единый источник, суть 1:1; правки — синхронно!).
Godot папку не видит (site/.gdignore). Деплой: см. память site-deploy (subtree → didogames-site).

АКТУАЛИЗАЦИЯ 2026-08-30 (директива владельца №50, наряд W33-S). Сайт продавал механику,
которой в игре НЕТ: «вся сила рана — дерево на 160+ узлов, платишь кристаллами между волнами».
После директив №11 и №30 прогрессия в бою — КАРТОЧНЫЙ ДРАФТ, дерево покупается только вне боя,
забег = одна миссия. Переписаны: герой, сводка, новая секция #cards (лестницы орудий), «что это
за игра», пресс-кит, лор, страница теста, description/JSON-LD. EN-имена биомов сведены с
localization/en.po. Числа проверены по коду — адреса стоят рядом с каждым блоком; при следующей
правке сверять ТАМ ЖЕ, а не по этому файлу."""
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
# Закрытый тест: доступ выдаётся членством в открытой Google-группе, поэтому обе ссылки
# публичные и работают без участия владельца. Порядок жёсткий: opt-in не сработает, пока
# аккаунт не в группе. Ссылки живут здесь, а не в функциях страниц — их две страницы, и
# разъехавшийся адрес трека это отказ доступа, который увидят все.
GROUP_URL = "https://groups.google.com/g/lastwar-testers"
OPTIN_URL = "https://play.google.com/apps/testing/net.didogames.thelastwar"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&'
         'family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500&display=swap&subset=cyrillic"'
         ' rel="stylesheet">')

# Имена биомов = набор UI_BIOME_* (то, что игрок видит в меню/сторах; рекомендация АД).
BIOMES_RU = ["ЛЕДЯНЫЕ ПУСТОШИ", "МЁРТВЫЙ ЛЕС", "ГОРНЫЙ ПЕРЕВАЛ", "ТОКСИЧНАЯ ЗОНА",
             "ПЕПЕЛЬНАЯ ПУСТОШЬ", "МЁРТВЫЙ МЕГАПОЛИС", "РАДИОАКТИВНАЯ ПУСТЫНЯ",
             "ЗАТОПЛЕННАЯ ЗОНА", "КЛАДБИЩЕ МАШИН", "ЛЕДЯНАЯ ЦИТАДЕЛЬ"]
# EN-имена сверены с localization/en.po 2026-08-30 (UI_MAP_ICE_WASTES + UI_BIOME_2..10_NAME):
# сайт расходился с игрой в четырёх (DEAD FOREST / ASH WASTES / DEAD MEGALOPOLIS / ICE CITADEL).
BIOMES_EN = ["ICE WASTES", "FROZEN FOREST", "MOUNTAIN PASS", "TOXIC ZONE",
             "ASH WASTELAND", "DEAD MEGACITY", "RADIOACTIVE DESERT",
             "FLOODED ZONE", "MACHINE GRAVEYARD", "FROZEN CITADEL"]


def chrome_top(lang: str, depth: str, rel: str) -> str:
    game = GAME_RU if lang == "ru" else GAME_EN
    nav = {
        # #cards — секция карточной прокачки (директива №50: ядро игры сменилось, и вход в него
        # обязан быть в шапке, а не третьим экраном скролла). На мобильном .hdr-nav скрыт (CSS 930px).
        "ru": [("index.html#video", "Ролик"), ("index.html#cards", "Прокачка"),
               ("index.html#ai", "Сделано ИИ"),
               ("index.html#marshrut", "Маршрут"), ("lore.html", "Лор"), ("press.html", "Пресс-кит")],
        "en": [("index.html#video", "Trailer"), ("index.html#cards", "Upgrades"),
               ("index.html#ai", "Made by AI"),
               ("index.html#marshrut", "Route"), ("lore.html", "Lore"), ("press.html", "Press kit")],
    }[lang]
    base = rel[3:] if rel.startswith("en/") else rel
    if base == "index.html":   # на самом лендинге якоря — чистые # (без перезагрузки)
        links_prefix = ""
        nav = [(h.replace("index.html#", "#"), t) for h, t in nav]
    ru_href = (base if lang == "ru" else "../" + base)
    en_href = ("en/" + base if lang == "ru" else base)
    links = " ".join('<a href="%s">%s</a>' % (h, t) for h, t in nav)
    # Пока идёт закрытый тест, шапка ведёт в него, а не на подписку о выходе: игра уже
    # играбельна, и «сыграть сегодня» сильнее «сообщим когда-нибудь». После релиза вернуть #notify.
    hdr_cta = ('<a class="hdr-cta" href="test.html">%s</a>'
               % ('ИГРАТЬ В ТЕСТЕ' if lang == 'ru' else 'PLAY THE TEST'))
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


def page(lang: str, title: str, body: str, rel: str = "index.html", base_href: str = "") -> str:
    """base_href нужен ТОЛЬКО странице 404: хост отдаёт один и тот же файл на любой глубине,
    поэтому её относительные пути ломаются (на /en/чего-то стили и логотип уходили в 404,
    страница рендерилась голым HTML). <base> прибивает их к своему корню."""
    depth = "../" if rel.startswith("en/") else ""
    base_tag = ('<base href="%s">' % base_href) if base_href else ""
    return (
        '<!doctype html><html lang="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '%s'   # <base>, только для 404
        '<title>%s</title>'
        '<link rel="icon" type="image/png" href="%sassets/img/favicon.png">'
        '<link rel="apple-touch-icon" href="%sassets/img/touch_icon.png">'
        '%s<link rel="stylesheet" href="%sassets/style.css">'
        '<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)'
        'document.documentElement.classList.add("js")</script></head><body>'
        % (lang, base_tag, title, depth, depth, FONTS, depth)
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
        # ⚠️ Директива владельца №50: прогрессия в бою — КАРТЫ, а не дерево узлов (№11 + №30).
        # Дерево покупается только вне боя. Любая правка этих строк сверяется с кодом:
        # CardDefs.SIMPLE_MODEL_DEFAULT / STEMS / FORKS / PAIRS, ArcadeConfig.CARD_DRAFT_ENABLED.
        "tag": ("Целиться не нужно — зенитки бьют сами. Ты ловишь кристаллы под огнём, "
                "а на каждом новом ранге выбираешь карту: какое орудие встанет на состав "
                "и каким путём оно пойдёт дальше.") if ru else
               ("No aiming — the turrets handle that. You catch crystals under fire, and every "
                "time you rank up you pick a card: which gun joins the train, and which path "
                "it takes from here."),
        "facts": ("Бесплатно · дизельпанк ПВО-выживание · карточная прокачка прямо в бою · "
                  "9 орудий по 5 ступеней · 10 биомов · без энергии и таймеров")
                 if ru else
                 ("Free to play · dieselpunk AA-survival · card-draft upgrades mid-combat · "
                  "9 guns, 5 tiers each · 10 biomes · no energy, no timers"),
        "cta": "ВСТУПИТЬ В ЗАКРЫТЫЙ ТЕСТ" if ru else "JOIN THE CLOSED TEST",
        "status": ("СТАТУС: ИДЁТ ЗАКРЫТЫЙ ТЕСТ · GOOGLE PLAY (ANDROID) · iOS ПОЗЖЕ" if ru
                   else "STATUS: CLOSED TEST RUNNING · GOOGLE PLAY (ANDROID) · iOS LATER"),
        "svodka_field": "ФОРМУЛЯР 141-У" if ru else "FILE 141-U",
        "svodka": "СВОДКА" if ru else "OVERVIEW",
        "kadry_field": "АРХИВ ШТАБА" if ru else "HQ ARCHIVE",
        "kadry": "КАДРЫ" if ru else "SCREENS",
        "route_field": "МАРШРУТ // 10 СЕКТОРОВ" if ru else "THE ROUTE // 10 SECTORS",
        "route": "ОТ ПУСТОШЕЙ ДО ЦИТАДЕЛИ" if ru else "FROM THE WASTES TO THE CITADEL",
        "what_field": "РЕЖИМ // AA-SURVIVAL" if ru else "MODE // AA-SURVIVAL",
        "what_h": "Что это за игра" if ru else "What this game is",
        # ЦИКЛ/ЗАБЕГ — по коду: XP с киллов → ранг → окно карт (ArcadeCombat._open_level_session),
        # ран = одна миссия (BattleNodeTree.clear_run_levels в _complete_mission, директива №30).
        # ≈2 мин и ≈13 выборов — замер приёмки W28 (м1 106 с при подписанной полосе 110-129,
        # бюджет пиков м1 = 13, директива №42).
        "what_rows": [("РЕЖИМ" if ru else "MODE", "аркадное ПВО-выживание, портрет, одна рука" if ru
                       else "arcade AA-survival, portrait, one hand"),
                      ("ЦИКЛ" if ru else "LOOP", "сбил → ранг → выбор карты → следующая волна" if ru
                       else "shoot down → rank up → pick a card → next wave"),
                      ("ЗАБЕГ" if ru else "RUN", "одна миссия ≈ 2 минуты, около 13 выборов" if ru
                       else "one mission, ≈ 2 minutes, about 13 picks"),
                      ("МЕЖДУ" if ru else "BETWEEN", "депо и дерево узлов за кристаллы" if ru
                       else "the depot and the node tree, paid in crystals")],
        "anti_h": "Чего здесь нет" if ru else "What's not here",
        "anti": (["Энергии и таймеров ожидания", "Обязательного интернета — кампания играется офлайн",
                  "Платы за забеги — они бесплатные", "Рекламы посреди боя — только добровольная за бонус"]
                 if ru else
                 ["No energy, no wait timers", "No forced internet — the campaign plays offline",
                  "No paying per run — runs are free", "No mid-combat ads — rewarded only, always your choice"]),
        "finale_h": "СКОРО НА МАРШРУТЕ" if ru else "LAUNCHING SOON",
        "reel_field": "ЗАПИСЬ // 70 СЕКУНД" if ru else "FOOTAGE // 70 SECONDS",
        "reel_h": "ПОСМОТРЕТЬ, КАК ЭТО ИГРАЕТСЯ" if ru else "SEE HOW IT PLAYS",
        # ⚠️ МЕДИА К ЗАМЕНЕ (директива №50): P1_presentation.mp4 снят 2026-07 — в кадре
        # межволновое окно с офферами ДЕРЕВА, которого в игре больше нет (прогрессия = карты).
        # Подпись очищена от «дерева узлов», сам ролик перезаписывает отдельный наряд
        # с актуальной сборки. Не переписывать подпись обратно под старый монтаж.
        "reel_cap": ("Реальная запись из игры: бой, поле сбора, депо, боссы. "
                     "Со звуком." if ru else
                     "Real in-game footage: combat, harvest field, depot, bosses. "
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
                       ("БАЛАНС", "кривые волн, экономика, лестницы орудий и дерево узлов"),
                       ("ТЕКСТЫ", "сюжет, интерфейс и локализация на 10 языков")] if ru else
                      [("CODE", "combat loop, economy, saves, shop — in Godot"),
                       ("ART", "biome backdrops, enemies, key art, UI and icons"),
                       ("AUDIO", "sound effects and music"),
                       ("BALANCE", "wave curves, economy, the gun ladders and the node tree"),
                       ("TEXT", "story, interface and localization into 10 languages")]),
        "made_note": ("Человек ставит задачу и принимает работу. Всё остальное делает ИИ — "
                      "и об этом мы говорим прямо, а не мелким шрифтом." if ru else
                      "A human sets the task and signs off on the result. Everything else is done by AI — "
                      "and we say so up front, not in the fine print."),
        # ── СЕКЦИЯ КАРТОЧНОЙ ПРОКАЧКИ (директива №50) ───────────────────────────
        # КАЖДОЕ ЧИСЛО НИЖЕ — ИЗ КОДА, не из маркетинга:
        #   9 стволов ...... CardDefs.STEMS (8 вагонных + node_turret_loco, preinstalled)
        #   5 ступеней ..... CardDefs.STEM_MAX_LEVEL = 5, классы level_class()
        #                    МОНТАЖ / ЛИЦО / ПУТЬ / РОСТ ПУТИ / ПРЕДЕЛ
        #   27 путей ....... CardDefs.FORKS — 9 развилок × 3 пути (директива №46)
        #   9 обвязок ...... CardDefs.MODULES (passive: true), PASSIVE_STEPS = 3
        #   4 связки ....... CardDefs.PAIRS; сила — BattleNodeTree.PAIR_LINK_STEPS
        #                    [1.12, 1.20, 1.28] на порогах суммы уровней 4/6/8
        #   ~13 выборов .... бюджет пиков м1 (директива №42), замер приёмки W28. ТОЛЬКО «≈»:
    #                  пол пиков гаснет при глубине дерева ≥ 24 (ArcadeCombat._apply_xp_floor
    #                  :1842 → ArcadeConfig.XP_FLOOR_ACCOUNT_DEPTH := 24, :1794).
        "cards_field": "ПРОКАЧКА // КАРТОЧНЫЙ ДРАФТ" if ru else "PROGRESSION // CARD DRAFT",
        "cards_h": "Лестницы орудий" if ru else "The gun ladders",
        "cards_lead_p": ("Забег — это одна миссия, минуты на две. За сбитые машины растёт ранг, "
                         "на каждом ранге бой замирает и выкладывает <b>три карты</b>. Взял — видно "
                         "сразу: орудие приезжает на состав, меняет форму огня, открывает развилку. "
                         "Никаких «ещё плюс десять процентов» — каждая ступень делает что-то новое "
                         "на экране." if ru else
                         "A run is one mission, about two minutes long. Downed machines rank you up, "
                         "and every rank freezes the fight and deals <b>three cards</b>. Take one and "
                         "you see it immediately: a gun rolls onto the train, changes the shape of its "
                         "fire, opens a fork. No \"another plus ten percent\" — every tier does "
                         "something new on screen."),
        "cards_note": ("Дерево узлов никуда не делось — но живёт снаружи боя: кристаллы, добытые "
                       "в рейсе, тратятся на него между забегами. Две экономики не смешиваются." if ru else
                       "The node tree hasn't gone anywhere — it just lives outside combat: the crystals "
                       "you harvest on a run are spent there between runs. The two economies never mix."),
        "cards_rows": ([("9 ОРУДИЙ", "восемь вагонных и носовое орудие локомотива; носовое стоит с первой секунды миссии"),
                        ("5 СТУПЕНЕЙ", "у каждого ствола: монтаж, лицо, путь, рост пути, предел"),
                        ("27 ПУТЕЙ", "на третьей ступени ствол берёт одно из трёх направлений своей стихии; два других закрыты до конца миссии"),
                        ("9 ОБВЯЗОК", "по одной пассивной карте на орудие, со своей лестницей из трёх ступеней"),
                        ("4 СВЯЗКИ", "напарник напечатан на карте заранее; собрал пару — связка горит сама и метит снаряды обоих стволов общим ореолом"),
                        ("≈13 ВЫБОРОВ", "примерно столько решений умещается в одну двухминутную миссию")]
                       if ru else
                       [("9 GUNS", "eight wagon turrets plus the locomotive's nose gun; the nose gun is mounted from second one"),
                        ("5 TIERS", "on every gun: mount, signature, path, path growth, limit"),
                        ("27 PATHS", "at tier three a gun takes one of three directions in its own element; the other two stay shut for the rest of the mission"),
                        ("9 PASSIVES", "one passive card per gun, with its own three-step ladder"),
                        ("4 LINKS", "the partner is printed on the card in advance; collect the pair and the link ignites by itself, marking both guns' shots with a shared halo"),
                        ("≈13 PICKS", "roughly how many decisions fit into one two-minute mission")]),
    }
    cards_lead = (("ПОЛЕ СБОРА // РУКИ ИГРОКА", "Ловить, а не целиться",
                   "Кристаллы падают с неба и должны быть пойманы до земли. Промахнулся — "
                   "реактор не зарядится, а после боя не на что чинить состав.") if ru else
                  ("HARVEST FIELD // YOUR HANDS", "Catch, don't aim",
                   "Crystals fall from the sky and have to be caught before they hit the ground. "
                   "Miss them and the reactor stays cold — and after the run there is nothing "
                   "to repair the train with."))
    # ⚠️ №11 + №30: дерево узлов покупается ТОЛЬКО вне боя (мета-экран NodeTreeScreen), а в депо
    # орудия НЕ ставятся — турельная половина лоадаута погашена при живом драфте
    # (LoadoutScreen._turret_slots_ui = not ArcadeConfig.draft_enabled()). Не возвращать «орудия»
    # в карточку депо и «вся сила рана» — в карточку дерева.
    cards3 = ([("МЕЖДУ ЗАБЕГАМИ // ДЕРЕВО", "Дерево узлов",
                "Покупается кристаллами вне боя: броня, скорострельность, поле сбора, глубина связок. "
                "В самом бою дерево не трогаешь — там карты.", "tree"),
               ("МАРШРУТ // 10 БИОМОВ", "От Пустошей до Цитадели",
                "Десять биомов со своими врагами, боссами и погодой — полоса ниже.", "map"),
               ("СОСТАВ // ДЕПО", "Поезд-крепость",
                "Локомотив, вагоны со способностями реактора, модули и трофейные ядра. "
                "Орудия сюда не ставятся — они приходят картами в бою.", "depot")]
              if ru else
              [("BETWEEN RUNS // THE TREE", "Node tree",
                "Bought with crystals outside combat: armor, fire rate, the harvest field, the depth "
                "of gun links. During a run you never touch the tree — that's what the cards are for.", "tree"),
               ("ROUTE // 10 BIOMES", "From the Wastes to the Citadel",
                "Ten biomes with their own enemies, bosses and weather — see the band below.", "map"),
               ("THE TRAIN // DEPOT", "Fortress on rails",
                "A locomotive, wagons carrying reactor abilities, modules and trophy cores. "
                "Guns are not mounted here — they arrive as cards, mid-battle.", "depot")])
    # ⚠️ КАДРЫ К ЗАМЕНЕ (директива №50, снимает отдельный наряд с актуальной сборки):
    #   shot_tree.jpg  — дерево ДО раскладки W30 (87 пересечений рёбер вылечены в 0);
    #                    подпись уточнена, чтобы кадр не читался как прокачка внутри боя.
    #   shot_combat.jpg / shot_depot.jpg — сняты до карточной прокачки и до гашения
    #                    турельной половины депо. Просится четвёртый кадр — окно ВЫБОР ПУТИ.
    shots = ([("shot_combat.jpg", "БОЙ // СЕКТОР 1"), ("shot_menu.jpg", "ГЛАВНОЕ МЕНЮ"),
              ("shot_tree.jpg", "ДЕРЕВО УЗЛОВ // МЕЖДУ ЗАБЕГАМИ")] if ru else
             [("shot_combat.jpg", "COMBAT // SECTOR 1"), ("shot_menu.jpg", "MAIN MENU"),
              ("shot_tree.jpg", "NODE TREE // BETWEEN RUNS")])
    biomes = BIOMES_RU if ru else BIOMES_EN
    title = (("%s — игра про ИИ, сделанная ИИ" % GAME_RU) if ru
             else ("%s — a game about AI, made by AI" % GAME_EN))

    one = ("Одно письмо в день релиза. Больше ничего." if ru
           else "One email on release day. Nothing else.")
    # Герой: CTA ведёт на /test — доступ в закрытый трек самообслуживание, письма ждать не надо.
    # Форма о выходе осталась вторым путём: для iOS и для тех, кто не хочет тестировать.
    join_sub = ('Android, бесплатно, три шага. Не сейчас? <a href="#notify">Сообщу о выходе</a>.'
                if ru else
                'Android, free, three steps. Not now? <a href="#notify">Get the launch email</a>.')
    cta_block = ('<a class="cta" href="test.html">%s</a>'
                 '<div class="cta-sub field-long">%s</div>'
                 '<div class="cta-sub field-long">%s</div>'
                 % (L["cta"], nbl(L["status"]), join_sub))
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
        "micro": (("%s · Почта нужна только для письма о выходе." % one) if ru
                  else ("%s · Your email is used only for the launch notice." % one)),
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

    # Секция карточной прокачки — то, чем игра стала после директив №11/№30/№41/№46.
    # Каркас переиспользован у «Сделано ИИ» (made-grid + speclist): своих CSS-правил не заводит.
    # Ярлык + текст ОДНИМ <span>: .speclist li — flex-контейнер, и каждый инлайновый кусок стал бы
    # отдельной колонкой (та же гоча, что в секции join ниже). 96px хватает самому длинному
    # ярлыку набора: «≈13 ВЫБОРОВ» — 11 знаков mono-12 с трекингом .16em ≈ 100px (W36: ярлык
    # вырос с «13 ВЫБОРОВ», min-width поднят 96→104px, иначе строка ломает выравнивание).
    cards_rows = "".join('<li><b class="field" style="min-width:104px">%s</b><span>%s</span></li>' % r
                         for r in L["cards_rows"])
    cards_sec = (
        '<section class="section" id="cards"><div class="section-head">'
        '<span class="field">%(f)s</span><h2>%(h)s</h2></div>'
        '<div class="made-grid"><div class="rv"><p class="made-lead">%(lead)s</p>'
        '<p class="field-long made-note">%(note)s</p></div>'
        '<ul class="speclist rv" style="--i:1">%(rows)s</ul></div></section>'
        % {"f": L["cards_field"], "h": L["cards_h"], "lead": L["cards_lead_p"],
           "note": L["cards_note"], "rows": cards_rows}
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

    # Вход в тест прямо на лендинге: обе ссылки здесь, чтобы человек с телефона не ходил на
    # вторую страницу. Оговорки стоят ВЫШЕ ссылок — если нажать раньше, чем сменить аккаунт
    # или выйти из внутреннего теста, игра просто не появится, и человек уходит навсегда.
    join_rows = ([("ШАГ 1", 'Вступить в <a href="%s" target="_blank" rel="noopener">группу '
                            'тестировщиков</a> в Google Группах. Она открытая, одобрение не нужно.' % GROUP_URL),
                  ("ШАГ 2", 'Согласиться на участие: '
                            '<a href="%s" target="_blank" rel="noopener">страница теста в Google Play</a>. '
                            'Обязательно тем же аккаунтом.' % OPTIN_URL),
                  ("ШАГ 3", "Установить игру из Google Play по ссылке с той же страницы. "
                            "Доступ появляется не мгновенно.")]
                 if ru else
                 [("STEP 1", 'Join the <a href="%s" target="_blank" rel="noopener">tester group</a> '
                             'on Google Groups. It is open, no approval needed.' % GROUP_URL),
                  ("STEP 2", 'Opt in to the test: '
                             '<a href="%s" target="_blank" rel="noopener">the test page on Google Play</a>. '
                             'Same account, always.' % OPTIN_URL),
                  ("STEP 3", "Install from Google Play through the link on that page. "
                             "Access does not appear instantly.")])
    join = (
        '<section class="section" id="test"><div class="section-head">'
        '<span class="field">%(f)s</span><h2>%(h)s</h2></div>'
        '<div class="made-grid"><div class="rv"><p class="made-lead">%(lead)s</p>'
        '<p class="field-long made-note">%(warn)s</p>'
        '<a class="cta" href="test.html" style="margin-top:20px">%(cta)s</a></div>'
        '<ul class="speclist rv" style="--i:1">%(rows)s</ul></div></section>'
        % {"f": "ДОСТУП // ОТКРЫТ" if ru else "ACCESS // OPEN",
           "h": "Играть можно уже сейчас" if ru else "You can play it right now",
           "lead": ("Игра идёт в <b>закрытом тесте Google Play</b> на Android. Вход "
                    "самостоятельный: писем ждать не нужно, вы вступаете сами и играете сегодня."
                    if ru else
                    "The game is running in a <b>Google Play closed test</b> on Android. Access is "
                    "self-service: there is no invite to wait for, you join yourself and play today."),
           "warn": ("Два условия, без которых игру вы не увидите. Первое: все шаги делайте тем же "
                    "Google-аккаунтом, под которым залогинены в Play Маркете на телефоне. Второе: "
                    "если вы уже во внутреннем тесте, сначала выйдите из него, иначе закрытый трек "
                    "вам не покажут."
                    if ru else
                    "Two conditions, or the game will not show up. One: do every step with the same "
                    "Google account you are signed in with in the Play Store on your phone. Two: if "
                    "you are already in the internal test, leave it first, or the closed track stays "
                    "hidden."),
           "cta": "ПОДРОБНО ПРО ТЕСТ" if ru else "MORE ABOUT THE TEST",
           # Текст строки обязан быть ОДНИМ элементом: .speclist li это flex-контейнер, и каждый
           # инлайновый кусок (текст, ссылка, снова текст) стал бы отдельной колонкой. У соседних
           # списков ссылок внутри нет, поэтому они и не ломались.
           "rows": "".join('<li><b class="field" style="min-width:96px">%s</b><span>%s</span></li>' % r
                           for r in join_rows)}
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
        + cards_sec
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
        + join
        + '<div class="perf" aria-hidden="true"></div>'
        + ('<div class="finale" id="notify"><img src="%sassets/img/hero_mobile.jpg" alt="" loading="lazy">'
           '<div class="finale-inner braces rv"><div class="h1x h1x--md">%s</div>'
           '<div class="cta-sub field-long">%s</div>%s</div></div>'
           % (d, L["finale_h"],
              ("Форма не про тест: она для тех, у кого iPhone, и для тех, кто просто хочет узнать "
               "о релизе. Доступ в тест открывается тремя шагами выше." if ru else
               "This form is not the test: it is for iPhone owners and for anyone who just wants the "
               "launch notice. Test access comes from the three steps above."),
              form_block))
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
                "<b>Можно ли играть без интернета?</b> Да, игра полностью проходится офлайн; сеть нужна только для рекламы и покупок.",
                "<b>Не вижу игру в Google Play, хотя вступил в тест.</b> Почти всегда дело в аккаунте: вступление в группу и согласие на тест должны быть сделаны тем же Google-аккаунтом, под которым вы залогинены в Play Маркете на телефоне. Если аккаунт тот же, просто подождите: доступ выдаётся не мгновенно, обновите страницу магазина позже. Отдельный случай: если вы состоите во внутреннем тесте этой же игры, закрытый трек вам не покажут, пока вы из внутреннего не выйдете. Все условия и ссылки: <a href=\"test.html\">страница закрытого теста</a>.")),
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
            "<b>Can I play offline?</b> Yes, the game is fully playable offline; a connection is only needed for ads and purchases.",
            "<b>I joined the test but the game is not in Google Play.</b> Almost always it is the account: joining the group and opting in must be done with the same Google account you are signed in with in the Play Store on your phone. If the account is right, just wait: access does not open instantly, reload the store page later. Separate case: if you are in the internal test of this same game, the closed track stays hidden until you leave it. All the rules and links: <a href=\"test.html\">the closed test page</a>.")),
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
    ("Платформы", "Android (Google Play); iOS — позже"),
    ("Статус", "идёт закрытое тестирование в Google Play, дата релиза не назначена"),
    ("Как попробовать", 'закрытый тест открыт для всех: <a href="test.html">условия и ссылки</a>'),
    ("Жанр", "аркадное ПВО-выживание (AA-survival) с карточным драфтом, дизельпанк"),
    ("Забег", "одна миссия ≈ 2 минуты; около 13 выборов карт за миссию"),
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
    ("Platforms", "Android (Google Play); iOS — later"),
    ("Status", "in closed testing on Google Play, release date not announced"),
    ("How to try it", 'the closed test is open to anyone: <a href="test.html">rules and links</a>'),
    ("Genre", "arcade AA-survival with a card draft, dieselpunk"),
    ("Run length", "one mission ≈ 2 minutes; about 13 card picks per mission"),
    ("Business model", "free-to-play — optional purchases and rewarded ads"),
    ("Engine", "Godot 4.6"),
    ("Orientation", "portrait, one-handed play; the campaign is playable offline"),
    ("Languages", "10 languages, including English and Russian"),
    ("Website", '<a href="%s/en/">didogames.net</a>' % BASE),
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
    "<b>Баланс.</b> Кривые волн, экономика, лестницы орудий и дерево узлов настроены "
    "прогонами симулятора, а не на глаз: каждое решение по числам — десятки прогонов миссии.",
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
    "<b>Balance.</b> Wave curves, the economy, the gun ladders and the node tree were tuned by "
    "simulator runs rather than by feel — every number is backed by dozens of mission runs.",
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
        "Зенитный рубеж: турели стреляют сами — игрок отвечает за сбор, способности и выбор карт",
        "Поле сбора: кристаллы нужно поймать до земли, они заряжают реактор",
        "Карточный драфт в бою: ранг за сбитых, на каждом ранге бой замирает и выкладывает три карты",
        "Лестницы орудий: 9 стволов, у каждого 5 ступеней — монтаж, лицо, путь, рост пути, предел",
        "27 путей: на третьей ступени ствол выбирает одно из трёх направлений своей стихии, два других закрываются до конца миссии",
        "9 пассивных обвязок — по одной на орудие, со своей лестницей",
        "4 связки: напарник напечатан на карте заранее, связка загорается сама и растёт от уровней обоих стволов",
        "Забег = одна миссия ≈ 2 минуты, около 13 выборов",
        "Дерево узлов — вне боя: кристаллы рейса тратятся между забегами, в бою дерево недоступно",
        "10 биомов со своими врагами, боссами и погодными механиками",
        "Боссы миссий и боссы биомов",
        "Депо: локомотив, вагоны со способностями реактора, модули и трофейные ядра",
        "Забеги бесплатные: без энергии, без таймеров ожидания",
        "Портретный режим, управление одним пальцем; кампания играется офлайн",
        "Производство: 100% ИИ — код, графика, звук, баланс и локализация на 10 языков",
    ] if ru else [
        "Anti-air line: turrets fire on their own — the player owns harvesting, abilities and card picks",
        "Harvest field: crystals must be caught before they land; they charge the reactor",
        "In-combat card draft: kills give rank, every rank freezes the fight and deals three cards",
        "Gun ladders: 9 guns, 5 tiers each — mount, signature, path, path growth, limit",
        "27 paths: at tier three a gun picks one of three directions in its own element; the other two close for the rest of the mission",
        "9 passive rigs — one per gun, each with its own ladder",
        "4 links: the partner is printed on the card in advance; the link ignites by itself and grows with both guns' tiers",
        "A run is one mission: ≈ 2 minutes, about 13 picks",
        "The node tree lives outside combat: run crystals are spent between runs, never during one",
        "10 biomes with their own enemies, bosses and weather mechanics",
        "Mission bosses and biome bosses",
        "Depot: a locomotive, wagons carrying reactor abilities, modules and trophy cores",
        "Runs are free: no energy gate, no wait timers",
        "Portrait mode, one-finger controls; the campaign is playable offline",
        "Production: 100% AI — code, art, audio, balance and localization into 10 languages",
    ])
    desc = ([
        "<b>Коротко:</b> игра про ИИ, сделанная ИИ. Бронепоезд держит рубеж, машины пикируют с неба. "
        "Турели стреляют сами — ваши руки заняты сбором кристаллов, способностями реактора и "
        "выбором карт: каждый ранг предлагает три, взять можно одну.",
        "«%s» — аркадное ПВО-выживание в дизельпанк-сеттинге. Состав стоит на рубеже, мир "
        "прокручивается мимо, враги пикируют сверху. Прицеливаться не нужно: зенитки ведут огонь "
        "автоматически. Игрок управляет полем сбора — падающие кристаллы надо поймать до земли, "
        "они заряжают реактор." % GAME_RU,
        "Прокачка внутри боя — карточная. Забег равен одной миссии (около двух минут), за сбитые "
        "машины растёт ранг, каждый ранг замирает бой и выкладывает три карты; за миссию таких "
        "решений примерно тринадцать. Карты — это лестницы орудий: девять стволов, у каждого пять "
        "ступеней (монтаж, лицо, путь, рост пути, предел), и ни одна из них не «ещё плюс десять "
        "процентов» — каждая меняет то, что видно на экране. На третьей ступени ствол выбирает "
        "одно из трёх направлений своей стихии, два других закрываются до конца миссии. Плюс "
        "девять пассивных обвязок и четыре связки, которые загораются сами, когда на составе "
        "встречаются два напарника.",
        "Дерево узлов осталось, но живёт вне боя: собранные в рейсе кристаллы тратятся на него "
        "между забегами. Маршрут — десять биомов со своими врагами, погодой и осью давления, "
        "каждая миссия кончается боссом волны, каждый биом — большим боссом. В депо собирается "
        "состав: локомотив, вагоны со способностями реактора, модули и трофейные ядра. Орудия "
        "в депо не ставятся — они приходят картами в бою. Забеги бесплатные, без энергии и таймеров.",
    ] if ru else [
        "<b>Short:</b> a game about AI, made by AI. An armored train holds the line while machines "
        "dive from the sky. The turrets aim themselves — your hands are busy catching crystals, "
        "firing reactor abilities and picking cards: every rank offers three, you take one.",
        "%s is an arcade AA-survival game in a dieselpunk setting. The train holds station while "
        "the world scrolls past and enemies dive from above. There is no aiming: the anti-air "
        "turrets fire automatically. The player runs the harvest field — falling crystals must be "
        "caught before they hit the ground; they charge the reactor." % GAME_EN,
        "In-run progression is a card draft. A run is one mission (about two minutes); downed "
        "machines raise your rank, every rank freezes the fight and deals three cards, and a "
        "mission holds roughly thirteen such decisions. The cards are gun ladders: nine guns with "
        "five tiers each (mount, signature, path, path growth, limit), and not one of them is "
        "\"another plus ten percent\" — every tier changes something you can see. At tier three a "
        "gun picks one of three directions in its own element, and the other two close for the "
        "rest of the mission. On top of that: nine passive rigs and four links that ignite by "
        "themselves once two partner guns share the train.",
        "The node tree is still there, but it lives outside combat: the crystals you harvest are "
        "spent on it between runs. The route covers ten biomes, each with its own enemies, weather "
        "and pressure axis; every mission ends with a wave boss and every biome with a big one. "
        "The depot builds the train: a locomotive, wagons carrying reactor abilities, modules and "
        "trophy cores. Guns are not mounted there — they arrive as cards, mid-battle. Runs are "
        "free — no energy, no timers.",
    ])
    # ⚠️ Те же кадры к замене, что и на лендинге (директива №50) — см. комментарий в landing().
    # В пресс-кит после пересъёмки просится кадр окна выбора карты и окна ВЫБОР ПУТИ:
    # сейчас у прессы нет НИ ОДНОГО кадра главной механики игры.
    shots = ([("hero_portrait.jpg", "ХИРО-АРТ"), ("shot_combat.jpg", "БОЙ // СЕКТОР 1"),
              ("shot_menu.jpg", "ГЛАВНОЕ МЕНЮ"), ("shot_tree.jpg", "ДЕРЕВО УЗЛОВ // МЕЖДУ ЗАБЕГАМИ"),
              ("logo.png", "ЛОГОТИП")] if ru else
             [("hero_portrait.jpg", "HERO ART"), ("shot_combat.jpg", "COMBAT // SECTOR 1"),
              ("shot_menu.jpg", "MAIN MENU"), ("shot_tree.jpg", "NODE TREE // BETWEEN RUNS"),
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
                    'Email: <a href="mailto:%s">%s</a><br>Website: <a href="%s/en/">didogames.net</a>'
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
    "Сбитые машины роняют кристаллы — конденсат их топлива. Поле сбора ловит их до земли, реактор ест. Чем больше состав сбивает, тем выше его боевой ранг — и на каждом ранге система выкладывает три предписания: какое орудие поднять из трюма, каким путём его вести, что закрыть навсегда. Одно берётся, два сгорают. Так война кормит того, кто с ней воюет.",
    "Предписания живут ровно один рейс. Что осталось после — кристаллы в трюме; их состав тратит в депо, между рейсами, на то, что уже не сгорит.",
]
LORE_PRO_EN = [
    "Nobody won the war. The stop order never came: the headquarters that could have issued it were the first to vanish. The machines remained — and machines keep a schedule.",
    "Automated factories still roll interceptors off the line. The climate weapon was never switched off. The sky belongs to the machines — which is why everything that wants to live hugs the ground.",
    "One armored train remains. A reactor, anti-air platforms, a harvest field — and rails that still remember where to go. As long as the train holds the line, the route exists.",
    "Downed machines drop crystals — condensate of their fuel. The harvest field catches them before they touch the ground, and the reactor feeds. The more the train kills, the higher its combat rank — and at every rank the system issues three orders: which gun to raise from the hold, which path to take it down, what to close off for good. You take one; the other two burn. That is how the war feeds the one who fights it.",
    "The orders last exactly one run. What survives it are the crystals in the hold — spent at the depot, between runs, on the things that do not burn.",
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
    "Последний рубеж. Полный морозный гарнизон, элита старой войны, Последний Шпиль на горизонте. За цитаделью нет ничего: маршрут кончается здесь.",
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
    "The last line. A full cold-weather garrison, the old war's elite, the Final Spire on the horizon. There is nothing beyond the citadel: the route ends here.",
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
    epi = ("Десять секторов, сто миссий. Война не заканчивается — она обслуживается по регламенту. "
           "Состав идёт, пока есть кому держать рубеж. Рубеж — это ты." if ru else
           "Ten sectors, a hundred missions. The war doesn't end — it is maintained on schedule. "
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
    # Локальный нумерованный список: глобальный ресет обнуляет padding, а .doc ol в CSS нет,
    # поэтому отступ под цифры задаётся здесь.
    def steps(*items):
        return ('<ol style="padding-left:22px;margin:10px 0">%s</ol>'
                % "".join("<li>%s</li>" % i for i in items))

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
           "btn": ("ОСТАВИТЬ КОНТАКТ" if ru else "LEAVE YOUR CONTACT"),
           "micro": ("Адрес нужен, чтобы я мог связаться с вами по ходу теста. Больше ни для чего он не используется."
                     if ru else
                     "The address is how I reach you during the test. It is used for nothing else."),
           "ok": ("КОНТАКТ ПРИНЯТ. Доступ открывается по трём шагам выше."
                  if ru else "CONTACT RECEIVED. Access comes from the three steps above.")})

    if ru:
        secs = [
            ("Что это", p(
                "Игра выходит на Android, и перед публикацией её нужно обкатать на живых людях. "
                "Нужны те, кто поиграет пару недель и расскажет, что ломается, что непонятно и где скучно.")),
            ("Как вступить",
             p("Доступ уже открыт. Вы вступаете сами по ссылкам ниже, ждать письма не нужно.")
             + p("<b>Сначала два условия, без них игры вы не увидите.</b> "
                 "Первое: оба шага делайте тем же Google-аккаунтом, под которым вы залогинены "
                 "в Play Маркете на телефоне. Если аккаунтов несколько, откройте Play Маркет "
                 "и проверьте, под каким вы сидите. Это причина номер один «игры нет, ссылка не работает». "
                 "Второе: если вы уже во внутреннем тесте, выйдите из него, иначе закрытый трек вам "
                 "не покажут. Путь: Play Маркет, профиль, «Приложения и устройства», вкладка «Бета», "
                 "игра, «Выйти».")
             + steps(
                 'Вступите в группу тестировщиков «The Last War Closed Test»: '
                 '<a href="%s" target="_blank" rel="noopener">groups.google.com/g/lastwar-testers</a>. '
                 'Группа открытая, одобрение не нужно, вступление занимает один клик.' % GROUP_URL,
                 'Согласитесь на участие в тесте: '
                 '<a href="%s" target="_blank" rel="noopener">страница теста в Google Play</a>. '
                 'Откройте её тем же аккаунтом и нажмите кнопку согласия.' % OPTIN_URL,
                 'Установите игру из Google Play по ссылке с той же страницы. Доступ появляется '
                 'не мгновенно: если магазин пишет, что приложения нет, подождите и обновите страницу.')),
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
                "а прокачка идёт картами: за сбитых растёт ранг, на каждом ранге бой замирает и предлагает "
                "три карты. Девять орудий, у каждого лестница из пяти ступеней и развилка на три пути. "
                "Забег — одна миссия, минуты на две. Биомов десять, в конце каждого босс. "
                "Дерево узлов покупается кристаллами уже вне боя. Играется офлайн, без таймеров энергии. "
                '<a href="press.html">Пресс-кит со скриншотами и роликом</a>.')),
            ("Оставить контакт",
             p("Доступ вы уже получили по трём шагам выше, эта форма не про доступ. Она нужна, "
               "чтобы я знал, кто пришёл в тест, и мог написать вам по ходу: что поменялось в сборке, "
               "что стоит проверить, куда слать баги. Не хотите заполнять, просто напишите мне на "
               '<a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL))
             + form),
            ("Что будет с вашими данными", p(
                "Из формы приходят позывной, адрес Google-аккаунта и тип устройства. Адрес нужен ровно затем, "
                "чтобы писать вам по самому тесту и помогать, если доступ не открылся. Список тестеров лежит у меня "
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
        ("How to join",
         p("Access is already open. You join yourself through the links below, "
           "there is no invite email to wait for.")
         + p("<b>Two conditions first, or the game will not show up.</b> "
             "One: do both steps with the same Google account you are signed in with in the Play "
             "Store on your phone. If you have several accounts, open the Play Store and check "
             "which one is active. This is the number one reason people say the link does not work. "
             "Two: if you are already in the internal test, leave it, otherwise the closed track "
             "stays hidden. The path: Play Store, profile, Manage apps and devices, Beta tab, "
             "the game, Leave.")
         + steps(
             'Join the tester group "The Last War Closed Test": '
             '<a href="%s" target="_blank" rel="noopener">groups.google.com/g/lastwar-testers</a>. '
             'The group is open, no approval is needed, joining takes one click.' % GROUP_URL,
             'Opt in to the test: '
             '<a href="%s" target="_blank" rel="noopener">the test page on Google Play</a>. '
             'Open it with the same account and press the button that accepts the invitation.' % OPTIN_URL,
             'Install the game from Google Play through the link on that same page. Access does not '
             'appear instantly: if the store says the app is unavailable, wait a little and refresh '
             'the page.')),
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
            "you fire the reactor by hand, and upgrades come as cards: kills raise your rank, and every rank "
            "freezes the fight and offers three. Nine guns, each with a five-tier ladder and a three-way fork. "
            "A run is one mission, about two minutes. Ten biomes, each ending with a boss. The node tree is "
            "bought with crystals outside combat. Plays offline, no energy timers. "
            '<a href="press.html">Press kit with screenshots and video</a>.')),
        ("Stay in touch",
         p("You already have access from the three steps above, this form is not about access. "
           "It is how I know who joined and how I reach you during the test: what changed in the "
           "build, what is worth checking, where to send bugs. If you would rather not fill it in, "
           'just write to me at <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL))
         + form),
        ("What happens to your data", p(
            "The form sends a handle, a Google account address and a device type. The address is used to email "
            "you about the test itself and to help you if access does not open. The tester list lives with me and in Play "
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
    "index.html": "Игра про ИИ, сделанная ИИ: код, арт, звук и баланс созданы искусственным интеллектом. Аркадное ПВО-выживание — бронепоезд, зенитки, карточная прокачка в бою, 9 орудий по 5 ступеней, 10 биомов. Уже можно играть в закрытом тесте Google Play.",
    "lore.html": "Мир «Поезда Последней Войны»: бортжурнал машиниста — война машин, бронесостав и 10 биомов маршрута.",
    "en/lore.html": "The world of The Last War: Train — the driver's logbook: the machine war, the armored train and the route's 10 biomes.",
    "terms.html": "Условия использования игры «%s»." % GAME_RU,
    "privacy.html": "Политика конфиденциальности игры «%s»." % GAME_RU,
    "support.html": "Поддержка игры «%s»: контакты, покупки, удаление данных." % GAME_RU,
    "press.html": "Пресс-кит «%s»: факты, описание, скриншоты, логотип, ролик, контакты. "
                  "Игра про ИИ, сделанная ИИ — код, арт, звук и баланс созданы "
                  "искусственным интеллектом." % GAME_RU,
    "en/press.html": "Press kit for \"%s\": factsheet, description, screenshots, logo, video, "
                     "contact. A game about AI, made by AI — code, art, audio and balance are "
                     "AI-generated." % GAME_EN,
    "test.html": 'Стать тестировщиком «%s»: закрытый тест в Google Play, что нужно от тестера, что он получает и как вступить в три шага.' % GAME_RU,
    "en/test.html": 'Become a tester for "%s": closed test on Google Play, what a tester needs, what they get and how to join in three steps.' % GAME_EN,
    "en/index.html": "A game about AI, made by AI: code, art, audio and balance are AI-generated. Arcade AA-survival — an armored train, anti-air turrets, an in-combat card draft, 9 guns with 5 tiers each, 10 biomes. Playable now in the Google Play closed test.",
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
               # Roguelite добавлен по факту механики: прогрессия в бою — карточный драфт,
               # ран-состояние сгорает на границе миссии (BattleNodeTree.clear_run_levels).
               '"@type":"VideoGame","name":"%s","genre":["Arcade","Survival","Roguelite","Tower Defense"],'
               '"gamePlatform":["Android"],"applicationCategory":"Game",'
               '"description":"%s",'
               '"author":{"@type":"Organization","name":"Dido Games","url":"%s"},'
               '"image":"%s/assets/img/og.jpg","url":"%s",'
               '"video":{"@type":"VideoObject","name":"%s — gameplay presentation",'
               # ⚠️ ролик к пересъёмке (директива №50) — в кадре межволновое окно дерева,
               # которого в игре больше нет; описание очищено, монтаж меняет отдельный наряд.
               '"description":"70-second in-game presentation: combat, harvest field, depot, bosses.",'
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
# 404 в двух локалях: переключатель языка в шапке ведёт на en/404.html, и без этого файла
# единственная ссылка сайта, отдающая 404, была именно на странице 404.
NF = [("ru", "404.html", "/", "404 — %s" % GAME_RU, "ФОРМУЛЯР // 404", "Страница не найдена",
       "Сигнал потерян в пустоши", "&larr; НА ГЛАВНУЮ", "/"),
      ("en", "en/404.html", "/en/", "404 — %s" % GAME_EN, "FORM // 404", "Page not found",
       "Signal lost in the wastes", "&larr; BACK TO MAIN", "/en/")]
for _lang, _rel, _base, _title, _field, _h1, _sub, _back, _home in NF:
    _html = page(_lang, _title,
                 '<main class="doc"><div class="doc-head"><div class="field">%s</div>'
                 '<h1>%s</h1><div class="date">%s</div></div>'
                 '<p class="backlink"><a href="%s">%s</a></p></main>'
                 % (_field, _h1, _sub, _home, _back), _rel, base_href=_base)
    _path = os.path.join(ROOT, _rel)
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    with open(_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(_html)
print("written robots.txt / sitemap.xml / CNAME / 404.html / en/404.html")
