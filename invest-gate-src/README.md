# مصدر موقع إنفست جيت

صفحات الموقع في مجلد `invest-gate/` تُولَّد من هذا المجلد، بثلاث لغات:

| اللغة | ملف النصوص | مكان الصفحات |
|---|---|---|
| العربية | `i18n/ar.py` | `invest-gate/` |
| الكوردية (سۆرانی) | `i18n/ku.py` | `invest-gate/ku/` |
| English | `i18n/en.py` | `invest-gate/en/` |

- أرقام الهواتف والبريد الإلكتروني: أعلى ملف `common.py`.
- رقم واتساب الذي تصله الطلبات: أول سطر في `invest-gate/assets/site.js`.

بعد أي تعديل شغّل:

```
python3 invest-gate-src/build.py
```
