import re
from pathlib import Path
from datetime import datetime
from platforms.tiktok import TikTok
from platforms.instagram import Instagram
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_folder='templates/static', template_folder='templates')
application = app

instances = []

class Validator:
    tiktok_video_pattern = r'tiktok\.com/.*/video/(\d+)'
    tiktok_photo_pattern = r'tiktok\.com/.*/photo/(\d+)'
    instagram_pattern = r'(?:https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/)([A-Za-z0-9_-]+)/?'

    @staticmethod
    def validate(url):
        video_match = re.search(Validator.tiktok_video_pattern, url)
        if video_match:
            return "TikTok Video", video_match.group(1)

        photo_match = re.search(Validator.tiktok_photo_pattern, url)
        if photo_match:
            return "TikTok Photo", photo_match.group(1)

        insta_match = re.match(Validator.instagram_pattern, url)
        if insta_match:
            return "Instagram", insta_match.group(1)

        return "Unknown", None

def read_action(file_path='action.txt'):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/webmedia/api/', methods=['POST', 'GET'])
@app.route('/api/', methods=['POST', 'GET'])
def api():
    url = request.form.get('url') if request.method == 'POST' else request.args.get('url')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    instagram = next((instance['instance'] for instance in instances if instance['name'] == 'instagram'), None)
    source, item_id = Validator.validate(url)
    if source == "Instagram":
        if not instagram:
            return jsonify({'error':True, 'message':'Instagram instance closed, check back in few minutes or go to https://github.com/devfemibadmus/webmedia for more info'})
        return jsonify({'success':True, 'data':instagram.getData(url, item_id, cut)}) if url else jsonify({'error':True, 'message':'aswear i no know'})
    elif source == "TikTok Video":
        return jsonify({'success':True, 'data':TikTok.get_videos(url, item_id, cut)}) if url else jsonify({'error':True, 'message':'aswear i no know'})
    return jsonify({'error':True, 'message':'Unsupported url'})

@app.before_request
def before_any_request():
    global instances
    action = read_action()
    if action == "end":
        instagram = next((instance['instance'] for instance in instances if instance['name'] == 'instagram'), None)
        if instagram:
            instagram.end()
            instances = [instance for instance in instances if instance['name'] != 'instagram']
            instances.append({'name': 'end instagram', 'instance': None})
    elif action == "start":
        if not any(instance['name'] == 'instagram' for instance in instances):
            instagram = Instagram()
            instances.append({'name': 'instagram', 'instance': instagram})

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

