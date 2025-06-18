# دليل التوافق مع Windows Server 2019 Standard

## نظرة عامة
تم تحديث مشروع المساعد الذكي ليكون متوافقاً بالكامل مع Windows Server 2019 Standard (Build 17763).

## التحديثات المطبقة للتوافق

### 1. إصدارات البرامج المحددة
```
- Python: 3.8.10 (متوافق مع Server 2019)
- Node.js: 14.21.3 LTS (مستقر على Server 2019)
- Git: 2.35.1 (آخر إصدار مدعوم)
- OWASP ZAP: 2.11.1 (متوافق مع Server 2019)
- SQLMap: 1.5.12 (إصدار مستقر)
```

### 2. مكتبات Python المحدثة
```
fastapi==0.68.2          # إصدار مستقر
uvicorn==0.15.0          # متوافق مع Server 2019
psutil==5.8.0            # مراقبة النظام
wmi==1.5.1               # إدارة Windows
pywin32==303             # Windows APIs
pyodbc==4.0.32           # SQL Server connectivity
winrm==0.4.1             # إدارة عن بُعد
```

### 3. ميزات Windows Server المضافة
- **IIS Web Server**: تثبيت تلقائي
- **NET Framework 4.5**: دعم كامل
- **Windows Management**: WMI و WinRM
- **Long Path Support**: تفعيل المسارات الطويلة
- **TLS 1.2**: تفعيل للأمان

## متطلبات النظام المحدثة

### الحد الأدنى:
- **OS**: Windows Server 2019 Standard (Build 17763)
- **RAM**: 8 GB (16 GB مُوصى به)
- **Storage**: 20 GB مساحة فارغة
- **Network**: اتصال إنترنت مستقر

### الأدوار والميزات المطلوبة:
```powershell
# تثبيت الأدوار الأساسية
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
Install-WindowsFeature -Name NET-Framework-45-Features
Install-WindowsFeature -Name PowerShell-ISE
```

## إعدادات الأمان المحسنة

### 1. إعدادات الجدار النار
```cmd
# فتح المنافذ المطلوبة
netsh advfirewall firewall add rule name="FastAPI Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="React Frontend" dir=in action=allow protocol=TCP localport=3000
```

### 2. إعدادات PowerShell
```powershell
# تفعيل تنفيذ السكريبتات
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# تفعيل المسارات الطويلة
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
```

### 3. إعدادات TLS
```powershell
# تفعيل TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

## أدوات الأمان المتوافقة

### 1. OWASP ZAP 2.11.1
- متوافق بالكامل مع Server 2019
- يدعم Java 8+ المثبت مع النظام
- واجهة GUI و API متاحة

### 2. SQLMap 1.5.12
- إصدار Python مستقر
- يعمل مع Python 3.8.10
- دعم قواعد البيانات المتعددة

### 3. أدوات Windows الأصلية
```cmd
# أدوات مراقبة النظام
wmic process list
wmic service list
netstat -an
tasklist /svc
```

## التثبيت المحسن

### 1. تشغيل سكريبت التثبيت
```cmd
# كمدير نظام
setup.bat
```

أو

```powershell
# PowerShell كمدير
.\setup.ps1
```

### 2. التحقق من التثبيت
```cmd
# فحص Python
python --version

# فحص Node.js
node --version

# فحص Git
git --version

# فحص المكتبات
pip list | findstr fastapi
```

## إعدادات الإنتاج

### 1. خدمة Windows
```cmd
# إنشاء خدمة للتشغيل التلقائي
sc create "WindowsServerAssistant" binPath="C:\path\to\start.bat" start=auto
sc description "WindowsServerAssistant" "AI Assistant for Windows Server Management"
```

### 2. إعداد IIS Reverse Proxy
```xml
<!-- web.config for IIS -->
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="API Proxy" stopProcessing="true">
          <match url="api/(.*)" />
          <action type="Rewrite" url="http://localhost:8000/api/{R:1}" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

### 3. إعدادات SSL/HTTPS
```cmd
# إنشاء شهادة SSL للتطوير
powershell -Command "New-SelfSignedCertificate -DnsName localhost -CertStoreLocation cert:\LocalMachine\My"
```

## مراقبة الأداء

### 1. Performance Counters
```powershell
# مراقبة استخدام المعالج
Get-Counter "\Processor(_Total)\% Processor Time"

# مراقبة الذاكرة
Get-Counter "\Memory\Available MBytes"

# مراقبة الشبكة
Get-Counter "\Network Interface(*)\Bytes Total/sec"
```

### 2. Event Logs
```powershell
# فحص سجلات التطبيق
Get-EventLog -LogName Application -Newest 50

# فحص سجلات النظام
Get-EventLog -LogName System -Newest 50
```

## استكشاف الأخطاء وإصلاحها

### 1. مشاكل Python شائعة
```cmd
# إعادة تثبيت pip
python -m ensurepip --upgrade

# تحديث setuptools
pip install --upgrade setuptools

# حل مشاكل SSL
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package>
```

### 2. مشاكل Node.js
```cmd
# تنظيف cache
npm cache clean --force

# إعادة تثبيت node_modules
rmdir /s node_modules
npm install --legacy-peer-deps
```

### 3. مشاكل الشبكة
```cmd
# فحص المنافذ
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# فحص DNS
nslookup google.com
```

## النسخ الاحتياطي والاستعادة

### 1. نسخ احتياطي للبيانات
```cmd
# نسخ قاعدة البيانات
xcopy backend\*.db backup\ /Y

# نسخ ملفات الإعداد
xcopy .env backup\ /Y
xcopy *.json backup\ /Y
```

### 2. نسخ احتياطي للنظام
```powershell
# إنشاء نقطة استعادة
Checkpoint-Computer -Description "Before AI Assistant Installation"
```

## الصيانة الدورية

### 1. تحديث المكتبات
```cmd
# تحديث Python packages
pip list --outdated
pip install --upgrade package_name

# تحديث Node.js packages
npm outdated
npm update
```

### 2. تنظيف النظام
```cmd
# تنظيف ملفات مؤقتة
del /q /s %temp%\*

# تنظيف logs قديمة
forfiles /p backend\logs /s /m *.log /d -30 /c "cmd /c del @path"
```

## الدعم والمساعدة

### موارد مفيدة:
- **Microsoft Docs**: https://docs.microsoft.com/en-us/windows-server/
- **Python on Windows**: https://docs.python.org/3/using/windows.html
- **Node.js on Windows**: https://nodejs.org/en/docs/guides/nodejs-docker-webapp/

### سجلات الأخطاء:
- **Application Logs**: `backend/logs/`
- **Windows Event Viewer**: `eventvwr.msc`
- **IIS Logs**: `C:\inetpub\logs\LogFiles\`

---

**ملاحظة**: تم اختبار جميع المكونات على Windows Server 2019 Standard Build 17763 وتعمل بشكل مثالي.
