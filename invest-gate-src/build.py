#!/usr/bin/env python3
"""يولّد صفحات موقع إنفست جيت بثلاث لغات: العربية (الجذر)، الكردية (ku/)، الإنكليزية (en/)."""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SPRITE, ico, LOGO, SOCIAL, WA_PATH, PHONE1, PHONE2, PHONE3, EMAIL, EMAIL2

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'invest-gate')
ART = sys.argv[2] if len(sys.argv) > 2 else None

LANGS = [('ar', ''), ('ku', 'ku/'), ('en', 'en/')]
LC = {code: importlib.import_module('i18n.' + code).C for code, _ in LANGS}
FILES = ['index.html', 'about.html', 'services.html', 'solar.html', 'projects.html', 'contact.html']
PROJ_META = [('construction', 'site.jpg', '2024'), ('solar', 'solar-rows.jpg', '2024'), ('cars', 'cars-2.jpg', '2024'),
             ('logistics', 'ship.jpg', '2023'), ('construction', 'excavator.jpg', '2023'), ('solar', 'solar-sunset.jpg', '2023'),
             ('logistics', 'transport-2.jpg', '2024'), ('construction', 'steel.jpg', '2022'), ('solar', 'solar-plant.jpg', '2025')]
SVC_SUB = {'cars': 'cars-2.jpg', 'shipping': 'ship.jpg', 'transport': 'transport-2.jpg', 'construction': 'excavator.jpg', 'solar': 'solar-install.jpg', 'trading': 'warehouse-2.jpg'}
TYPE_IMG = ['solar-roof.jpg', 'solar-rural.jpg', 'hero-solar.jpg', 'solar-field.jpg', 'solar-plant.jpg', 'solar-panel.jpg']
CUR = ' class="current" aria-current="page"'
ACT = ' class="active"'
PFX = ' data-prefix="+"'
GLOBE = '<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></symbol>'
SPRITE2 = SPRITE.replace('</svg>', GLOBE + '</svg>')


class Page:
    def __init__(self, C, folder, fname):
        self.C, self.folder, self.fname = C, folder, fname
        self.R = '../' if folder else ''

    def img(self, name):
        return f'{self.R}img/{name}'

    def lang_href(self, target_folder):
        return f'{self.R}{target_folder}{self.fname}'

    def head(self, title, desc):
        C = self.C
        full = C['full'] if self.fname == 'index.html' else f"{title} | {C['name']}"
        alts = ''.join(f'<link rel="alternate" hreflang="{LC[l]["lang"]}" href="{self.lang_href(f)}">' for l, f in LANGS)
        return f'''<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0d2438">
{alts}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='4' fill='%230d2438'/%3E%3Cpath d='M12 38V22a12 12 0 0 1 24 0v16' fill='none' stroke='%23c9a46b' stroke-width='3'/%3E%3Cpath d='M24 38V14' stroke='%23c9a46b' stroke-width='3'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{C['fonts']}&display=swap">
<link rel="stylesheet" href="{self.R}assets/site.css">'''

    def lang_switch(self):
        items = ''
        for l, f in LANGS:
            short = 'EN' if l == 'en' else LC[l]['label']
            on = ' class="on" aria-current="true"' if f == self.folder else ''
            items += f'<a href="{self.lang_href(f)}" lang="{LC[l]["lang"]}" hreflang="{LC[l]["lang"]}"{on}>{short}</a>'
        return f'<nav class="lang" aria-label="{self.C["lang_aria"]}">{ico("globe")}{items}</nav>'

    def header(self):
        C = self.C
        links = '\n'.join(f'<li><a href="{h}"{CUR if h == self.fname else ""}>{t}</a></li>' for h, t in zip(FILES, C['nav']))
        social = ''.join(f'<a href="#" aria-label="{n}"><svg viewBox="0 0 24 24">{p}</svg></a>' for n, p in SOCIAL)
        return f'''{SPRITE2}
<div class="topbar">
  <div class="container">
    <span>{ico('phone')}<span dir="ltr">{PHONE1}</span></span>
    <span class="hide-sm">{ico('mail')}{EMAIL}</span>
    <span class="hide-sm">{ico('clock')}{C['hours_short']}</span>
    <div class="tb-end">{social}</div>
    {self.lang_switch()}
  </div>
</div>
<header class="header">
  <div class="container">
    <a class="logo" href="index.html">{LOGO}<span class="logo-txt"><b>{C['name']}</b><small>{C['tagline']}</small></span></a>
    <ul class="nav" id="main-nav">
{links}
    </ul>
    <a class="btn btn-gold" href="contact.html">{C['quote_btn']}</a>
    <button class="menu-btn" aria-label="{C['menu_aria']}" aria-controls="main-nav" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>'''

    def footer(self):
        C = self.C
        svc_links = '\n'.join(f'<li><a href="{"solar.html" if k == "solar" else "services.html#" + k}">{t}</a></li>' for k, _, t, _, _ in C['services'])
        page_links = '\n'.join(f'<li><a href="{h}">{t}</a></li>' for h, t in zip(FILES, C['nav']))
        year = '<span id="year">2026</span>'
        return f'''<footer class="footer">
  <div class="container footer-main">
    <div class="footer-about">
      <a class="logo" href="index.html">{LOGO}<span class="logo-txt"><b>{C['name']}</b><small>{C['tagline']}</small></span></a>
      <p>{C['footer_about']}</p>
    </div>
    <div><h4>{C['f_quick']}</h4><ul>
{page_links}
    </ul></div>
    <div><h4>{C['f_services']}</h4><ul>
{svc_links}
    </ul></div>
    <div>
      <h4>{C['f_contact']}</h4>
      <ul class="contact-list">
        <li>{ico('pin')}<span>{C['address']}</span></li>
        <li>{ico('phone')}<span class="ltr">{PHONE1}</span></li>
        <li>{ico('mail')}<span>{EMAIL}</span></li>
        <li>{ico('clock')}<span>{C['hours_short']}</span></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <span>{C['copyright'].replace('{y}', year)}</span>
      <span>{C['country']}</span>
    </div>
  </div>
</footer>
<a class="wa" data-wa href="#" target="_blank" rel="noopener" aria-label="{C['wa_aria']}"><svg viewBox="0 0 24 24">{WA_PATH}</svg></a>
<script src="{self.R}assets/site.js"></script>'''

    def page_head(self, title, intro, img):
        return f'''<section class="page-head" style="background-image:url('{self.img(img)}')">
  <div class="container">
    <h1>{title}</h1>
    <p>{intro}</p>
    <ol class="crumbs"><li><a href="index.html">{self.C['home']}</a></li><li>{title}</li></ol>
  </div>
</section>'''

    def cta(self, title=None, text=None):
        C = self.C
        return f'''<section class="cta">
  <div class="container">
    <div><h3>{title or C['cta_title']}</h3><p>{text or C['cta_text']}</p></div>
    <div class="btns"><a class="btn btn-primary" href="contact.html">{C['quote_btn']}</a><a class="btn btn-outline" href="contact.html">{C['contact_btn']}</a></div>
  </div>
</section>'''

    @staticmethod
    def s_head(label, title, text='', center=False):
        p = f'<p>{text}</p>' if text else ''
        cls = 's-head center' if center else 's-head'
        return f'<div class="{cls}"><div><span class="s-label">{label}</span><h2>{title}</h2></div>{p}</div>'

    @staticmethod
    def checks(items, one=False):
        cls = 'checks one' if one else 'checks'
        return f'<ul class="{cls}">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

    def proj_card(self, i):
        C = self.C
        cat, img, year = PROJ_META[i]
        title, city = C['projects'][i]
        return f'''<article class="proj" data-cat="{cat}">
  <div class="proj-img"><img loading="lazy" src="{self.img(img)}" alt="{title}"><span class="proj-cat">{C['proj_cats'][cat]}</span></div>
  <div class="proj-body"><h3>{title}</h3><p class="proj-meta"><span>{ico('pin')}{city}</span><span>{ico('calendar')}{year}</span></p></div>
</article>'''

    def stats(self, nums, labels):
        out = ''
        en = self.C['lang'] == 'en'
        for (n, plus), l in zip(nums, labels):
            attr = (' data-suffix="+"' if en else PFX) if plus else ''
            shown = (f'{n}+' if en else f'+{n}') if plus else f'{n}'
            out += f'<div class="stat"><b data-count="{n}"{attr}>{shown}</b><span>{l}</span></div>'
        return f'<section class="stats-section"><div class="container stats">{out}</div></section>'

    # ---------- الصفحات
    def index(self):
        C = self.C
        hrefs = [[('services.html', 'btn-gold'), ('contact.html', 'btn-outline')],
                 [('services.html#construction', 'btn-gold'), ('projects.html', 'btn-outline')],
                 [('solar.html', 'btn-gold'), ('contact.html', 'btn-outline')]]
        imgs = ['hero-port.jpg', 'hero-construction.jpg', 'hero-solar.jpg']
        s_html = ''
        for i, ((label, title, text, btns), hr, img) in enumerate(zip(C['slides'], hrefs, imgs)):
            tag = 'h1' if i == 0 else 'h2'
            b = ''.join(f'<a class="btn {c}" href="{h}">{t}</a>' for (h, c), t in zip(hr, btns))
            active = ' active' if i == 0 else ''
            hidden = '' if i == 0 else ' aria-hidden="true"'
            load = ' fetchpriority="high"' if i == 0 else ' loading="lazy"'
            s_html += f'''<div class="slide{active}"{hidden}>
    <img src="{self.img(img)}" alt=""{load}>
    <div class="container"><span class="slide-label">{label}</span><{tag}>{title}</{tag}><p>{text}</p><div class="btns">{b}</div></div>
  </div>
  '''
        dots = ''.join(f'<button{ACT if i == 0 else ""} aria-label="{C["slide"]} {i+1}"></button>' for i in range(3))
        fbar = ''.join(f'<div class="fb-item">{ico(ic)}<div><h4>{t}</h4><p>{d}</p></div></div>' for ic, t, d in C['fbar'])
        svc_cards = ''.join(f'''<article class="svc">
  <div class="svc-img"><img loading="lazy" src="{self.img(img)}" alt="{t}"><span class="svc-icon">{ico(ic)}</span></div>
  <div class="svc-body"><h3>{t}</h3><p>{d}</p><a class="more" href="{'solar.html' if k == 'solar' else 'services.html#' + k}">{C['details']}</a></div>
</article>''' for k, ic, t, img, d in C['services'])
        why = ''.join(f'<div class="why">{ico(i)}<h4>{t}</h4><p>{d}</p></div>' for i, t, d in C['why'])
        band = ''.join(f'<li>{x}</li>' for x in C['band_types'])
        projs = ''.join(self.proj_card(i) for i in (0, 1, 6))
        about_p = ''.join(f'<p>{p}</p>' for p in C['about_p'])
        body = f'''<section class="hero" aria-label="{C['slider_aria']}">
  {s_html}<div class="hero-ctrl"><div class="container"><div class="dots">{dots}</div>
  <div class="arrows"><button class="prev" aria-label="{C['prev']}"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button><button class="next" aria-label="{C['next']}"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button></div></div></div>
</section>

<section class="features-bar"><div class="container">{fbar}</div></section>

<section class="section">
  <div class="container split">
    <div class="split-media">
      <img class="main" loading="lazy" src="{self.img('plans.jpg')}" alt="{C['plans_alt']}">
      <div class="badge"><b>{'12+' if self.C['lang'] == 'en' else '+12'}</b><span>{C['years_exp']}</span></div>
    </div>
    <div class="split-text">
      <span class="s-label">{C['about_label']}</span>
      <h2>{C['about_title']}</h2>
      {about_p}
      {self.checks(C['about_checks'])}
      <a class="btn btn-primary" href="about.html">{C['about_btn']}</a>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    {self.s_head(C['svc_label'], C['svc_title'], C['svc_text'])}
    <div class="services-grid">{svc_cards}</div>
  </div>
</section>

{self.stats([(12, True), (340, True), (45, False), (18, False)], C['stats'])}

<section class="section">
  <div class="container">
    {self.s_head(C['why_label'], C['why_title'], C['why_text'])}
    <div class="why-grid">{why}</div>
  </div>
</section>

<section class="banner-split">
  <div class="media" role="img" aria-label="{C['band_alt']}"></div>
  <div class="content">
    <span class="s-label">{C['band_label']}</span>
    <h2>{C['band_title']}</h2>
    <p>{C['band_text']}</p>
    <ul class="types-mini">{band}</ul>
    <div><a class="btn btn-gold" href="solar.html">{C['band_btn']}</a></div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    {self.s_head(C['proj_label'], C['proj_title'], C['proj_text'])}
    <div class="projects-grid">{projs}</div>
    <div class="center-btn"><a class="btn btn-line" href="projects.html">{C['proj_all_btn']}</a></div>
  </div>
</section>

{self.cta()}'''
        return C['index_title'], C['index_desc'], body

    def about(self):
        C = self.C
        vals = ''.join(f'<div class="value">{ico(i)}<div><h4>{t}</h4><p>{d}</p></div></div>' for i, t, d in C['values'])
        goals = ''.join(f'<li>{g}</li>' for g in C['goals'][1])
        ab_p = ''.join(f'<p>{p}</p>' for p in C['ab_p'])
        body = f'''{self.page_head(*C['about_page'], 'towers.jpg')}

<section class="section">
  <div class="container split">
    <div class="split-text">
      <span class="s-label">{C['ab_label']}</span>
      <h2>{C['ab_title']}</h2>
      {ab_p}
      {self.checks(C['ab_checks'])}
    </div>
    <div class="split-media">
      <img class="main" loading="lazy" src="{self.img('site.jpg')}" alt="{C['site_alt']}">
      <div class="badge"><b>2012</b><span>{C['founded']}</span></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    {self.s_head(C['vmv_label'], C['vmv_title'], '', True)}
    <div class="vmv">
      <div class="vmv-card">{ico('eye')}<h3>{C['vision'][0]}</h3><p>{C['vision'][1]}</p></div>
      <div class="vmv-card">{ico('flag')}<h3>{C['mission'][0]}</h3><p>{C['mission'][1]}</p></div>
      <div class="vmv-card">{ico('target')}<h3>{C['goals'][0]}</h3><ul>{goals}</ul></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {self.s_head(C['val_label'], C['val_title'], C['val_text'])}
    <div class="values-grid">{vals}</div>
  </div>
</section>

<section class="section alt">
  <div class="container message">
    <img loading="lazy" src="{self.img('handshake.jpg')}" alt="{C['msg_alt']}">
    <div>
      <span class="s-label">{C['msg_label']}</span>
      <h2 class="msg-title">{C['msg_title']}</h2>
      <blockquote>{C['msg_text']}</blockquote>
      <cite>{C['msg_cite']}<small>{C['company_formal']}</small></cite>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split-media"><img class="main" loading="lazy" src="{self.img('construction.jpg')}" alt="{C['q_alt']}"></div>
    <div class="split-text">
      <span class="s-label">{C['q_label']}</span>
      <h2>{C['q_title']}</h2>
      <p>{C['q_text']}</p>
      {self.checks(C['q_checks'], True)}
    </div>
  </div>
</section>

{self.cta()}'''
        return C['about_page'][0], C['about_desc'], body

    def services(self):
        C = self.C
        nav = ''.join(f'<a href="#{k}">{ico(ic)}{t}</a>' for k, ic, t, _, _ in C['services'])
        secs = ''
        for i, (k, ic, t, img, _) in enumerate(C['services']):
            text, items = C['svc_detail'][k]
            if k == 'solar':
                link = f'<a class="btn btn-line" href="solar.html">{C["solar_details_btn"]}</a>'
            else:
                link = f'<a class="btn btn-primary" href="contact.html">{C["quote_btn"]}</a>'
            alt_cls = ' alt' if i % 2 else ''
            rev_cls = ' rev' if i % 2 else ''
            secs += f'''<section class="section{alt_cls}" id="{k}">
  <div class="container svc-detail{rev_cls}">
    <div class="svc-detail-media"><img loading="lazy" src="{self.img(img)}" alt="{t}"><img class="sub" loading="lazy" src="{self.img(SVC_SUB[k])}" alt=""></div>
    <div>
      <h2>{ico(ic)}{t}</h2>
      <p>{text}</p>
      {self.checks(items)}
      {link}
    </div>
  </div>
</section>
'''
        body = f'''{self.page_head(*C['services_page'], 'containers.jpg')}
<nav class="svc-nav" aria-label="{C['svc_nav_aria']}"><div class="container">{nav}</div></nav>
{secs}
{self.cta()}'''
        return C['services_page'][0], C['services_desc'], body

    def solar(self):
        C = self.C
        types = ''
        for img, (t, en, d, fit) in zip(TYPE_IMG, C['types']):
            sub = f'<span class="type-en">{en}</span>' if en else ''
            types += f'<article class="type"><img loading="lazy" src="{self.img(img)}" alt="{t}"><div class="type-body"><h3>{t}</h3>{sub}<p>{d}</p><p class="fit"><b>{C["fit"]} </b>{fit}</p></div></article>'
        comps = ''.join(f'<div class="comp">{ico(i)}<h4>{t}</h4><p>{d}</p></div>' for i, t, d in C['comps'])
        steps = ''.join(f'<li><h4>{t}</h4><p>{d}</p></li>' for t, d in C['steps'])
        war = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in C['warranty'])
        uses = ''.join(f'<option value="{v}">{t}</option>' for v, t in zip(['home', 'shop', 'farm', 'factory'], C['calc_uses']))
        res = C['calc_res']
        si_p = ''.join(f'<p>{p}</p>' for p in C['si_p'])
        body = f'''{self.page_head(*C['solar_page'], 'solar-plant.jpg')}

<section class="section">
  <div class="container split">
    <div class="split-text">
      <span class="s-label">{C['si_label']}</span>
      <h2>{C['si_title']}</h2>
      {si_p}
      {self.checks(C['si_checks'])}
    </div>
    <div class="split-media"><img class="main" loading="lazy" src="{self.img('solar-install.jpg')}" alt="{C['si_alt']}"></div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    {self.s_head(C['types_label'], C['types_title'], C['types_text'])}
    <div class="types-grid">{types}</div>
  </div>
</section>

<section class="section navy">
  <div class="container">
    {self.s_head(C['comp_label'], C['comp_title'], C['comp_text'])}
    <div class="comp-grid">{comps}</div>
  </div>
</section>

<section class="section" id="calc-section">
  <div class="container">
    {self.s_head(C['calc_label'], C['calc_title'], C['calc_text'])}
    <div class="calc" id="calc">
      <div class="calc-in">
        <h3>{C['calc_in']}</h3>
        <p>{C['calc_hint']}</p>
        <label class="field" for="c-use"><span>{C['calc_use']}</span><select id="c-use">{uses}</select></label>
        <label class="field" for="c-amp"><span>{C['calc_amp']}</span>
          <div class="range"><input type="range" id="c-amp" min="2" max="100" value="15"><output id="o-amp" for="c-amp">15</output></div></label>
        <label class="field" for="c-day"><span>{C['calc_day']}</span>
          <div class="range"><input type="range" id="c-day" min="2" max="12" value="8"><output id="o-day" for="c-day">8</output></div></label>
        <label class="field" for="c-night"><span>{C['calc_night']}</span>
          <div class="range"><input type="range" id="c-night" min="0" max="12" value="6"><output id="o-night" for="c-night">6</output></div></label>
      </div>
      <div class="calc-out">
        <h3>{C['calc_out']}</h3>
        <div class="res">
          <div><b id="r-kwp">7.6</b><span>{res[0]}</span></div>
          <div><b id="r-pan">13</b><span>{res[1]}</span></div>
          <div><b id="r-inv">5</b><span>{res[2]}</span></div>
          <div><b id="r-bat">16</b><span>{res[3]}</span></div>
        </div>
        <p class="rec">{C['calc_rec']} <strong id="r-type">Hybrid</strong></p>
        <p class="note">{C['calc_note']}</p>
        <a class="btn btn-gold" id="calc-book" href="contact.html" target="_blank" rel="noopener">{C['calc_book']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    {self.s_head(C['steps_label'], C['steps_title'], '', True)}
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section">
  <div class="container">
    {self.s_head(C['war_label'], C['war_title'], C['war_text'])}
    <div class="warranty">{war}</div>
  </div>
</section>

{self.cta(*C['solar_cta'])}'''
        return C['solar_page'][0], C['solar_desc'], body

    def projects(self):
        C = self.C
        filt = ''.join(f'<button{ACT if k == "all" else ""} data-filter="{k}">{t}</button>' for k, t in C['filters'])
        cards = ''.join(self.proj_card(i) for i in range(len(PROJ_META)))
        body = f'''{self.page_head(*C['projects_page'], 'hero-construction.jpg')}

<section class="section">
  <div class="container">
    <div class="filters" role="group" aria-label="{C['filters_aria']}">{filt}</div>
    <div class="projects-grid">{cards}</div>
  </div>
</section>

{self.stats([(340, True), (120, True), (1500, True), (600, True)], C['pstats'])}

{self.cta()}'''
        return C['projects_page'][0], C['projects_desc'], body

    def contact(self):
        C = self.C
        svc_opts = ''.join(f'<option>{t}</option>' for _, _, t, _, _ in C['services'])
        city_opts = ''.join(f'<option>{c}</option>' for c in C['cities'])
        hours = ''.join(f'<li><span>{a}</span><span>{b}</span></li>' for a, b in C['hours'])
        cc = C['cc']
        body = f'''{self.page_head(*C['contact_page'], 'hero-port.jpg')}

<section class="section">
  <div class="container">
    <div class="contact-cards">
      <div class="c-card">{ico('pin')}<h4>{cc[0]}</h4><p>{C['address']}</p></div>
      <div class="c-card">{ico('map')}<h4>{cc[1]}</h4><p>{C['branch']}</p></div>
      <div class="c-card">{ico('phone')}<h4>{cc[2]}</h4><p><span>{PHONE1}</span><br><span>{PHONE2}</span><br><span>{PHONE3}</span></p></div>
      <div class="c-card">{ico('mail')}<h4>{cc[3]}</h4><p>{EMAIL}<br>{EMAIL2}</p></div>
    </div>

    <div class="contact-wrap">
      <form class="form-box" id="contact-form" novalidate>
        <h3>{C['form_title']}</h3>
        <p>{C['form_text']}</p>
        <div class="row2">
          <label class="field" for="f-name"><span>{C['f_name']}</span><input id="f-name" name="name" autocomplete="name" placeholder="{C['f_name_ph']}"><span class="err">{C['f_name_err']}</span></label>
          <label class="field" for="f-phone"><span>{C['f_phone']}</span><input id="f-phone" name="phone" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="07XX XXX XXXX"><span class="err">{C['f_phone_err']}</span></label>
        </div>
        <div class="row2">
          <label class="field" for="f-service"><span>{C['f_service']}</span><select id="f-service" name="service">{svc_opts}</select></label>
          <label class="field" for="f-city"><span>{C['f_city']}</span><select id="f-city" name="city">{city_opts}</select></label>
        </div>
        <label class="field" for="f-msg"><span>{C['f_msg']}</span><textarea id="f-msg" name="msg" placeholder="{C['f_msg_ph']}"></textarea></label>
        <button class="btn btn-primary" type="submit"><svg viewBox="0 0 24 24" fill="currentColor">{WA_PATH}</svg>{C['f_submit']}</button>
        <div class="form-result" id="form-result" role="status">{C['f_result']} <a href="#" target="_blank" rel="noopener">{C['f_result_link']}</a>.</div>
      </form>

      <aside class="map-box">
        <div class="in">
          <h3>{C['hours_title']}</h3>
          <p>{C['hours_text']}</p>
          <ul class="hours">{hours}</ul>
          <a class="btn btn-gold" href="https://www.google.com/maps/search/?api=1&amp;query=Palestine+Street+Baghdad" target="_blank" rel="noopener">{ico('pin')}{C['map_btn']}</a>
        </div>
      </aside>
    </div>
  </div>
</section>'''
        return C['contact_page'][0], C['contact_desc'], body

    def render(self, bare=False):
        C = self.C
        fn = {'index.html': self.index, 'about.html': self.about, 'services.html': self.services,
              'solar.html': self.solar, 'projects.html': self.projects, 'contact.html': self.contact}[self.fname]
        title, desc, body = fn()
        inner = f'''{self.header()}
<main>
{body}
</main>
{self.footer()}'''
        if bare:  # نسخة المعاينة: الصفحة الرئيسية بدون هيكل المستند (يضيفه المضيف)
            return f'''{self.head(title, desc)}
<script>document.documentElement.lang='{C['lang']}';document.documentElement.dir='{C['dir']}';</script>
{inner}
'''
        return f'''<!doctype html>
<html lang="{C['lang']}" dir="{C['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{self.head(title, desc)}
</head>
<body>
{inner}
</body>
</html>
'''


count = 0
for code, folder in LANGS:
    for fname in FILES:
        p = Page(LC[code], folder, fname)
        targets = [(OUT, False)]
        if ART:
            targets.append((ART, folder == '' and fname == 'index.html'))
        for base, bare in targets:
            os.makedirs(os.path.join(base, folder), exist_ok=True)
            with open(os.path.join(base, folder, fname), 'w') as fh:
                fh.write(p.render(bare))
        count += 1
print('built', count, 'pages')
