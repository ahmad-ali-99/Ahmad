/**
 * ✨ الحل الكامل بملف واحد — قاعدة بيانات عشيرة السوره ميري ✨
 *
 * هذا الملف يسوي كلشي داخل جوجل:
 *   1. الاستمارة (صفحة التسجيل) — نفس رابط التطبيق يفتح الاستمارة مباشرة
 *   2. قاعدة البيانات — كل تسجيل ينحفظ سطر جديد في Google Sheets
 *
 * طريقة التشغيل (3 خطوات فقط):
 *   1. افتح جدول جديد في sheets.google.com ثم: Extensions ← Apps Script
 *   2. احذف الكود الموجود والصق محتوى هذا الملف كامل، ثم احفظ 💾
 *   3. Deploy ← New deployment ← ⚙️ Web app ← (Execute as: Me) ←
 *      (Who has access: Anyone) ← Deploy
 *
 * الرابط الذي يطلع لك (ينتهي بـ /exec) هو رابط الاستمارة —
 * دزّه بگروب العشيرة وكل شخص يسجل بياناته وتوصلك بالجدول فوراً.
 */

var SHEET_NAME = 'البيانات';

/* ========== فتح الاستمارة ========== */
function doGet() {
  return HtmlService.createHtmlOutput(FORM_HTML)
    .setTitle('قاعدة بيانات عشيرة السوره ميري')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/* ========== حفظ البيانات في الجدول ========== */
function saveData(data) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(SHEET_NAME);

    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'التاريخ والوقت', 'الاسم الكامل', 'رقم الهاتف', 'العنوان',
        'خط العرض (Lat)', 'خط الطول (Lng)', 'رابط الموقع على الخريطة'
      ]);
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#d9ead3');
      sheet.setFrozenRows(1);
    }

    var mapLink = (data.lat && data.lng)
      ? 'https://www.google.com/maps?q=' + data.lat + ',' + data.lng
      : '';

    sheet.appendRow([
      new Date(),
      data.fullName || '',
      data.phone || '',
      data.address || '',
      data.lat || '',
      data.lng || '',
      mapLink
    ]);

    return { result: 'success' };
  } finally {
    lock.releaseLock();
  }
}

/* ========== صفحة الاستمارة ========== */
var FORM_HTML = '<!DOCTYPE html>' +
'<html lang="ar" dir="rtl"><head><meta charset="UTF-8">' +
'<style>' +
'*{margin:0;padding:0;box-sizing:border-box;font-family:Tahoma,Arial,sans-serif}' +
'body{min-height:100vh;background:linear-gradient(135deg,#1a2a3a,#2c4a3e);display:flex;align-items:center;justify-content:center;padding:20px}' +
'.card{background:#fff;width:100%;max-width:480px;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:hidden}' +
'.header{background:linear-gradient(135deg,#14532d,#166534);color:#fff;text-align:center;padding:28px 20px}' +
'.header h1{font-size:22px;margin-bottom:6px}.header p{font-size:13px;opacity:.85}' +
'form{padding:24px}' +
'label{display:block;font-weight:600;font-size:14px;color:#1f2937;margin:14px 0 6px}' +
'.req{color:#dc2626}' +
'input,textarea{width:100%;padding:12px;border:1.5px solid #d1d5db;border-radius:10px;font-size:15px;background:#f9fafb}' +
'input:focus,textarea:focus{outline:none;border-color:#166534;background:#fff}' +
'textarea{resize:vertical;min-height:70px}' +
'.hint{font-size:12px;color:#6b7280;margin-top:4px}' +
'.loc-box{margin-top:8px;display:flex;gap:10px;align-items:center}' +
'.btn-loc{flex-shrink:0;background:#eff6ff;color:#1d4ed8;border:1.5px solid #bfdbfe;padding:11px 16px;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer}' +
'.loc-status{font-size:13px;color:#374151}.loc-status.ok{color:#166534;font-weight:600}' +
'.btn-send{width:100%;margin-top:22px;background:linear-gradient(135deg,#14532d,#166534);color:#fff;border:none;padding:14px;border-radius:10px;font-size:17px;font-weight:700;cursor:pointer}' +
'.btn-send:disabled{opacity:.6;cursor:wait}' +
'.msg{display:none;margin-top:16px;padding:12px;border-radius:10px;font-size:14px;text-align:center}' +
'.msg.ok{display:block;background:#dcfce7;color:#14532d}' +
'.msg.err{display:block;background:#fee2e2;color:#991b1b}' +
'.footer{text-align:center;font-size:12px;color:#9ca3af;padding:0 20px 20px}' +
'</style></head><body>' +
'<div class="card">' +
'<div class="header"><h1>قاعدة بيانات عشيرة السوره ميري</h1><p>استمارة تسجيل بيانات أبناء العشيرة (ذكور فقط)</p></div>' +
'<form id="f" onsubmit="return send(event)">' +
'<label>الاسم الكامل (الرباعي واللقب) <span class="req">*</span></label>' +
'<input type="text" id="fullName" required placeholder="مثال: أحمد علي حسين محمد السوره ميري">' +
'<label>رقم الهاتف <span class="req">*</span></label>' +
'<input type="tel" id="phone" required placeholder="مثال: 07701234567">' +
'<div class="hint">رقم عراقي يبدأ بـ 07 (11 رقم)</div>' +
'<label>العنوان (المحافظة / المنطقة) <span class="req">*</span></label>' +
'<textarea id="address" required placeholder="مثال: بغداد - مدينة الصدر - قطاع 40"></textarea>' +
'<label>الموقع الجغرافي (اختياري)</label>' +
'<div class="loc-box"><button type="button" class="btn-loc" onclick="getLoc()">📍 إرسال موقعي</button>' +
'<span class="loc-status" id="locStatus">لم يتم تحديد الموقع</span></div>' +
'<input type="hidden" id="lat"><input type="hidden" id="lng">' +
'<button type="submit" class="btn-send" id="btnSend">إرسال البيانات</button>' +
'<div class="msg" id="msg"></div>' +
'</form>' +
'<div class="footer">جميع البيانات تُحفظ بشكل آمن في قاعدة بيانات العشيرة</div>' +
'</div>' +
'<script>' +
'function getLoc(){' +
'  var s=document.getElementById("locStatus");' +
'  if(!navigator.geolocation){s.textContent="المتصفح لا يدعم تحديد الموقع";return}' +
'  s.textContent="جاري تحديد الموقع...";' +
'  navigator.geolocation.getCurrentPosition(function(p){' +
'    document.getElementById("lat").value=p.coords.latitude.toFixed(6);' +
'    document.getElementById("lng").value=p.coords.longitude.toFixed(6);' +
'    s.textContent="✅ تم تحديد الموقع بنجاح";s.className="loc-status ok";' +
'  },function(){' +
'    s.textContent="تعذر تحديد الموقع — اكتب أقرب معلم بالعنوان";' +
'  },{enableHighAccuracy:true,timeout:15000});' +
'}' +
'function send(e){' +
'  e.preventDefault();' +
'  var btn=document.getElementById("btnSend"),msg=document.getElementById("msg");' +
'  btn.disabled=true;btn.textContent="جاري الإرسال...";msg.className="msg";' +
'  google.script.run.withSuccessHandler(function(){' +
'    msg.textContent="✅ تم إرسال بياناتك بنجاح، شكراً لك";msg.className="msg ok";' +
'    document.getElementById("f").reset();' +
'    document.getElementById("lat").value="";document.getElementById("lng").value="";' +
'    var s=document.getElementById("locStatus");s.textContent="لم يتم تحديد الموقع";s.className="loc-status";' +
'    btn.disabled=false;btn.textContent="إرسال البيانات";' +
'  }).withFailureHandler(function(){' +
'    msg.textContent="❌ حدث خطأ أثناء الإرسال، حاول مرة أخرى";msg.className="msg err";' +
'    btn.disabled=false;btn.textContent="إرسال البيانات";' +
'  }).saveData({' +
'    fullName:document.getElementById("fullName").value.trim(),' +
'    phone:document.getElementById("phone").value.trim(),' +
'    address:document.getElementById("address").value.trim(),' +
'    lat:document.getElementById("lat").value,' +
'    lng:document.getElementById("lng").value' +
'  });' +
'  return false;' +
'}' +
'</scr'+'ipt></body></html>';
