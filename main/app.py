from flask import Flask, render_template, request, jsonify, session, Response
import os, uuid, time, threading, atexit, urllib.parse
from engine.helper import GlobalMessagesManager
from flask_cors import cross_origin
from engine.scraper import Scraper
from google.cloud import storage
from pathlib import Path

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

    def delete_file(self, file_path):
        if file_path:
            blob = self.bucket.blob(file_path)
            blob.delete()
            return True
        return False
class Common:
    def __init__(self):
        self.binList = []

    def get_folder(self, url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        path_components = path.split('/')
        folder = '/'.join(path_components[2:-1])
        return folder

    def get_file_name(self, url: str) -> str:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        path_components = path.split('/')
        file_name = path_components[-1]
        return file_name

    def add_to_bin_list(self, bin_list):
        timestamp = time.time() + 180
        for bin in bin_list:
            folder = self.get_folder(bin)
            file_name = self.get_file_name(bin)
            bin = f"{folder}/{file_name}"
            if bin not in [b[0] for b in self.binList]:
                self.binList.append((bin, timestamp))
        print("binList: ", self.binList)

    def threemin_autodelete(self):
        while True:
            time.sleep(1)
            current_time = time.time()
            bins_to_delete = []

            for bin, delete_time in self.binList:
                if current_time >= delete_time:
                    try:
                        print(f"delete {bin}: {manager.delete_file(bin)}")
                        self.binList.remove((bin, delete_time))
                    except:
                        pass

manager = CloudStorageManager()
common = Common()

delete_thread = threading.Thread(target=common.threemin_autodelete)
# stop_event = threading.Event()
delete_thread.daemon = True
delete_thread.start()

@app.route('/app/', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def home():
    userId = session['userId']
    globalMessage = GlobalMessagesManager(userId)
    if request.method == 'POST':
        if not request.form.get('src'):
            return "Nigga"
        if not globalMessage.pageUnload():
            globalMessage.pageUnload()
            return jsonify({"message": "wait for a process to end before requesting new one", "cancel": True})
        globalMessage.updateMessage(f"Starting")
        globalMessage.reset()
        globalMessage.reload()
        scraper = Scraper(userId)
        message = scraper.getMedia(request.form.get('src'))
        if "error" in message.lower():
            return jsonify({"message":message, "error":True})
        return jsonify({"message":message})
    return render_template("home.html")

@app.route('/uploadMedia', methods=['POST'])
@cross_origin()
def upload_video():
    if len(request.files) == 0:
        return jsonify({"message": "No media found!", "error": True})

    file = next(iter(request.files.values()))

    if file.filename == "":
        return jsonify({"message": "Missing file name", "error": True})

    file_size_mb = file.content_length / (1024 * 1024) 
    file_folder = request.form.get('file_folder')
    mediaType = request.form.get('mediaType')

    if file_size_mb > 80:
        return jsonify({"message": "Media too big for web, Try using app", "error": True})
    
    data = manager.upload_file(file_folder, file)

    return jsonify({"message": "Files uploaded successfully!", "success": True, "src": data, "mediaType": mediaType})

@app.route('/getData', methods=['POST'])
def getData():
    globalMessage = GlobalMessagesManager(session['userId'])
    globalMessage.update()
    message = globalMessage.getMessage()
    mediaurl = globalMessage.getData()
    common.add_to_bin_list(globalMessage.getUrl())
    # print(mediaurl)
    return jsonify({'message':message, 'mediaurl':mediaurl})

@app.before_request
def ensure_userId():
    if 'userId' not in session:
        session['userId'] = str(uuid.uuid4())

def stop_thread():
    stop_event.set()
    delete_thread.join()

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


# atexit.register(stop_thread)


if __name__ == '__main__':
    app.run(debug=True)

