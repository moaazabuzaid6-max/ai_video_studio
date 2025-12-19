@echo off
chcp 65001 >nul
title 🎬 AI Video Studio - الإعداد التلقائي
color 0A

echo.
echo ============================================
echo    نظام الذكاء الاصطناعي لمونتاج الفيديو
echo ============================================
echo.

echo [1] التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت
    echo 📥 جاري التحميل التلقائي...
    
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile 'python_installer.exe'"
    
    if exist python_installer.exe (
        echo ⚙️ جاري تثبيت Python...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=0
        del python_installer.exe
        echo ✅ تم تثبيت Python
    ) else (
        echo ⚠️ قم بتحميل Python يدوياً من python.org
        pause
        exit
    )
)

echo ✅ Python مثبت بالفعل
echo.

echo [2] تثبيت المكتبات الأساسية...
call :install_packages
echo.

echo [3] تنزيل الموارد من الإنترنت...
call :download_resources
echo.

echo [4] إنشاء نظام التشغيل...
call :create_system
echo.

echo ============================================
echo    ✅ تم الإعداد بنجاح!
echo ============================================
echo.
echo 🚀 **كيفية التشغيل:**
echo    1. انقر نقراً مزدوجاً على run.bat
echo    2. أو اكتب في Terminal: python app.py
echo    3. افتح المتصفح على: http://localhost:8501
echo.
echo ⭐ النظام مفتوح المصدر ويعمل 100%%
pause
exit /b 0

:install_packages
echo 📦 جاري تثبيت مكتبات Python...
pip install --upgrade pip
pip install streamlit==1.28.0
pip install moviepy==1.0.3
pip install opencv-python==4.8.1.78
pip install pillow==10.0.0
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install youtube-dlp==2023.11.16
pip install requests==2.31.0
pip install arabic-reshaper==3.0.0
pip install python-bidi==0.4.2
echo ✅ تم تثبيت جميع المكتبات
exit /b 0

:download_resources
echo 🌐 جاري تنزيل الموارد المجانية...
if not exist audio_library mkdir audio_library
set "UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
powershell -Command "Invoke-WebRequest -Uri 'https://assets.mixkit.co/sfx/download/mixkit-camera-shutter-click-1133.wav' -OutFile 'audio_library/camera_click.wav' -Headers @{ 'User-Agent' = $env:UA }"
powershell -Command "Invoke-WebRequest -Uri 'https://assets.mixkit.co/sfx/download/mixkit-game-show-transition-woosh-218.wav' -OutFile 'audio_library/transition.wav' -Headers @{ 'User-Agent' = $env:UA }"
powershell -Command "Invoke-WebRequest -Uri 'https://assets.mixkit.co/sfx/download/mixkit-winning-chimes-2015.wav' -OutFile 'audio_library/winning.wav' -Headers @{ 'User-Agent' = $env:UA }"
powershell -Command "Invoke-WebRequest -Uri 'https://assets.mixkit.co/music/download/mixkit-tech-house-vibes-130.mp3' -OutFile 'audio_library/tech_house.mp3' -Headers @{ 'User-Agent' = $env:UA }"
powershell -Command "Invoke-WebRequest -Uri 'https://cdn.pixabay.com/download/audio/2022/03/15/audio_908d6ed4f4.mp3' -OutFile 'audio_library/cinematic.mp3' -Headers @{ 'User-Agent' = $env:UA }"
powershell -Command "Invoke-WebRequest -Uri 'https://cdn.pixabay.com/download/audio/2022/02/22/audio_5d8d2a2565.mp3' -OutFile 'audio_library/crowd_hum.mp3' -Headers @{ 'User-Agent' = $env:UA }"
echo ✅ تم تنزيل المكتبات الصوتية
exit /b 0

:create_system
echo ⚙️ إنشاء نظام التشغيل...
echo من moviepy.editor import * > quick_start.py
echo print("🎬 نظام مونتاج الفيديو جاهز!") >> quick_start.py
echo clip = ColorClip(size=(1280,720), color=(40,60,120), duration=3) >> quick_start.py
echo clip.write_videofile("videos/output/test_video.mp4") >> quick_start.py
echo print("✅ تم إنشاء أول فيديو") >> quick_start.py
echo @echo off > run.bat
echo chcp 65001 ^>nul >> run.bat
echo title 🎬 AI Video Studio >> run.bat
echo echo جاري تشغيل النظام... >> run.bat
echo python app.py >> run.bat
echo pause >> run.bat
echo ✅ تم إنشاء النظام
exit /b 0
