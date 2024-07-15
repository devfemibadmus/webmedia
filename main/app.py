from flask import Flask, render_template, request, jsonify, session
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
from datetime import datetime
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'a5f4b6e9c7d1a8b2e0f3c9d2a8b1f4e5'
application = app

class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client.from_service_account_json(os.path.join(BASE_DIR, "mediasaver.json"))
        self.bucket = self.storage_client.bucket('mediasaver')

    def upload_file(self, file_folder, file_upload):
        if file_upload:
            blob = self.bucket.blob(file_folder + "/" + file_upload.filename)
            blob.upload_from_file(file_upload)
            signed_url = blob.generate_signed_url(expiration=1200, version='v4')
            return signed_url
        return False

    def get_signed_url(self, file_folder, file_name, expiration=1200):
        if file_name:
            blob = self.bucket.blob(file_folder + "/" + file_name)
            signed_url = blob.generate_signed_url(expiration=expiration, version='v4')
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
    if request.method == 'POST' and request.form.get('video_url'):
        video_url = request.form.get('video_url')
        scraper = Scraper()
        response = scraper.get_video(file_folder, video_url)
        return jsonify(response)
    return render_template("home.html")

@app.route('/upload-video', methods=['POST'])
@cross_origin()
def upload_video():
    if 'file' not in request.files:
        session['error'] = "No file part"

    file = request.files['file']
    
    if file.filename == '':
        session['error'] = "No selected file"

    file_folder = request.form.get('file_folder')
    
    video_url = manager.upload_file(file_folder, file)
    
    return jsonify({"message": "Video uploaded successfully!", "video_url": video_url})

@app.route('/get-video-url/', methods=['POST'])
def get_video_url():
    file_name = request.form.get('file_name')
    file_folder = request.form.get('file_folder')
    return jsonify({"video_url": manager.get_signed_url(file_folder, file_name)})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
