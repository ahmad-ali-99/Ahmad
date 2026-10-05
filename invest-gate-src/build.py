#!/usr/bin/env python3
"""Invest Gate — static site generator (Arabic at root, Kurdish in ku/, English in en/)."""
import os, re, sys, shutil, importlib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'invest-gate')
BASE = 'https://ahmad-ali-99.github.io/investgate/'

PHONE1, PHONE1_T = '+964 770 000 0000', '+9647700000000'
PHONE2, PHONE2_T = '+964 780 000 0000', '+9647800000000'
PHONE3, PHONE3_T = '+964 771 000 0000', '+9647710000000'
EMAIL, EMAIL2 = 'info@investgate.iq', 'sales@investgate.iq'
MAP = 'https://www.google.com/maps/search/?api=1&amp;query=Palestine+Street+Baghdad'

LANGS = [('ar', ''), ('ku', 'ku/'), ('en', 'en/')]
LC = {c: importlib.import_module('i18n.' + c).C for c, _ in LANGS}
FILES = ['index.html', 'about.html', 'services.html', 'solar.html', 'projects.html', 'contact.html']
LOCALE = {'ar': 'ar_IQ', 'ku': 'ckb_IQ', 'en': 'en_US'}
SKIP = {'ar': 'تخطَّ إلى المحتوى', 'ku': 'بازدان بۆ ناوەڕۆک', 'en': 'Skip to content'}
LANG_SHORT = {'ar': 'عربي', 'ku': 'کوردی', 'en': 'EN'}

PROJ_META = [('construction', 'site', '2024'), ('solar', 'solar-rows', '2024'), ('cars', 'cars-2', '2024'),
             ('logistics', 'ship', '2023'), ('construction', 'excavator', '2023'), ('solar', 'solar-sunset', '2023'),
             ('logistics', 'transport-2', '2024'), ('construction', 'steel', '2022'), ('solar', 'solar-plant', '2025')]
SVC_IMG = {'cars': 'cars', 'shipping': 'shipping', 'transport': 'transport', 'construction': 'construction', 'solar': 'solar-install', 'trading': 'warehouse-2'}
TYPE_IMG = ['solar-roof', 'solar-rural', 'hero-solar', 'solar-field', 'solar-plant', 'solar-panel']

SEP = '<span class="sep"></span>'
CURP = ' aria-current="page"'
ONC = ' class="on"'
ARR = '<svg class="arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
STEP = '<svg class="mq__sep" viewBox="0 0 36 36" aria-hidden="true"><path d="M0 36V24H6V12H12V0H24V12H30V24H36V36Z"/></svg>'
MARK = ('<svg class="brand__mark" viewBox="0 0 48 48" aria-hidden="true">'
        '<path class="m b" fill-rule="evenodd" d="M6 16H42V44H6Z M17 44V32A7 7 0 0 1 31 32V44Z"/>'
        '<rect class="m b" x="6" y="11" width="8" height="5"/><rect class="m b" x="20" y="11" width="8" height="5"/><rect class="m b" x="34" y="11" width="8" height="5"/>'
        '<rect class="m b" x="8" y="7" width="4" height="4"/><rect class="m b" x="22" y="7" width="4" height="4"/><rect class="m b" x="36" y="7" width="4" height="4"/></svg>')
WA_PATH = '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4a.5.5 0 0 0 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.6-.3z"/>'

HEAD_JS = ("<script>(function(h){h.classList.add('js');try{var s=sessionStorage;"
           "if(s.getItem('ig-seen')||matchMedia('(prefers-reduced-motion: reduce)').matches)h.classList.add('no-loader');"
           "if(s.getItem('ig-pt')){h.classList.add('pt-in');s.removeItem('ig-pt')}}catch(e){h.classList.add('no-loader')}})(document.documentElement)</script>")

# image sizes for width/height attributes
DIMS = {}
for f in os.listdir(os.path.join(HERE, 'img')):
    if f.endswith('-1600.webp'):
        with Image.open(os.path.join(HERE, 'img', f)) as im:
            DIMS[f[:-10]] = im.size

# fonts to preload
FONT_CSS = open(os.path.join(HERE, 'assets/css/fonts.css')).read()
def font_file(family_tag, weight=None):
    for block in FONT_CSS.split('/* ')[1:]:
        if block.startswith(family_tag) and (weight is None or f'font-weight: {weight};' in block):
            return re.search(r'url\(\.\./fonts/([^)]+)\)', block).group(1)
PRELOAD = {
    'rtl': [font_file('Reem+Kufi arabic'), font_file('IBM+Plex+Sans+Arabic arabic', 400)],
    'ltr': [font_file('Archivo latin '), font_file('IBM+Plex+Sans latin ')],
}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


class Page:
    def __init__(self, code, folder, fname):
        self.code, self.folder, self.fname = code, folder, fname
        self.C = LC[code]
        self.R = '../' if folder else ''
        self.rtl = self.C['dir'] == 'rtl'

    # ---------- helpers
    def img(self, name, alt='', sizes='100vw', eager=False, cls=''):
        w, h = DIMS[name]
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        c = f' class="{cls}"' if cls else ''
        return (f'<img{c} src="{self.R}img/{name}-1600.webp" srcset="{self.R}img/{name}-800.webp 800w, {self.R}img/{name}-1600.webp 1600w" '
                f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async">')

    def url(self, folder, fname):
        return BASE + folder + ('' if fname == 'index.html' else fname)

    def lang_href(self, folder):
        return f'{self.R}{folder}{self.fname}'

    def langs(self):
        out = []
        for c, f in LANGS:
            cur = ' aria-current="true"' if f == self.folder else ''
            out.append(f'<a href="{self.lang_href(f)}" lang="{LC[c]["lang"]}" hreflang="{LC[c]["lang"]}"{cur}>{LANG_SHORT[c]}</a>')
        return '<div class="langs">' + SEP.join(out) + '</div>'

    @staticmethod
    def idx(i):
        return f'{i + 1:02d}'

    def btn(self, href, label, cls='', attrs=''):
        return f'<a class="btn {cls}" href="{href}"{attrs}><span>{label}</span>{ARR}</a>'

    def shead(self, label, title, text='', h='h-l'):
        p = f'<p data-reveal>{text}</p>' if text else ''
        return f'<div class="shead"><div><p class="eyebrow">{label}</p><h2 class="{h}" data-split>{title}</h2></div>{p}</div>'

    def ticks(self, items, two=False):
        cls = 'ticks ticks--2' if two else 'ticks'
        return f'<ul class="{cls}" data-stagger>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

    # ---------- document parts
    def head(self, title, desc):
        C = self.C
        full = C['full'] if self.fname == 'index.html' else f'{title} — {C["name"]}'
        alts = ''.join(f'<link rel="alternate" hreflang="{LC[c]["lang"]}" href="{self.url(f, self.fname)}">' for c, f in LANGS)
        alts += f'<link rel="alternate" hreflang="x-default" href="{self.url("", self.fname)}">'
        pre = ''.join(f'<link rel="preload" href="{self.R}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>'
                      for f in PRELOAD['rtl' if self.rtl else 'ltr'])
        return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{self.url(self.folder, self.fname)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(C['full'])}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{self.url(self.folder, self.fname)}">
<meta property="og:image" content="{BASE}og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{LOCALE[self.code]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a1440">
<link rel="icon" href="{self.R}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{self.R}apple-touch-icon.png">
{HEAD_JS}
{pre}
<link rel="stylesheet" href="{self.R}assets/css/fonts.css">
<link rel="stylesheet" href="{self.R}assets/css/main.css">'''

    def chrome_top(self):
        C = self.C
        nav = ''.join(f'<a href="{h}"{CURP if h == self.fname else ""}>{t}</a>' for h, t in zip(FILES, C['nav']))
        ovl_links = ''.join(f'<li><a href="{h}"><i>{self.idx(i)}</i>{t}</a></li>' for i, (h, t) in enumerate(zip(FILES, C['nav'])))
        small = 'GENERAL TRADING &amp; CONTRACTING' if self.code == 'en' else 'INVEST GATE'
        brand = f'<a class="brand" href="index.html" aria-label="{esc(C["name"])}">{MARK}<span class="brand__txt"><b>{C["name"]}</b><small>{small}</small></span></a>'
        return f'''<a class="skip" href="#main">{SKIP[self.code]}</a>
<div class="ldr" aria-hidden="true"><div class="ldr__mid">{MARK.replace('brand__mark', 'ldr__mark')}<div class="ldr__name">{C["name"]}<small>INVEST GATE</small></div></div><div class="ldr__count">0</div></div>
<div class="pt" aria-hidden="true"></div>
<header class="hdr" id="top">
  <div class="wrap hdr__in">
    {brand}
    <nav class="nav" aria-label="{esc(C['menu'])}">{nav}</nav>
    {self.langs()}
    <a class="btn hdr__cta" href="contact.html"><span>{C['quote_btn']}</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="ovl"><span>{C['menu']}</span><i></i></button>
  </div>
</header>
<div class="ovl bricks" id="ovl" role="dialog" aria-modal="true" aria-label="{esc(C['menu'])}">
  <div class="wrap ovl__top">{brand}<button class="ovl__close" type="button"><span>{C['close']}</span><i></i></button></div>
  <div class="wrap ovl__body">
    <ol class="ovl__links">{ovl_links}</ol>
    <div class="ovl__aside">
      <div><h4>{C['call_us']}</h4><a class="ltr" href="tel:{PHONE1_T}">{PHONE1}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div><h4>{C['offices']}</h4><p>{C['address']}<br>{C['branch']}</p></div>
      <div><h4>{C['lang_aria']}</h4>{self.langs()}</div>
    </div>
  </div>
</div>'''

    def footer(self, cta=True, cta_title=None, cta_text=None):
        C = self.C
        pages = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in zip(FILES, C['nav']))
        svcs = ''.join(f'<li><a href="{"solar.html" if k == "solar" else "services.html#" + k}">{t}</a></li>' for k, _, t, _, _ in C['services'])
        word = ''.join(f'<span>{ch if ch != " " else "&nbsp;"}</span>' for ch in 'INVEST GATE')
        cta_html = ''
        if cta:
            cta_html = f'''<div class="ftr__cta">
      <div><p class="eyebrow">{C['quote_title']}</p><h2 data-split>{cta_title or C['cta_title']}</h2><p>{cta_text or C['cta_text']}</p></div>
      <div class="magnet-wrap"><a class="magnet" href="contact.html" data-magnetic><span>{ARR}{C['quote_btn']}</span></a></div>
    </div>'''
        year = '<span id="year">2026</span>'
        return f'''<div class="edge" aria-hidden="true"></div>
<div class="foot-wrap"><footer class="ftr bricks">
  <div class="wrap">
    {cta_html}
    <div class="ftr__grid">
      <div class="ftr__col ftr__col--wide"><h4>{C['call_us']}</h4><a class="big-tel ltr" href="tel:{PHONE1_T}">{PHONE1}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="ftr__col"><h4>{C['offices']}</h4><p>{C['address']}</p><p>{C['branch']}</p><p>{C['hours_short']}</p></div>
      <div class="ftr__col ftr__col--sm"><h4>{C['f_quick']}</h4><ul>{pages}</ul></div>
      <div class="ftr__col ftr__col--svc"><h4>{C['f_services']}</h4><ul>{svcs}</ul></div>
    </div>
  </div>
  <div class="ftr__word" aria-hidden="true">{word}</div>
  <div class="wrap ftr__bottom"><span>{C['copyright'].replace('{y}', year)}</span><a href="#top">{C['back_top']} ↑</a></div>
</footer></div>
<a class="wa" data-wa href="#" target="_blank" rel="noopener" aria-label="{esc(C['wa_aria'])}"><svg viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg></a>
<script src="{self.R}assets/vendor/gsap.min.js" defer></script>
<script src="{self.R}assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="{self.R}assets/vendor/lenis.min.js" defer></script>
<script src="{self.R}assets/js/main.js" defer></script>'''

    def phero(self, title, intro, img):
        C = self.C
        return f'''<section class="phero bricks">
  <div class="wrap phero__in">
    <div class="phero__copy">
      <ol class="crumbs"><li><a href="index.html">{C['home']}</a></li><li aria-current="page">{title}</li></ol>
      <h1 class="phero__title">{title}</h1>
      <p class="phero__text">{intro}</p>
    </div>
    <div class="phero__media" data-par>{self.img(img, '', '(max-width: 860px) 100vw, 34vw', eager=True)}</div>
  </div>
</section>'''

    def work(self, i, cls, sizes):
        C = self.C
        cat, img, year = PROJ_META[i]
        title, city = C['projects'][i]
        return f'''<a class="{cls}" href="projects.html" data-cat="{cat}">
  <div class="work__img" data-img data-par><span class="pill">{C['proj_cats'][cat]}</span>{self.img(img, title, sizes)}</div>
  <div class="work__cap"><h3>{title}</h3><span>{city} · {year}</span></div>
</a>'''

    # ---------- pages
    def p_index(self):
        C = self.C
        lines = ''.join(f'<span class="ln">{l}</span>' for l in C['hero_lines'])
        cap = ''.join(f'<li><span>{self.idx(i)}</span>{t}</li>' for i, (_, _, t, _, _) in enumerate(C['services']))
        rows = ''
        hover = ''
        for i, (k, _, t, img, d) in enumerate(C['services']):
            href = 'solar.html' if k == 'solar' else f'services.html#{k}'
            im = SVC_IMG[k]
            rows += f'''<li class="row"><span class="row__i">{self.idx(i)}</span><h3 class="row__t">{t}</h3><p class="row__d">{d}</p><span class="row__go">{ARR}</span><div class="row__thumb">{self.img(im, '', '90vw')}</div><a class="cover" href="{href}" aria-label="{esc(t)}"></a></li>'''
            hover += f'<img src="{self.R}img/{im}-800.webp" alt="" loading="lazy" decoding="async">'
        nums = [(12, '+'), (340, '+'), (45, ''), (18, '')]
        en = self.code == 'en'
        nums_html = ''
        for (n, plus), label in zip(nums, C['stats']):
            attr = ' data-suffix="+"' if plus else ''
            shown = f'{n}+' if plus else str(n)
            nums_html += f'<div class="num"><b data-count="{n}"{attr}>{shown}</b><span>{label}</span></div>'
        cards = ''
        for i, ((t, sub, d, fit), im) in enumerate(zip(C['types'], TYPE_IMG)):
            cards += f'''<article class="hs__card"><div class="k"><span>{self.idx(i)}</span><span>{sub}</span></div><div class="hs__img">{self.img(im, t, '(max-width: 860px) 78vw, 30vw')}</div><h3>{t}</h3><p>{d}</p></article>'''
        mq_items = ''.join(f'<span class="mq__item">{t}{STEP}</span>' for _, _, t, _, _ in C['services'])
        body = f'''<section class="gate bricks" aria-label="{esc(C['full'])}">
  <div class="gate__media" aria-hidden="true">{self.img('hero-port', '', '100vw', eager=True)}</div>
  <div class="wrap gate__in">
    <div class="gate__copy">
      <p class="gate__meta">{C['founded_line']}</p>
      <h1 class="gate__title">{lines}</h1>
      <p class="gate__sub">{C['hero_sub']}</p>
      <div class="gate__actions">{self.btn('services.html', C['slides'][0][3][0], 'btn--light')}{self.btn('contact.html', C['quote_btn'], 'btn--solid')}</div>
    </div>
    <div class="gate__frame"><div class="gate__media">{self.img('hero-port', C['band_alt'] if False else '', '(max-width: 860px) 90vw, 34vw', eager=True)}</div></div>
  </div>
  <div class="gate__caption" aria-hidden="true"><div class="wrap"><ul>{cap}</ul></div></div>
  <div class="scroll-cue" aria-hidden="true"><i></i>{C['scroll']}</div>
</section>

<section class="sec bg-paper">
  <div class="wrap intro__grid">
    <div class="intro__meta" data-reveal><b>2012</b><span>{C['founded_line']}</span></div>
    <p class="intro__text" data-scrub>{C['intro_statement']}</p>
    <div class="intro__link" data-reveal><a class="link-u" href="about.html">{C['intro_link']}{ARR}</a></div>
  </div>
</section>

<section class="sec bg-white">
  <div class="wrap">
    {self.shead(C['svc_label'], C['svc_title'], C['svc_text'])}
    <ul class="rows">{rows}</ul>
    <div class="rows-foot"><span>{C['sectors_hint']}</span>{self.btn('services.html', C['all_services'])}</div>
  </div>
  <div class="hover-media" aria-hidden="true">{hover}</div>
</section>

<section class="sec bg-lapis bricks crenel">
  <div class="wrap nums__grid">
    <div class="nums__head"><p class="eyebrow">{C['why_label']}</p><h2 class="h-l" data-split>{C['numbers_title']}</h2><p class="lead" data-reveal style="margin-top:28px;color:rgba(255,255,255,.8)">{C['why_text']}</p></div>
    <div class="nums__list" data-stagger>{nums_html}</div>
  </div>
</section>

<section class="hs bricks" aria-label="{esc(C['band_label'])}">
  <div class="hs__pin">
    <div class="hs__row">
      <div class="hs__intro">
        <div><p class="eyebrow">{C['band_label']}</p><h2 class="h-m">{C['band_title']}</h2><p style="margin-top:22px">{C['band_text']}</p></div>
        <div>{self.btn('solar.html', C['band_btn'], 'btn--light')}<div class="hs__hint"><span>{C['solar_scroll_hint']}</span><span class="hs__bar"><i></i></span></div></div>
      </div>
      <div class="hs__track">{cards}</div>
      <div class="hs__end"><p>{C['solar_cta'][0]}</p>{self.btn('contact.html', C['quote_btn'], 'btn--light')}</div>
    </div>
  </div>
</section>

<section class="sec bg-paper">
  <div class="wrap">
    {self.shead(C['proj_label'], C['proj_title'], C['proj_text'])}
    <div class="works__grid">
      {self.work(0, 'work work--a', '(max-width: 860px) 100vw, 58vw')}
      {self.work(1, 'work work--b', '(max-width: 860px) 100vw, 34vw')}
      {self.work(6, 'work work--c', '(max-width: 860px) 100vw, 66vw')}
    </div>
    <div class="rows-foot"><span></span>{self.btn('projects.html', C['proj_all_btn'])}</div>
  </div>
</section>

<section class="mq bg-paper" aria-hidden="true"><div class="mq__track">{mq_items}{mq_items}</div></section>'''
        return C['index_title'], C['index_desc'], body, {}

    def p_about(self):
        C = self.C
        vals = ''.join(f'<li class="value"><i>{self.idx(i)}</i><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (_, t, d) in enumerate(C['values']))
        goals = ''.join(f'<li>{g}</li>' for g in C['goals'][1])
        ab_p = ''.join(f'<p data-reveal>{p}</p>' for p in C['ab_p'])
        body = f'''{self.phero(*C['about_page'], 'towers')}

<section class="sec bg-paper">
  <div class="wrap split">
    <div class="split__media"><div class="frame frame--arch" data-img>{self.img('site', C['site_alt'], '(max-width: 860px) 80vw, 40vw')}</div></div>
    <div class="split__body">
      <p class="eyebrow">{C['ab_label']}</p>
      <h2 class="h-m" data-split>{C['ab_title']}</h2>
      <div class="big-year" data-reveal>2012</div>
      {ab_p}
      {self.ticks(C['ab_checks'], True)}
    </div>
  </div>
</section>

<section class="sec bg-lapis bricks crenel">
  <div class="wrap">
    {self.shead(C['vmv_label'], C['vmv_title'], '', 'h-l')}
    <div class="vmv" data-stagger>
      <div><h3>{C['vision'][0]}</h3><p>{C['vision'][1]}</p></div>
      <div><h3>{C['mission'][0]}</h3><p>{C['mission'][1]}</p></div>
      <div><h3>{C['goals'][0]}</h3><ul>{goals}</ul></div>
    </div>
  </div>
</section>

<section class="sec bg-white">
  <div class="wrap">
    {self.shead(C['val_label'], C['val_title'], C['val_text'])}
    <ul class="values" data-stagger>{vals}</ul>
  </div>
</section>

<section class="sec bg-night bricks crenel">
  <div class="wrap quote">
    <div class="quote__img"><div class="frame frame--arch" data-img>{self.img('handshake', C['msg_alt'], '(max-width: 860px) 60vw, 30vw')}</div></div>
    <div class="quote__body">
      <p class="eyebrow">{C['msg_label']}</p>
      <span class="quote__mark" aria-hidden="true">&#8221;</span>
      <blockquote class="quote__text" data-reveal>{C['msg_text']}</blockquote>
      <p class="quote__cite"><span><b>{C['msg_cite']}</b>{C['company_formal']}</span></p>
    </div>
  </div>
</section>

<section class="sec bg-paper">
  <div class="wrap split split--rev">
    <div class="split__media"><div class="frame frame--tall" data-img>{self.img('construction', C['q_alt'], '(max-width: 860px) 100vw, 40vw')}</div></div>
    <div class="split__body">
      <p class="eyebrow">{C['q_label']}</p>
      <h2 class="h-m" data-split>{C['q_title']}</h2>
      <p data-reveal style="margin-top:28px">{C['q_text']}</p>
      {self.ticks(C['q_checks'])}
    </div>
  </div>
</section>'''
        return C['about_page'][0], C['about_desc'], body, {}

    def p_services(self):
        C = self.C
        side = ''.join(f'<a href="#{k}"><i>{self.idx(i)}</i>{t}</a>' for i, (k, _, t, _, _) in enumerate(C['services']))
        chips = ''.join(f'<a href="#{k}">{t}</a>' for k, _, t, _, _ in C['services'])
        blocks = ''
        for i, (k, _, t, img, _) in enumerate(C['services']):
            text, items = C['svc_detail'][k]
            foot = self.btn('solar.html', C['solar_details_btn']) if k == 'solar' else self.btn('contact.html', C['quote_btn'], 'btn--solid')
            blocks += f'''<article class="svc" id="{k}">
  <div class="svc__head"><i>{self.idx(i)}</i><h2 data-split>{t}</h2></div>
  <div class="frame svc__img" data-img data-par>{self.img(SVC_IMG[k] if k != 'cars' else 'cars-2', t, '(max-width: 860px) 100vw, 64vw')}</div>
  <div class="svc__body"><p data-reveal>{text}</p>{self.ticks(items)}</div>
  <div class="svc__foot" data-reveal>{foot}</div>
</article>'''
        body = f'''{self.phero(*C['services_page'], 'containers')}

<section class="sec bg-paper">
  <div class="wrap svc-layout">
    <nav class="side" aria-label="{esc(C['svc_nav_aria'])}"><p>{C['side_nav']}</p>{side}</nav>
    <div class="svc-list">
      <nav class="chips" aria-label="{esc(C['svc_nav_aria'])}">{chips}</nav>
      {blocks}
    </div>
  </div>
</section>'''
        return C['services_page'][0], C['services_desc'], body, {}

    def p_solar(self):
        C = self.C
        si_p = ''.join(f'<p data-reveal>{p}</p>' for p in C['si_p'])
        types = ''
        for (t, en, d, fit), im in zip(C['types'], TYPE_IMG):
            sub = f'<span class="en">{en}</span>' if en else ''
            types += f'''<article class="type"><div class="frame type__img" data-img>{self.img(im, t, '(max-width: 560px) 100vw, (max-width: 1024px) 50vw, 32vw')}</div><h3>{t}</h3>{sub}<p>{d}</p><p class="fit"><b>{C['fit']}</b> {fit}</p></article>'''
        specs = ''.join(f'<div class="spec"><i>{self.idx(i)}</i><h3>{t}</h3><p>{d}</p></div>' for i, (_, t, d) in enumerate(C['comps']))
        uses = ''.join(f'<option value="{v}">{t}</option>' for v, t in zip(['home', 'shop', 'farm', 'factory'], C['calc_uses']))
        res = C['calc_res']
        steps = ''.join(f'<li class="tl__item" data-reveal><b>{self.idx(i)}</b><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(C['steps']))
        warr = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in C['warranty'])
        body = f'''{self.phero(*C['solar_page'], 'solar-plant')}

<section class="sec bg-paper">
  <div class="wrap split">
    <div class="split__media"><div class="frame frame--arch" data-img>{self.img('solar-install', C['si_alt'], '(max-width: 860px) 80vw, 40vw')}</div></div>
    <div class="split__body">
      <p class="eyebrow">{C['si_label']}</p>
      <h2 class="h-m" data-split>{C['si_title']}</h2>
      <div style="margin-top:28px">{si_p}</div>
      {self.ticks(C['si_checks'], True)}
    </div>
  </div>
</section>

<section class="sec bg-white">
  <div class="wrap">
    {self.shead(C['types_label'], C['types_title'], C['types_text'])}
    <div class="types">{types}</div>
  </div>
</section>

<section class="sec bg-night bricks crenel">
  <div class="wrap">
    {self.shead(C['comp_label'], C['comp_title'], C['comp_text'], 'h-m')}
    <div class="specs" data-stagger>{specs}</div>
  </div>
</section>

<section class="sec bg-paper" id="calc-section">
  <div class="wrap">
    {self.shead(C['calc_label'], C['calc_title'], C['calc_text'], 'h-m')}
    <div class="calc" id="calc" data-reveal>
      <div class="calc__in">
        <h3>{C['calc_in']}</h3>
        <p>{C['calc_hint']}</p>
        <label class="ctl" for="c-use"><span>{C['calc_use']}</span><select id="c-use">{uses}</select></label>
        <label class="ctl" for="c-amp"><span>{C['calc_amp']}<output id="o-amp" for="c-amp">15</output></span><input type="range" id="c-amp" min="2" max="100" value="15"></label>
        <label class="ctl" for="c-day"><span>{C['calc_day']}<output id="o-day" for="c-day">8</output></span><input type="range" id="c-day" min="2" max="12" value="8"></label>
        <label class="ctl" for="c-night"><span>{C['calc_night']}<output id="o-night" for="c-night">6</output></span><input type="range" id="c-night" min="0" max="12" value="6"></label>
      </div>
      <div class="calc__out bricks">
        <h3>{C['calc_out']}</h3>
        <div class="res">
          <div><b id="r-kwp">7.6</b><span>{res[0]}</span></div>
          <div><b id="r-pan">13</b><span>{res[1]}</span></div>
          <div><b id="r-inv">5</b><span>{res[2]}</span></div>
          <div><b id="r-bat">16</b><span>{res[3]}</span></div>
        </div>
        <p class="rec">{C['calc_rec']} <strong id="r-type">Hybrid</strong></p>
        <p class="note">{C['calc_note']}</p>
        <a class="btn btn--light" id="calc-book" href="contact.html" target="_blank" rel="noopener"><span>{C['calc_book']}</span>{ARR}</a>
      </div>
    </div>
  </div>
</section>

<section class="sec bg-white">
  <div class="wrap">
    {self.shead(C['steps_label'], C['steps_title'], '', 'h-m')}
    <ol class="tl"><span class="tl__line" aria-hidden="true"><i></i></span>{steps}</ol>
  </div>
</section>

<section class="sec bg-paper">
  <div class="wrap">
    {self.shead(C['war_label'], C['war_title'], C['war_text'], 'h-m')}
    <div class="warr" data-stagger>{warr}</div>
  </div>
</section>'''
        return C['solar_page'][0], C['solar_desc'], body, {'cta_title': C['solar_cta'][0], 'cta_text': C['solar_cta'][1]}

    def p_projects(self):
        C = self.C
        counts = {k: sum(1 for m in PROJ_META if m[0] == k) for k, _ in C['filters']}
        counts['all'] = len(PROJ_META)
        filt = ''.join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}"{ONC if k == "all" else ""}>{t}<sup>{counts[k]}</sup></button>' for k, t in C['filters'])
        items = ''.join(self.work(i, 'gitem', '(max-width: 860px) 100vw, 58vw') for i in range(len(PROJ_META)))
        figs = ''
        en = self.code == 'en'
        for n, label in zip([340, 120, 1500, 600], C['pstats']):
            attr = ' data-suffix="+"'
            figs += f'<div class="num"><b data-count="{n}"{attr}>{n}</b><span>{label}</span></div>'
        body = f'''{self.phero(*C['projects_page'], 'hero-construction')}

<section class="sec bg-paper">
  <div class="wrap">
    <div class="filters" role="group" aria-label="{esc(C['filters_aria'])}">{filt}</div>
    <div class="gallery">{items}</div>
  </div>
</section>

<section class="sec bg-lapis bricks crenel">
  <div class="wrap"><div class="figs" data-stagger>{figs}</div></div>
</section>'''
        return C['projects_page'][0], C['projects_desc'], body, {}

    def p_contact(self):
        C = self.C
        svc_opts = ''.join(f'<option>{t}</option>' for _, _, t, _, _ in C['services'])
        city_opts = ''.join(f'<option>{c}</option>' for c in C['cities'])
        hours = ''.join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in C['hours'])
        body = f'''{self.phero(*C['contact_page'], 'hero-port')}

<section class="sec bg-paper">
  <div class="wrap contact">
    <div class="c-info">
      <p class="eyebrow">{C['call_us']}</p>
      <a class="c-big" href="tel:{PHONE1_T}">{PHONE1}</a>
      <a class="c-big" href="tel:{PHONE2_T}" style="font-size:clamp(20px,2vw,28px);color:var(--ink-2)">{PHONE2}</a>
      <a class="c-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="c-mail" href="mailto:{EMAIL2}" style="margin-top:0">{EMAIL2}</a>
      <div class="c-block" style="margin-top:44px">
        <div class="c-offices">
          <div><h3>{C['cc'][0]}</h3><p>{C['address']}</p></div>
          <div><h3>{C['cc'][1]}</h3><p>{C['branch']}<br><span class="ltr">{PHONE3}</span></p></div>
        </div>
      </div>
      <div class="c-block"><h3>{C['hours_title']}</h3><ul class="hours">{hours}</ul><p class="muted" style="margin-top:14px;font-size:14.5px">{C['hours_text']}</p></div>
      <div class="c-block"><a class="link-u" href="{MAP}" target="_blank" rel="noopener">{C['map_btn']}{ARR}</a></div>
    </div>
    <div class="c-form">
      <form class="form" id="qform" novalidate data-reveal>
        <h2>{C['form_title']}</h2>
        <p>{C['form_text']}</p>
        <div class="fields">
          <label class="field" for="f-name"><span>{C['f_name']}</span><input id="f-name" name="name" autocomplete="name" placeholder="{esc(C['f_name_ph'])}"><em class="err">{C['f_name_err']}</em></label>
          <label class="field" for="f-phone"><span>{C['f_phone']}</span><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="07XX XXX XXXX"><em class="err">{C['f_phone_err']}</em></label>
          <label class="field" for="f-service"><span>{C['f_service']}</span><select id="f-service" name="service">{svc_opts}</select></label>
          <label class="field" for="f-city"><span>{C['f_city']}</span><select id="f-city" name="city">{city_opts}</select></label>
          <label class="field field--full" for="f-msg"><span>{C['f_msg']}</span><textarea id="f-msg" name="msg" rows="4" placeholder="{esc(C['f_msg_ph'])}"></textarea></label>
        </div>
        <button class="btn btn--solid" type="submit"><span>{C['f_submit']}</span>{ARR}</button>
        <div class="form__result" role="status">{C['f_result']} <a href="#" target="_blank" rel="noopener">{C['f_result_link']}</a>.</div>
      </form>
    </div>
  </div>
</section>'''
        return C['contact_page'][0], C['contact_desc'], body, {'cta': False}

    def render(self):
        fn = {'index.html': self.p_index, 'about.html': self.p_about, 'services.html': self.p_services,
              'solar.html': self.p_solar, 'projects.html': self.p_projects, 'contact.html': self.p_contact}[self.fname]
        title, desc, body, fopts = fn()
        C = self.C
        return f'''<!doctype html>
<html lang="{C['lang']}" dir="{C['dir']}">
<head>
{self.head(title, desc)}
</head>
<body>
{self.chrome_top()}
<main id="main">
{body}
</main>
{self.footer(**fopts)}
</body>
</html>
'''


def page_404():
    p = Page('ar', '', 'index.html')
    C = p.C
    E = LC['en']
    head = p.head(C['nf_title'], C['nf_text']).replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/investgate/">')
    head = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex">', head)
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
{head}
</head>
<body class="no-loader">
<main class="nf bricks"><div class="wrap">
  <b>404</b>
  <h1 class="h-m">{C['nf_title']}</h1>
  <p class="lead" style="margin-top:16px">{C['nf_text']}<br><span lang="en" dir="ltr">{E['nf_text']}</span></p>
  <p style="margin-top:32px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn--light" href="index.html"><span>{C['nf_btn']}</span>{ARR}</a><a class="btn btn--light" href="en/" lang="en"><span>{E['nf_btn']}</span></a></p>
</div></main>
</body>
</html>
'''


def build():
    if os.path.exists(OUT):
        for n in os.listdir(OUT):
            if n == '.git':
                continue
            path = os.path.join(OUT, n)
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    shutil.copytree(os.path.join(HERE, 'img'), os.path.join(OUT, 'img'))
    for f in ('favicon.svg', 'apple-touch-icon.png', 'og.jpg'):
        if os.path.exists(os.path.join(HERE, 'static', f)):
            shutil.copy(os.path.join(HERE, 'static', f), OUT)
    urls = []
    for code, folder in LANGS:
        os.makedirs(os.path.join(OUT, folder), exist_ok=True)
        for fname in FILES:
            html = Page(code, folder, fname).render()
            with open(os.path.join(OUT, folder, fname), 'w') as fh:
                fh.write(html)
            urls.append(BASE + folder + ('' if fname == 'index.html' else fname))
    with open(os.path.join(OUT, '404.html'), 'w') as fh:
        fh.write(page_404())
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'  <url><loc>{u}</loc></url>' for u in urls]
    sm.append('</urlset>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    print('built', len(urls), 'pages into', OUT)


if __name__ == '__main__':
    build()
