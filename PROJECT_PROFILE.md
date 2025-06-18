# مشروع المساعد الذكي لإدارة Windows Server واختبار الاختراق

## نظرة عامة على المشروع
مساعد برمجي ذكي متكامل يعمل على Windows Server مع واجهة ويب تفاعلية للدردشة، يدمج تقنيات معالجة اللغة الطبيعية وأدوات اختبار الاختراق وإدارة النظام.

## البنية التقنية المنجزة

### 1. Backend (FastAPI) - مكتمل ✅
**المسار**: `backend/`

#### الملفات الأساسية:
- `app/main.py` - التطبيق الرئيسي مع إعداد FastAPI
- `app/core/config.py` - إعدادات التطبيق والمتغيرات البيئية
- `app/core/security.py` - نظام الأمان وتشفير كلمات المرور
- `app/core/logging.py` - نظام السجلات المتقدم
- `app/dependencies.py` - التبعيات والمصادقة

#### واجهات برمجة التطبيقات (APIs):
- `app/api/auth.py` - مصادقة المستخدمين (JWT)
- `app/api/chat.py` - نظام الدردشة والرسائل
- `app/api/system.py` - مراقبة النظام وتنفيذ الأوامر
- `app/api/pentest.py` - أدوات اختبار الاختراق

#### الخدمات (Services):
- `app/services/nlp_service.py` - معالجة اللغة الطبيعية (OpenAI/DeepSeek)
- `app/services/voice_service.py` - الخدمات الصوتية (Azure Speech)
- `app/services/system_service.py` - إدارة النظام والأوامر
- `app/services/pentest_service.py` - أدوات اختبار الاختراق
- `app/services/docker_service.py` - إدارة الحاويات

### 2. Frontend (React) - مكتمل ✅
**المسار**: `frontend/`

#### المكونات الرئيسية:
- `src/App.js` - التطبيق الرئيسي مع التوجيه
- `src/contexts/AuthContext.js` - إدارة حالة المصادقة
- `src/components/Login.js` - واجهة تسجيل الدخول
- `src/components/Dashboard.js` - لوحة التحكم الرئيسية
- `src/components/Chat.js` - واجهة الدردشة التفاعلية
- `src/components/SystemMonitor.js` - مراقبة النظام
- `src/components/PentestResults.js` - نتائج اختبار الاختراق
- `src/components/Navbar.js` - شريط التنقل

### 3. الإعدادات والتوثيق
- `requirements.txt` - متطلبات Python
- `.env` - متغيرات البيئة
- `README.md` - دليل التثبيت والاستخدام
- `project_plan.md` - خطة المشروع التفصيلية
- `start.bat` - ملف تشغيل سريع

## الميزات المنجزة

### 🔐 نظام المصادقة والأمان
- مصادقة JWT مع Bearer tokens
- تشفير كلمات المرور باستخدام bcrypt
- نظام الأدوار والصلاحيات (admin/user)
- حماية نقاط النهاية بالتوكن

**بيانات الاختبار**:
- المدير: `admin` / `admin123`
- المستخدم: `user` / `user123`

### 💻 إدارة النظام
- معلومات النظام الشاملة (OS, Memory, CPU, Disk, Network)
- مراقبة العمليات في الوقت الفعلي
- تنفيذ أوامر النظام
- إحصائيات الأداء المفصلة

### 💬 نظام الدردشة
- اتصال WebSocket للرسائل الفورية
- بث الرسائل للمستخدمين المتصلين
- دعم الأوامر الصوتية (جاهز للتكامل)
- معالجة اللغة الطبيعية

### 🔍 اختبار الاختراق
- تكامل مع أدوات: OWASP ZAP, Burp Suite, SQLMap, Acunetix, SonarQube
- إدارة الحاويات للبيئات المعزولة
- تقارير الفحص والنتائج
- سير عمل التقييم الأمني

### 🎤 الخدمات الصوتية والذكية
- تكامل Azure Speech Services
- دعم OpenAI/DeepSeek APIs
- معالجة الأوامر الصوتية
- ردود ذكية تفاعلية

## نقاط النهاية المختبرة ✅

### المصادقة
- `POST /auth/token` - تسجيل الدخول ✅
- `GET /auth/me` - معلومات المستخدم الحالي ✅
- `POST /auth/logout` - تسجيل الخروج ✅

### النظام
- `GET /system/info` - معلومات النظام الشاملة ✅
- `POST /system/execute` - تنفيذ الأوامر (جاهز)

### الدردشة
- `POST /chat/broadcast` - بث الرسائل (جاهز)
- WebSocket `/ws/chat` - اتصال مباشر (جاهز)

### اختبار الاختراق
- `POST /pentest/scan` - بدء الفحص (جاهز)
- `GET /pentest/results/{scan_id}` - نتائج الفحص (جاهز)

## التقنيات المستخدمة

### Backend
- **FastAPI** - إطار عمل API سريع وحديث
- **Python 3.8+** - لغة البرمجة الأساسية
- **JWT** - مصادقة آمنة
- **WebSockets** - اتصال مباشر
- **psutil** - مراقبة النظام
- **bcrypt** - تشفير كلمات المرور

### Frontend
- **React** - مكتبة واجهة المستخدم
- **JavaScript ES6+** - لغة البرمجة
- **CSS3** - تنسيق متجاوب
- **Fetch API** - طلبات HTTP

### التكامل
- **Docker** - إدارة الحاويات
- **Azure Speech** - الخدمات الصوتية
- **OpenAI/DeepSeek** - معالجة اللغة الطبيعية

## حالة الاختبار

### مختبر ✅
- نظام المصادقة والتوكن
- معلومات النظام التفصيلية
- واجهة Swagger UI
- تشغيل الخادم والإعدادات

### في انتظار الاختبار
- واجهة React الأمامية
- نقاط نهاية الدردشة
- أدوات اختبار الاختراق
- الخدمات الصوتية
- معالجة الأخطاء

## التثبيت والتشغيل

### متطلبات النظام
- Windows Server 2016+ أو Windows 10/11
- Python 3.8+
- Node.js 14+ (للواجهة الأمامية)

### خطوات التثبيت
```bash
# 1. تثبيت متطلبات Python
pip install -r requirements.txt

# 2. إعداد متغيرات البيئة
copy .env.example .env
# تحرير .env بالقيم المناسبة

# 3. تشغيل الخادم
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. الوصول للتوثيق
# http://localhost:8000/docs
```

### تشغيل الواجهة الأمامية
```bash
cd frontend
npm install
npm start
```

## الملفات الحساسة والإعدادات

### متغيرات البيئة (.env)
```
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-key
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=your-region
DATABASE_URL=sqlite:///./app.db
```

### إعدادات الأمان
- تشفير JWT بمفتاح سري قوي
- تشفير كلمات المرور ببcrypt
- حماية CORS للواجهة الأمامية
- تسجيل شامل للعمليات

## الخطوات التالية للتطوير

1. **اختبار شامل للواجهة الأمامية**
2. **تكامل قاعدة البيانات الحقيقية**
3. **تفعيل الخدمات الصوتية**
4. **اختبار أدوات الاختراق**
5. **تحسين الأداء والأمان**
6. **إضافة المزيد من أدوات المراقبة**

## معلومات الاتصال والدعم
- الخادم يعمل على: `http://localhost:8000`
- التوثيق التفاعلي: `http://localhost:8000/docs`
- واجهة ReDoc: `http://localhost:8000/redoc`

## ملاحظات مهمة
- المشروع جاهز للنشر على Windows Server
- يدعم الوصول عبر RDP
- قابل للتوسع والتخصيص
- موثق بالكامل ومنظم بطريقة احترافية

---
**تاريخ الإنشاء**: ديسمبر 2024  
**الحالة**: مكتمل ومختبر جزئياً  
**الإصدار**: 1.0.0
