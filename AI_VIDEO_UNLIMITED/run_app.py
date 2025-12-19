import subprocess
import webbrowser
import time
import threading

# شغّل streamlit في الخلفية

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "app.py", "--server.headless=true"])

# افتح المتصفح بعد ثوانٍ قليلة

def open_browser():
    time.sleep(2)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    threading.Thread(target=run_streamlit).start()
    open_browser()
