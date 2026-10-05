# مصدر موقع إنفست جيت

الموقع المنشور: https://ahmad-ali-99.github.io/investgate/ (مستودع `ahmad-ali-99/investgate`).

| المجلد / الملف | المحتوى |
|---|---|
| `i18n/ar.py` · `i18n/ku.py` · `i18n/en.py` | جميع نصوص الموقع بالعربية والكوردية والإنكليزية |
| `build.py` (الأسطر الأولى) | أرقام الهواتف والبريد الإلكتروني ورابط الخريطة |
| `assets/js/main.js` (أول سطر) | رقم واتساب الذي تصله الطلبات |
| `assets/css/main.css` | التصميم والألوان |
| `assets/vendor/` | مكتبات الحركة: GSAP + ScrollTrigger + Lenis |
| `assets/fonts/` | الخطوط: Reem Kufi · IBM Plex Sans Arabic · Archivo · IBM Plex Sans |
| `img/` | الصور بصيغة WebP بمقاسين |

للتوليد (يحتاج Python 3 و Pillow):

```
python3 invest-gate-src/build.py
```

تُكتب الصفحات في مجلد `invest-gate/`، ثم تُنسخ إلى مستودع `investgate` للنشر.
