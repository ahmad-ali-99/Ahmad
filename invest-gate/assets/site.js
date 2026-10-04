/* إنفست جيت — السكربت العام */
(function () {
  // رقم واتساب الشركة بالصيغة الدولية (بدون + وبدون أصفار في البداية)
  var WHATSAPP = '9647700000000';

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var waLink = function (text) { return 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(text); };

  /* الرأس والقائمة */
  var header = $('.header');
  var onScroll = function () { header.classList.toggle('shadow', window.scrollY > 10); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var menuBtn = $('.menu-btn'), nav = $('.nav');
  menuBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
  });

  /* زر واتساب العائم */
  $$('[data-wa]').forEach(function (a) {
    a.href = waLink('السلام عليكم، أود الاستفسار عن خدمات شركة إنفست جيت.');
  });

  /* السلايدر */
  var slides = $$('.slide');
  if (slides.length) {
    var dots = $$('.dots button'), cur = 0, timer;
    var go = function (n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('active', i === cur); s.setAttribute('aria-hidden', i !== cur); });
      dots.forEach(function (d, i) { d.classList.toggle('active', i === cur); });
    };
    var play = function () { clearInterval(timer); timer = setInterval(function () { go(cur + 1); }, 7000); };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); play(); }); });
    $('.prev').addEventListener('click', function () { go(cur - 1); play(); });
    $('.next').addEventListener('click', function () { go(cur + 1); play(); });
    play();
  }

  /* عدّاد الأرقام */
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, end = +el.dataset.count, pre = el.dataset.prefix || '', t0 = performance.now();
        var step = function (t) {
          var p = Math.min((t - t0) / 1400, 1);
          el.textContent = pre + Math.round(end * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        io.unobserve(el);
      });
    }, { threshold: .5 });
    counters.forEach(function (c) { io.observe(c); });
  }

  /* فلترة المشاريع */
  $$('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('.filters button').forEach(function (x) { x.classList.toggle('active', x === b); });
      var f = b.dataset.filter;
      $$('.proj').forEach(function (p) { p.classList.toggle('hidden', f !== 'all' && p.dataset.cat !== f); });
    });
  });

  /* قائمة الخدمات الفرعية */
  var subLinks = $$('.svc-nav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        subLinks.forEach(function (l) { l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    subLinks.forEach(function (l) { var t = $(l.getAttribute('href')); if (t) spy.observe(t); });
  }

  /* حاسبة المنظومة الشمسية */
  var calc = $('#calc');
  if (calc) {
    var SUN = 5.5, EFF = 0.78, PANEL = 585, DOD = 0.9, DIVERSITY = 0.7;
    var f = { use: $('#c-use'), amp: $('#c-amp'), day: $('#c-day'), night: $('#c-night') };
    var hrs = function (n) { return n === 0 ? 'لا يوجد' : n === 1 ? 'ساعة' : n === 2 ? 'ساعتان' : n <= 10 ? n + ' ساعات' : n + ' ساعة'; };
    var update = function () {
      var amp = +f.amp.value, day = +f.day.value, night = +f.night.value, use = f.use.value;
      $('#o-amp').textContent = amp + ' أمبير';
      $('#o-day').textContent = hrs(day);
      $('#o-night').textContent = hrs(night);
      var kw = amp * 220 / 1000;
      var energy = kw * (day + night) * DIVERSITY;
      var panels = Math.max(2, Math.ceil(energy / (SUN * EFF) * 1000 / PANEL));
      $('#r-kwp').textContent = (Math.round(panels * PANEL / 100) / 10).toString();
      $('#r-pan').textContent = panels;
      $('#r-inv').textContent = Math.max(3, Math.ceil(kw * 1.25));
      $('#r-bat').textContent = night ? Math.ceil(kw * night * DIVERSITY / DOD) : 0;
      $('#r-type').textContent =
        use === 'farm' && night === 0 ? 'منظومة ضخ مباشر بدون بطاريات' :
        night === 0 ? 'منظومة مرتبطة بالشبكة (On-Grid)' :
        use === 'farm' ? 'منظومة مستقلة (Off-Grid)' : 'منظومة هجينة (Hybrid)';
    };
    Object.keys(f).forEach(function (k) { f[k].addEventListener('input', update); });
    update();
    var book = $('#calc-book');
    var setBook = function () {
      book.href = waLink('السلام عليكم، أرغب بحجز زيارة كشف لمنظومة طاقة شمسية.\nالحمل التقريبي: ' + f.amp.value +
        ' أمبير\nساعات التشغيل النهارية: ' + f.day.value + '\nساعات التشغيل الليلية: ' + f.night.value);
    };
    Object.keys(f).forEach(function (k) { f[k].addEventListener('input', setBook); });
    setBook();
  }

  /* نموذج التواصل */
  var form = $('#contact-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    if (params.get('service')) form.elements.service.value = params.get('service');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      [['name', function (v) { return v.trim().length > 1; }], ['phone', function (v) { return v.replace(/\D/g, '').length >= 10; }]]
        .forEach(function (r) {
          var input = form.elements[r[0]], valid = r[1](input.value);
          input.closest('.field').classList.toggle('invalid', !valid);
          if (!valid) ok = false;
        });
      if (!ok) return;
      var d = form.elements;
      var text = 'طلب عرض سعر من الموقع الإلكتروني\n' +
        'الاسم: ' + d.name.value.trim() + '\n' +
        'رقم الهاتف: ' + d.phone.value.trim() + '\n' +
        'الخدمة المطلوبة: ' + d.service.value + '\n' +
        'المحافظة: ' + d.city.value +
        (d.msg.value.trim() ? '\nالتفاصيل: ' + d.msg.value.trim() : '');
      var url = waLink(text);
      var res = $('#form-result');
      $('a', res).href = url;
      res.classList.add('show');
      try { window.open(url, '_blank', 'noopener'); } catch (err) { /* يبقى الرابط ظاهراً */ }
    });
  }

  var yr = $('#year');
  if (yr) yr.textContent = new Date().getFullYear();
})();
