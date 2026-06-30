from server import app
import webview
import threading
import time
import requests

def run_flask():
    app.run(port=5099, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 等服务器就绪再打开窗口
    for _ in range(30):
        try:
            r = requests.get("http://127.0.0.1:5099/", timeout=1)
            if r.status_code == 200:
                break
        except:
            pass
        time.sleep(0.2)

    webview.create_window("Yuanne", "http://127.0.0.1:5099/?v=5", width=420, height=700)
    webview.start()
