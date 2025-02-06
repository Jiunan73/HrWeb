from flask import Flask, send_file
import cv2
from io import BytesIO
import os
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# 設定照片保存的目錄
SAVE_DIR = "captured_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# IP 攝像頭 URL
ip_camera_url = "http://admin:123456@192.168.2.151/snapshot.JPG"  # 替換為您的 IP 攝像頭 URL
def capture_images():
    while True:
        # 獲取當前時間
        now = datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%S") + ".jpg"
        file_path = os.path.join(SAVE_DIR, file_name)

        # 使用 OpenCV 從 IP 攝像頭獲取照片
        cap = cv2.VideoCapture(ip_camera_url)
        ret, frame = cap.read()
        cap.release()

        if ret:
            # 保存照片到本地磁碟
            cv2.imwrite(file_path, frame)

        # 刪除七天前相同時分秒的照片
        delete_old_images(now)

        # 每秒抓取一張照片
        time.sleep(1)

def delete_old_images(now):
    cutoff = now - timedelta(days=7)
    file_name = cutoff.strftime("%Y%m%d%H%M%S") + ".jpg"
    file_path = os.path.join(SAVE_DIR, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/capture')
def capture():
    # 使用 OpenCV 從 IP 攝像頭獲取照片
    cap = cv2.VideoCapture(ip_camera_url)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "Failed to capture image", 500

    # 將照片保存到內存中
    # 壓縮照片
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  # 壓縮質量設置為50
    is_success, buffer = cv2.imencode(".jpg", frame, encode_param)
    img = BytesIO(buffer)


    return send_file(img, mimetype='image/jpeg')

if __name__ == '__main__':
    # 啟動照片抓取執行緒
    #capture_thread = threading.Thread(target=capture_images)
    #capture_thread.daemon = True
    #capture_thread.start()

    app.run(debug=True, port=8000)
