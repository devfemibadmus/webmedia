import re
from pathlib import Path
from datetime import datetime
from platforms.tiktok import TikTok
from platforms.instagram import Instagram
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')
application = app

instagram = Instagram()

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

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/api/', methods=['POST', 'GET'])
def api():
    url = request.form.get('url') if request.method == 'POST' else request.args.get('url')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    source, item_id = Validator.validate(url)
    if source == "Instagram":
        return jsonify(instagram.getData(url, item_id, cut)) if url else {'error':True, 'message':'aswear i no know'}
    elif source == "TikTok Video":
        return jsonify(TikTok.get_videos(url, item_id, cut)) if url else {'error':True, 'message':'aswear i no know'}
    return {'error':True, 'message':'Unsupported url'}

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)

