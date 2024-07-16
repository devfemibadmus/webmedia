from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
from datetime import datetime
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')
application = app

class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, "mediasaver.json"))
        self.bucket = self.storage_client.bucket('mediasaver')

    def upload_file(self, file_folder, file_upload):
        if file_upload:
            blob = self.bucket.blob(file_folder + "/" + file_upload.filename)
            blob.upload_from_file(file_upload)
            signed_url = blob.generate_signed_url(expiration=3600, version='v4')
            return signed_url
        return False

    def get_signed_url(self, file_folder, file_name):
        if file_name:
            blob = self.bucket.blob(file_folder + "/" + file_name)
            signed_url = blob.generate_signed_url(expiration=3600, version='v4')
            print("signed_url: ", signed_url)
            return signed_url
        return False

    def delete_file(self, file_folder, file_name):
        if file_name:
            blob = self.bucket.blob(file_folder + "/" + file_name)
            blob.delete()
            return True
        return False

manager = CloudStorageManager()

@app.route('/app/', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def home():
    now = datetime.now()
    date = now.strftime("%m-%d-%Y")
    time = now.strftime("%H:%M:%S")
    file_folder = f"{date}/{time}"
    if request.method == 'POST' and request.form.get('src'):
        src = request.form.get('src')
        scraper = Scraper()
        response = scraper.get_video(file_folder, src)
        print(response)
        return jsonify(response)
    return render_template("home.html")

@app.route('/upload-video', methods=['POST'])
@cross_origin()
def upload_video():
    if 'file' not in request.files:
        return jsonify({"message": "No file part", "error": True})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file", "error": True})

    file_folder = request.form.get('file_folder')
    
    data = [{"src": manager.upload_file(file_folder, file)}]
    
    return jsonify({"message": "Video uploaded successfully!", "success": True, "data": data})

@app.route('/test-mode/', methods=['POST'])
def get_test_url():
    src = [{"src": "static/0713.mp4"}, {"src": "static/0713.mp4"}, {"src": "static/icon-512.png"}]
    return jsonify({"data": src})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
