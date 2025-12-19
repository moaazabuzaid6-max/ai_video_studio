# AI Video Studio Pro (PyQt5)

## تشغيل التطبيق

1. تأكد من تثبيت Python 3.10.11
2. ثبّت الحزم:
   ```
   pip install PyQt5 yt-dlp moviepy numpy
   ```
3. شغّل التطبيق:
   ```
   python ai_video_studio_app.py
   ```

---

## تحويل التطبيق إلى ملف EXE (تشغيل مباشر)

1. ثبّت PyInstaller:
   ```
   pip install pyinstaller
   ```
2. أنشئ الملف التنفيذي:
   ```
   pyinstaller --onefile --noconsole ai_video_studio_app.py
   ```
3. ستجد الملف التنفيذي في مجلد dist/run_app.exe
4. شغّل run_app.exe وسيتم فتح التطبيق كبرنامج مستقل.

> **ملاحظة:** يجب أن تكون جميع المجلدات (videos/input, videos/output, audio_library, إلخ) في نفس المجلد مع run_app.exe أو استخدم --add-data مع PyInstaller لنقل الملفات.
