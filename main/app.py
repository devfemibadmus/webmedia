from flask import Flask, render_template, request, jsonify, session
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
from pathlib import Path
import os, uuid

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
user_instances = {}

@app.route('/app/', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def home():
    userId = session['userId']
    if request.method == 'POST':
        if not request.form.get('src'):
            return "Nigga"
        scraper = Scraper(userId)
        src = request.form.get('src')
        response = scraper.getMedia(src)
        print("response: ", response)
        if isinstance(response, list):
            return jsonify(response)
        return response
    return render_template("home.html")

@app.route('/uploadMedia', methods=['POST'])
@cross_origin()
def upload_video():
    print("request.files: ", request.files)

    if len(request.files) == 0:
        return jsonify({"message": "No media found!", "error": True})

    file = next(iter(request.files.values()))

    if file.filename == "":
        return jsonify({"message": "Missing file name", "error": True})

    file_folder = request.form.get('file_folder')
    print("file_folder: ", file_folder)
    
    data = manager.upload_file(file_folder, file)

    return jsonify({"message": "Files uploaded successfully!", "success": True, "src": data})

@app.before_request
def ensure_userId():
    if 'userId' not in session:
        session['userId'] = str(uuid.uuid4())

@app.route('/close/', methods=['POST'])
def close():
    userId = session.get('userId')
    if userId in user_instances:
        print(userId, " in user_instances")
        scraper = user_instances[userId]
        closed = scraper.close()
        if closed:
            del user_instances[userId]
            session.pop('userId', None)
        return jsonify({'success': closed})
    return jsonify({'success': False, 'message': 'No user ID found or instance not found'})

@app.route('/test-mode/', methods=['POST'])
def get_test_url():
    src = [{"src": "static/0713.mp4"}, {"src": "static/0713.mp4"}, {"src": "static/icon-512.png"}]
    return jsonify({"data": src})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
