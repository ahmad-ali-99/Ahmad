/**
 * النسخة الثالثة — قاعدة بيانات عشيرة السوره ميري
 * يحفظ التسجيلات في الجدول + يرسل نسخة واتساب تلقائية للمشرف مع كل تسجيل.
 *
 * ملاحظة: النسخة التلقائية تعمل عبر خدمة CallMeBot المجانية —
 * اتبع خطوات التفعيل في المحادثة، ثم ضع المفتاح في CALLMEBOT_KEY أدناه.
 */

var SHEET_NAME = 'البيانات';
var ADMIN_PHONE = '+9647728736250';
var CALLMEBOT_KEY = 'PUT_YOUR_KEY_HERE'; // ← بدّل هذا بمفتاحك من CallMeBot

/* إرسال نسخة واتساب للمشرف (لا يؤثر على الحفظ إذا فشل) */
function notifyWhatsApp(p) {
  try {
    if (!CALLMEBOT_KEY || CALLMEBOT_KEY === 'PUT_YOUR_KEY_HERE') return;
    var msg = '📋 تسجيل جديد — عشيرة السوره ميري\n' +
      '👤 رب الأسرة: ' + (p.fullName || '') + '\n' +
      '📞 الهاتف: ' + (p.phone || '') + '\n' +
      '🏠 العنوان: ' + (p.address || '') + '\n' +
      '👥 الأولاد (' + (p.sonsCount || '0') + '): ' + (p.sons || 'لا يوجد');
    if (p.lat && p.lng) {
      msg += '\n📍 الموقع: https://www.google.com/maps?q=' + p.lat + ',' + p.lng;
    }
    var url = 'https://api.callmebot.com/whatsapp.php' +
      '?phone=' + encodeURIComponent(ADMIN_PHONE) +
      '&apikey=' + encodeURIComponent(CALLMEBOT_KEY) +
      '&text=' + encodeURIComponent(msg);
    UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  } catch (e) { /* الإشعار اختياري — الحفظ بالجدول لا يتأثر */ }
}

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
  notifyWhatsApp(p);
}

/* استقبال التسجيل من الاستمارة */
function doPost(e) {
  var p = (e && e.parameter) || {};
  saveRow(p);
  return ContentService.createTextOutput(JSON.stringify({ result: 'success' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.fullName) {
    saveRow(p);
    return HtmlService.createHtmlOutput('<div style="font-family:Tahoma;padding:30px;text-align:center;direction:rtl">✅ تم التسجيل، شكراً لك</div>');
  }
  return HtmlService.createHtmlOutput('<div style="font-family:Tahoma;padding:30px;text-align:center;direction:rtl">✅ قاعدة بيانات العشيرة شغالة</div>');
}
