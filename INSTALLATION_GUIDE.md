# دليل التثبيت الشامل - مساعد Windows Server الذكي

## متطلبات النظام

### الحد الأدنى للمتطلبات:
- **نظام التشغيل**: Windows Server 2016+ أو Windows 10/11
- **المعالج**: Intel/AMD 64-bit
- **الذاكرة**: 8 GB RAM (16 GB مُوصى به)
- **مساحة القرص**: 10 GB مساحة فارغة
- **الشبكة**: اتصال إنترنت للتحميل والتثبيت

### البرامج المطلوبة:
- **Python 3.8+**
- **Node.js 14+**
- **Git**
- **Docker Desktop** (اختياري)

## طرق التثبيت

### الطريقة الأولى: التثبيت التلقائي (مُوصى به)

#### 1. تشغيل سكربت PowerShell
```powershell
# تشغيل PowerShell كمدير
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

#### 2. تشغيل سكربت Batch
```cmd
# تشغيل Command Prompt كمدير
setup.bat
```

### الطريقة الثانية: التثبيت اليدوي

#### الخطوة 1: تثبيت Chocolatey
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### الخطوة 2: تثبيت البرامج الأساسية
```cmd
choco install python -y
choco install nodejs-lts -y
choco install git -y
choco install docker-desktop -y
```

#### الخطوة 3: تثبيت أدوات الأمان
```cmd
choco install zap -y
choco install burp-suite-free-edition -y
pip install sqlmap
```

#### الخطوة 4: تثبيت متطلبات Python
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

#### الخطوة 5: تثبيت متطلبات Frontend
```cmd
cd frontend
npm install
cd ..
```

## إعداد المتغيرات البيئية

### إنشاء ملف .env
```env
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key
AZURE_SPEECH_KEY=your-azure-speech-key
AZURE_SPEECH_REGION=your-azure-region
DATABASE_URL=sqlite:///./app.db
CORS_ORIGINS=http://localhost:3000
```

### الحصول على مفاتيح API

#### OpenAI API Key
1. اذهب إلى [OpenAI Platform](https://platform.openai.com/)
2. سجل الدخول أو أنشئ حساب جديد
3. اذهب إلى API Keys
4. أنشئ مفتاح جديد وانسخه

#### Azure Speech Services
1. اذهب إلى [Azure Portal](https://portal.azure.com/)
2. أنشئ حساب Azure (يوجد نسخة مجانية)
3. أنشئ Speech Service resource
4. احصل على المفتاح والمنطقة

## تشغيل التطبيق

### تشغيل Backend
```cmd
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### تشغيل Frontend (في terminal منفصل)
```cmd
cd frontend
npm start
```

### الوصول للتطبيق
- **API Documentation**: http://localhost:8000/docs
- **Frontend Interface**: http://localhost:3000
- **ReDoc Documentation**: http://localhost:8000/redoc

## بيانات تسجيل الدخول الافتراضية

### حساب المدير
- **اسم المستخدم**: `admin`
- **كلمة المرور**: `admin123`
- **الصلاحيات**: كاملة

### حساب المستخدم
- **اسم المستخدم**: `user`
- **كلمة المرور**: `user123`
- **الصلاحيات**: قراءة فقط

## اختبار التثبيت

### اختبار Backend API
```cmd
curl -X POST "http://localhost:8000/auth/token" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "grant_type=password&username=admin&password=admin123"
```

### اختبار معلومات النظام
```cmd
curl -X GET "http://localhost:8000/system/info" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## حل المشاكل الشائعة

### مشكلة: Python غير موجود
**الحل**:
```cmd
choco install python -y
refreshenv
```

### مشكلة: pip غير موجود
**الحل**:
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### مشكلة: Node.js غير موجود
**الحل**:
```cmd
choco install nodejs-lts -y
refreshenv
```

### مشكلة: صلاحيات PowerShell
**الحل**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### مشكلة: Docker لا يعمل
**الحل**:
1. تأكد من تشغيل Docker Desktop
2. أعد تشغيل النظام بعد التثبيت
3. تأكد من تفعيل Virtualization في BIOS

### مشكلة: منافذ مشغولة
**الحل**:
```cmd
# للتحقق من المنافذ المستخدمة
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# لإيقاف العملية
taskkill /PID <PID_NUMBER> /F
```

## الأمان والحماية

### تغيير كلمات المرور الافتراضية
1. افتح `backend/app/dependencies.py`
2. غيّر كلمات المرور في `fake_users_db`
3. أعد تشغيل الخادم

### تحديث SECRET_KEY
```env
SECRET_KEY=your-new-super-secret-key-minimum-32-characters
```

### تفعيل HTTPS (للإنتاج)
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
```

## النشر على الخادم

### إعداد Windows Server
1. فتح منافذ الجدار النار:
```cmd
netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="React" dir=in action=allow protocol=TCP localport=3000
```

2. إعداد خدمة Windows:
```cmd
# إنشاء خدمة للتشغيل التلقائي
sc create "WindowsServerAssistant" binPath="C:\path\to\your\start.bat"
sc config "WindowsServerAssistant" start=auto
```

### إعداد Reverse Proxy (IIS)
1. تثبيت IIS و URL Rewrite Module
2. إعداد Application Request Routing
3. إنشاء قواعد إعادة التوجيه

## المراقبة والسجلات

### مواقع ملفات السجلات
- **Backend Logs**: `backend/logs/`
- **System Logs**: Windows Event Viewer
- **Application Logs**: Console output

### مراقبة الأداء
```cmd
# مراقبة استخدام الذاكرة
tasklist /fi "imagename eq python.exe"

# مراقبة استخدام المعالج
wmic process where name="python.exe" get processid,percentprocessortime
```

## التحديث والصيانة

### تحديث Python Dependencies
```cmd
pip install --upgrade -r requirements.txt
```

### تحديث Frontend Dependencies
```cmd
cd frontend
npm update
```

### نسخ احتياطي للبيانات
```cmd
# نسخ قاعدة البيانات
copy backend\app.db backup\app_backup_%date%.db

# نسخ ملفات الإعداد
copy .env backup\.env_backup_%date%
```

## الدعم والمساعدة

### الموارد المفيدة
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://reactjs.org/docs/
- **Python Documentation**: https://docs.python.org/3/

### التواصل للدعم
- راجع ملف `PROJECT_PROFILE.md` للتفاصيل الكاملة
- تحقق من السجلات للأخطاء
- استخدم GitHub Issues للإبلاغ عن المشاكل

---

**ملاحظة مهمة**: تأكد من تحديث جميع كلمات المرور والمفاتيح السرية قبل النشر في بيئة الإنتاج.
