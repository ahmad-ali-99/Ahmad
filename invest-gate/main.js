/* إنفست جيت — main.js */
(() => {
  // رقم الواتساب الذي تصله الطلبات (بالصيغة الدولية بدون + أو أصفار)
  const WHATSAPP = '9647700000000';

  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- header ---------- */
  const header = $('.site-header');
  const onScroll = () => header.classList.toggle('scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const burger = $('#burger'), menu = $('#menu');
  burger.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });
  $$('#menu a').forEach(a => a.addEventListener('click', () => {
    menu.classList.remove('open');
    burger.setAttribute('aria-expanded', false);
  }));

  // active menu link
  const links = $$('#menu a');
  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  $$('main section[id]').forEach(s => spy.observe(s));

  /* ---------- hero slideshow ---------- */
  const slides = $$('.hs'), idx = $$('.hi');
  let cur = 0, timer;
  const show = n => {
    cur = (n + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('is-on', i === cur));
    idx.forEach((b, i) => {
      b.classList.remove('is-on');
      if (i === cur) { void b.offsetWidth; b.classList.add('is-on'); }
    });
  };
  const play = () => { clearInterval(timer); timer = setInterval(() => show(cur + 1), 6000); };
  idx.forEach(b => b.addEventListener('click', () => { show(+b.dataset.slide); play(); }));
  play();

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal').forEach((el, i) => {
    if (!el.closest('.hero')) el.style.transitionDelay = (i % 4) * 70 + 'ms';
    io.observe(el);
  });
  requestAnimationFrame(() => $$('.hero .reveal').forEach(el => el.classList.add('in')));

  /* ---------- counters ---------- */
  const fmt = new Intl.NumberFormat('en-US');
  const countIO = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target, end = +el.dataset.count, suf = el.dataset.suffix || '';
      const t0 = performance.now(), dur = 1600;
      const step = t => {
        const p = Math.min((t - t0) / dur, 1), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
        el.textContent = fmt.format(v) + suf;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      countIO.unobserve(el);
    });
  }, { threshold: .6 });
  $$('[data-count]').forEach(el => countIO.observe(el));

  /* ---------- division tabs ---------- */
  const tabs = $$('.dt');
  const openTab = key => {
    tabs.forEach(t => {
      const on = t.dataset.tab === key;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on);
    });
    $$('.dp').forEach(p => p.classList.toggle('is-on', p.id === 'tab-' + key));
  };
  tabs.forEach(t => t.addEventListener('click', () => {
    openTab(t.dataset.tab);
    t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
  }));
  $$('[data-go]').forEach(a => a.addEventListener('click', () => openTab(a.dataset.go)));

  // links that preselect a service in the quote form
  const qService = $('#q-service');
  $$('[data-service]').forEach(a => a.addEventListener('click', () => { qService.value = a.dataset.service; }));

  /* ---------- project filter ---------- */
  $$('.f').forEach(b => b.addEventListener('click', () => {
    $$('.f').forEach(x => x.classList.toggle('is-on', x === b));
    const f = b.dataset.f;
    $$('.pj').forEach(p => p.classList.toggle('hide', f !== 'all' && p.dataset.cat !== f));
  }));

  /* ---------- solar calculator ---------- */
  const SUN_HOURS = 5.5;      // متوسط ساعات الذروة الشمسية في العراق
  const LOSSES = 0.78;        // كفاءة المنظومة بعد الفقد (حرارة، غبار، أسلاك)
  const PANEL_W = 585;
  const DOD = 0.9;            // عمق التفريغ لبطاريات الليثيوم
  const c = { use: $('#c-use'), amp: $('#c-amp'), day: $('#c-day'), night: $('#c-night') };
  const r = { kwp: $('#r-kwp'), pan: $('#r-pan'), inv: $('#r-inv'), bat: $('#r-bat'), type: $('#r-type') };
  const one = n => (Math.round(n * 10) / 10).toString();

  const calc = () => {
    const amp = +c.amp.value, day = +c.day.value, night = +c.night.value, use = c.use.value;
    $('#o-amp').textContent = amp + ' أمبير';
    $('#o-day').textContent = day + (day > 10 ? ' ساعة' : ' ساعات');
    $('#o-night').textContent = night === 0 ? 'بدون' : night + (night > 10 ? ' ساعة' : night > 2 ? ' ساعات' : ' ساعة');

    const kw = amp * 220 / 1000;                       // الحمل اللحظي
    const energy = kw * (day + night) * 0.7;           // معامل تزامن الأحمال
    const kwp = energy / (SUN_HOURS * LOSSES);
    const panels = Math.max(2, Math.ceil(kwp * 1000 / PANEL_W));
    const inv = Math.max(3, Math.ceil(kw * 1.25));
    const bat = night ? Math.ceil((kw * night * 0.7) / DOD) : 0;

    r.kwp.textContent = one(panels * PANEL_W / 1000);
    r.pan.textContent = panels;
    r.inv.textContent = inv;
    r.bat.textContent = bat;
    r.type.textContent =
      use === 'farm' && night === 0 ? 'منظومة ضخ مباشر بدون بطاريات' :
      night === 0 ? 'مرتبطة بالشبكة (On-Grid)' :
      use === 'farm' ? 'مستقلة (Off-Grid) مع بطاريات ليثيوم' :
      'هجينة (Hybrid) مع بطاريات ليثيوم';
  };
  Object.values(c).forEach(el => el.addEventListener('input', calc));
  calc();

  $('#calc-cta').addEventListener('click', () => {
    qService.value = 'الطاقة الشمسية';
    const msg = $('#qform [name=msg]');
    if (!msg.value.trim()) {
      msg.value = `أرغب بزيارة كشف لمنظومة شمسية. الحمل التقريبي ${c.amp.value} أمبير، تشغيل نهاري ${c.day.value} ساعات وليلي ${c.night.value} ساعات. الحاسبة اقترحت ${r.pan.textContent} لوح وانفرتر ${r.inv.textContent} ك.واط وبطاريات ${r.bat.textContent} ك.واط ساعة.`;
    }
  });

  /* ---------- quote form → WhatsApp ---------- */
  const form = $('#qform'), out = $('#form-msg');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form));
    let ok = true;
    ['name', 'phone'].forEach(k => {
      const el = form.elements[k];
      const bad = k === 'phone' ? d.phone.replace(/\D/g, '').length < 10 : !d[k].trim();
      el.classList.toggle('invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { out.textContent = 'رجاءً اكتب الاسم ورقم هاتف صحيح.'; return; }

    const text = [
      'طلب عرض سعر — موقع إنفست جيت',
      `الاسم: ${d.name.trim()}`,
      `الهاتف: ${d.phone.trim()}`,
      `الخدمة: ${d.service}`,
      `المحافظة: ${d.city}`,
      d.msg.trim() && `التفاصيل: ${d.msg.trim()}`
    ].filter(Boolean).join('\n');

    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
    out.textContent = 'تم تجهيز طلبك في واتساب، اضغط إرسال لإكماله. شكراً لتواصلك معنا.';
    form.reset();
  });

  $('#wa-float').href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent('السلام عليكم، أرغب بالاستفسار عن خدماتكم.')}`;
  $('#yr').textContent = new Date().getFullYear();
})();
