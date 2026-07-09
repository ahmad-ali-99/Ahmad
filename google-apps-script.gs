/**
 * كود Google Apps Script — قاعدة بيانات عشيرة السوره ميري
 *
 * هذا الكود يستقبل البيانات من الاستمارة (index.html)
 * ويخزنها في جدول Google Sheets بشكل تلقائي.
 *
 * طريقة التنصيب موجودة بالتفصيل في ملف README.md
 */

var SHEET_NAME = 'البيانات';

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);

    // إذا الورقة غير موجودة، أنشئها مع رؤوس الأعمدة
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'التاريخ والوقت',
        'الاسم الكامل',
        'رقم الهاتف',
        'العنوان',
        'خط العرض (Lat)',
        'خط الطول (Lng)',
        'رابط الموقع على الخريطة'
      ]);
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#d9ead3');
      sheet.setFrozenRows(1);
    }

    var p = e.parameter;
    var lat = p.lat || '';
    var lng = p.lng || '';
    var mapLink = (lat && lng) ? 'https://www.google.com/maps?q=' + lat + ',' + lng : '';

    sheet.appendRow([
      new Date(),
      p.fullName || '',
      p.phone || '',
      p.address || '',
      lat,
      lng,
      mapLink
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// دالة تجريبية للتأكد أن التطبيق منشور وشغال (افتح رابط التطبيق بالمتصفح)
function doGet() {
  return ContentService.createTextOutput('✅ قاعدة بيانات العشيرة شغالة');
}
