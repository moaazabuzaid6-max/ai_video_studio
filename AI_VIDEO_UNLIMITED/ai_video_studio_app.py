import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import os
import threading

PASSWORD = "mySuperStrongPassword2025"

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("تسجيل الدخول - AI Video Studio Pro")
        self.setGeometry(600, 300, 350, 150)
        layout = QVBoxLayout()
        self.label = QLabel("أدخل كلمة المرور:")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)
        self.button = QPushButton("دخول")
        self.button.clicked.connect(self.check_password)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        self.setLayout(layout)
    def check_password(self):
        if self.input.text() == PASSWORD:
            self.on_success()
            self.close()
        else:
            QMessageBox.critical(self, "خطأ", "كلمة المرور غير صحيحة!")

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 AI Video Studio Pro")
        self.setGeometry(400, 100, 600, 400)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.info = QLabel("منصة المونتاج الذكي غير المحدود!\nارفع فيديو، أضف مؤثرات، وحمّل النتيجة فوراً.")
        self.info.setAlignment(Qt.AlignCenter)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("أدخل رابط الفيديو أو الصوت (يوتيوب ...)")
        self.download_video_btn = QPushButton("تنزيل فيديو")
        self.download_audio_btn = QPushButton("تنزيل صوت فقط")
        self.download_video_btn.clicked.connect(self.download_video)
        self.download_audio_btn.clicked.connect(self.download_audio)
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        # مونتاج تلقائي
        self.yt_montage_url = QLineEdit()
        self.yt_montage_url.setPlaceholderText("رابط فيديو يوتيوب (لنسخ المونتاج)")
        self.user_video_btn = QPushButton("اختر فيديوك لتطبيق المونتاج")
        self.user_video_btn.clicked.connect(self.select_user_video)
        self.user_video_path = None
        self.montage_btn = QPushButton("نفذ مونتاج احترافي تلقائي")
        self.montage_btn.clicked.connect(self.run_montage)
        # ترتيب العناصر
        layout.addWidget(self.info)
        layout.addWidget(self.url_input)
        h1 = QHBoxLayout()
        h1.addWidget(self.download_video_btn)
        h1.addWidget(self.download_audio_btn)
        layout.addLayout(h1)
        layout.addWidget(self.status)
        layout.addWidget(QLabel("--- مونتاج احترافي تلقائي ---"))
        layout.addWidget(self.yt_montage_url)
        layout.addWidget(self.user_video_btn)
        layout.addWidget(self.montage_btn)
        self.setLayout(layout)
    def log(self, msg):
        self.status.append(msg)
    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.log("يرجى إدخال رابط!")
            return
        self.log("جاري تنزيل الفيديو ...")
        threading.Thread(target=self._download, args=(url, True)).start()
    def download_audio(self):
        url = self.url_input.text().strip()
        if not url:
            self.log("يرجى إدخال رابط!")
            return
        self.log("جاري تنزيل الصوت ...")
        threading.Thread(target=self._download, args=(url, False)).start()
    def _download(self, url, is_video):
        try:
            import yt_dlp as youtube_dlp
            ydl_opts = {
                'outtmpl': 'videos/input/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best' if is_video else 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
            }
            with youtube_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            self.log(f"تم التنزيل: {info.get('title', 'ملف')}")
        except Exception as e:
            self.log(f"خطأ أثناء التنزيل: {e}")
    def select_user_video(self):
        fname, _ = QFileDialog.getOpenFileName(self, "اختر فيديوك", "", "Video Files (*.mp4 *.mov *.avi)")
        if fname:
            self.user_video_path = fname
            self.log(f"تم اختيار الفيديو: {fname}")
    def run_montage(self):
        yt_url = self.yt_montage_url.text().strip()
        if not yt_url or not self.user_video_path:
            self.log("يرجى إدخال رابط يوتيوب واختيار فيديو!")
            return
        self.log("جاري تنفيذ المونتاج ...")
        threading.Thread(target=self._montage, args=(yt_url, self.user_video_path)).start()
    def _montage(self, yt_url, user_video_path):
        try:
            import yt_dlp as youtube_dlp
            import moviepy.editor as mp
            import tempfile
            import numpy as np
            from datetime import datetime
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {'outtmpl': f'{tmpdir}/yt_source.%(ext)s', 'format': 'bestvideo+bestaudio/best', 'quiet': True}
                with youtube_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(yt_url, download=True)
                    yt_path = ydl.prepare_filename(info)
                yt_clip = mp.VideoFileClip(yt_path)
                audio = yt_clip.audio.to_soundarray(fps=22050)
                volume = np.abs(audio).mean(axis=1)
                threshold = np.percentile(volume, 60)
                is_speech = volume > threshold
                cuts = []
                start = None
                for i, val in enumerate(is_speech):
                    if val and start is None:
                        start = i
                    elif not val and start is not None:
                        end = i
                        cuts.append((start/22050, end/22050))
                        start = None
                if start is not None:
                    cuts.append((start/22050, len(is_speech)/22050))
                user_clip = mp.VideoFileClip(user_video_path)
                montage = mp.concatenate_videoclips([
                    user_clip.subclip(max(0, s), min(user_clip.duration, e)) for s, e in cuts if e-s > 0.5
                ])
                out_path = os.path.join("videos/output", f"montage_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4")
                montage.write_videofile(out_path)
            self.log(f"تم تنفيذ المونتاج! النتيجة في: {out_path}")
        except Exception as e:
            self.log(f"خطأ أثناء المونتاج: {e}")

def main():
    app = QApplication(sys.argv)
    def show_main():
        main_win = MainApp()
        main_win.show()
        app.exec_()
    login = LoginWindow(on_success=show_main)
    login.show()
    app.exec_()

if __name__ == "__main__":
    main()
