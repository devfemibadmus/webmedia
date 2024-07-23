from flask import Flask, render_template, request, jsonify, session, Response
from engine.helper import GlobalMessagesManager
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
from pathlib import Path
import os, uuid, base64

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'aaaaaaaaaaa2222222222!!!!!!!!!##'
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
    userId = session['userId']
    if request.method == 'POST':
        if not request.form.get('src'):
            return "Nigga"
        GlobalMessagesManager.updateMessage(f"Starting")
        GlobalMessagesManager.update()
        scraper = Scraper(userId)
        return jsonify({'message':scraper.getMedia(request.form.get('src'))})
    return render_template("home.html")

@app.route('/uploadMedia', methods=['POST'])
@cross_origin()
def upload_video():
    print("request.files: ", request.files)
    print("session['userId'] ", session['userId'])

    if len(request.files) == 0:
        return jsonify({"message": "No media found!", "error": True})

    file = next(iter(request.files.values()))

    if file.filename == "":
        return jsonify({"message": "Missing file name", "error": True})

    file_type = request.form.get("file_type")
    file_data = base64.b64encode(file.read()).decode('utf-8')
    print("file_type: ", file_type)

    GlobalMessagesManager.setData({'blob': file_data, 'type': file_type})

    return jsonify({"message": "Gotten a blob", "success": True})

@app.route('/getData', methods=['POST'])
def getData():
    GlobalMessagesManager.update()
    message = GlobalMessagesManager.getMessage()
    blobs = GlobalMessagesManager.getData()
    return jsonify({'message':message, 'blob':blobs})


@app.before_request
def ensure_userId():
    if 'userId' not in session:
        session['userId'] = str(uuid.uuid4())
    if 'blobs' not in session:
        session['blobs'] = []

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
