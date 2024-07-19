from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
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
scraper = Scraper()

@app.route('/app/', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST' and request.form.get('src'):
        src = request.form.get('src')
        response = scraper.getMedia(src)
        print(response)
        return jsonify(response)
    return render_template("home.html")

@app.route('/uploadMedia', methods=['POST'])
@cross_origin()
def upload_video():
    print("request.files: ", request.files)
    if 'video_0' not in request.files and 'image_0' not in request.files:
        return jsonify({"message": "No media found!", "error": True})

    file_folder = request.form.get('file_folder')
    print("file_folder: ", file_folder)
    data = []

    for key in request.files:
        file = request.files[key]
        if file.filename == "":
            return jsonify({"message": "No media found!", "error": True})
        print("file: ", file.filename)      
        uploaded_file = manager.upload_file(file_folder, file)
        data.append({"src": uploaded_file})

    return jsonify({"message": "Files uploaded successfully!", "success": True, "data": data})

@app.route('/close/', methods=['POST'])
def close():
    close = scraper.close()
    return close

@app.route('/test-mode/', methods=['POST'])
def get_test_url():
    src = [{"src": "static/0713.mp4"}, {"src": "static/0713.mp4"}, {"src": "static/icon-512.png"}]
    return jsonify({"data": src})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
