/**
 * النسخة الثانية — قاعدة بيانات عشيرة السوره ميري
 * يستقبل التسجيلات ويحفظها في الجدول، ويعرض صفحة تأكيد جميلة للمسجّل.
 */

var SHEET_NAME = 'البيانات';

function saveRow(p) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['التاريخ والوقت', 'رب الأسرة', 'رقم الهاتف', 'العنوان', 'الأولاد وأرقامهم', 'عدد الأولاد', 'رابط الموقع على الخريطة']);
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#d9ead3');
      sheet.setFrozenRows(1);
    }
    var lat = p.lat || '';
    var lng = p.lng || '';
    var mapLink = (lat && lng) ? 'https://www.google.com/maps?q=' + lat + ',' + lng : '';
    sheet.appendRow([
      new Date(),
      p.fullName || '',
      p.phone || '',
      p.address || '',
      p.sons || '',
      p.sonsCount || '0',
      mapLink
    ]);
  } finally {
    lock.releaseLock();
  }
}

function successPage(p) {
  var waBtn = '';
  var to = (p.to || '').replace(/\D/g, '');
  if (/^\d{8,15}$/.test(to)) {
    var msg = '📋 تسجيل أسرة — عشيرة السوره ميري\n' +
      '👤 رب الأسرة: ' + (p.fullName || '') + '\n' +
      '📞 الهاتف: ' + (p.phone || '') + '\n' +
      '🏠 العنوان: ' + (p.address || '') + '\n' +
      '👥 الأولاد: ' + (p.sons || 'لا يوجد');
    if (p.lat && p.lng) msg += '\n📍 الموقع: https://www.google.com/maps?q=' + p.lat + ',' + p.lng;
    waBtn = '<a class="wa" target="_blank" href="https://wa.me/' + to +
      '?text=' + encodeURIComponent(msg) + '">📱 دز نسخة على واتساب المشرف (اختياري)</a>';
  }
  var html = '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<style>body{font-family:Tahoma,Arial,sans-serif;background:linear-gradient(135deg,#1a2a3a,#2c4a3e);' +
    'min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;margin:0}' +
    '.card{background:#fff;max-width:430px;width:100%;border-radius:16px;padding:34px 26px;text-align:center;' +
    'box-shadow:0 20px 60px rgba(0,0,0,.35)}' +
    '.tick{font-size:54px;margin-bottom:10px}' +
    'h1{font-size:20px;color:#14532d;margin:0 0 8px}' +
    'p{font-size:14px;color:#555;line-height:1.8;margin:0 0 18px}' +
    'a{display:block;text-decoration:none;font-weight:700;border-radius:10px;padding:13px;margin-top:10px;font-size:15px}' +
    '.wa{background:#1da851;color:#fff}' +
    '.back{background:#eef4ee;color:#14532d;border:1.5px solid #14532d;cursor:pointer;width:100%;font:inherit;font-weight:700;border-radius:10px;padding:13px;margin-top:10px;font-size:15px}' +
    '</style></head><body><div class="card">' +
    '<div class="tick">✅</div>' +
    '<h1>انحفظت بياناتك بقاعدة بيانات العشيرة</h1>' +
    '<p>شكراً لك، تم تسجيل الأسرة بنجاح.</p>' +
    waBtn +
    '<button class="back" onclick="history.back()">⬅ رجوع للاستمارة</button>' +
    '</div></body></html>';
  return HtmlService.createHtmlOutput(html)
    .setTitle('تم التسجيل — عشيرة السوره ميري')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0');
}

/* استقبال التسجيل عبر رابط مباشر (من الاستمارة) */
function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.fullName) {
    saveRow(p);
    return successPage(p);
  }
  return HtmlService.createHtmlOutput('<div style="font-family:Tahoma;padding:30px;text-align:center;direction:rtl">✅ قاعدة بيانات العشيرة شغالة</div>');
}

/* استقبال التسجيل عبر POST (للتوافق) */
function doPost(e) {
  var p = (e && e.parameter) || {};
  saveRow(p);
  return ContentService.createTextOutput(JSON.stringify({ result: 'success' }))
    .setMimeType(ContentService.MimeType.JSON);
}
