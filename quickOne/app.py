from flask import Flask, request, jsonify, render_template
from quickOne.platforms.tiktok import *
import re

tiktok_video_pattern = r'tiktok\.com/.*/video/(\d+)'
tiktok_photo_pattern = r'tiktok\.com/.*/photo/(\d+)'

app = Flask(__name__, static_url_path='/static')
application = app

@app.route('/api/', methods=['POST'])
def api():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    tiktok_video = re.search(tiktok_video_pattern, url)
    tiktok_images = re.search(tiktok_photo_pattern, url)
    if tiktok_video:
        item_id = tiktok_video.group(1)
        tiktok_videos = get_tiktok_videos(url, item_id)
        if not isinstance(tiktok_videos, dict):
            return jsonify({'error': True, 'message': tiktok_videos.replace('error: ', '')})
        return jsonify({'success': True, 'message': 'Successful', 'data':tiktok_videos})
    elif tiktok_images:
        item_id = tiktok_images.group(1)
        tiktok_images = get_tiktok_images(url, item_id)
        if not isinstance(tiktok_images, dict):
            return jsonify({'error': True, 'message': tiktok_images.replace('error: ', '')})
        return jsonify({'success': True, 'message': 'Successful', 'data':tiktok_images})
    else:
        return jsonify({'error': True, 'message': 'UNSUPPORTED URL FORMAT.'}), 400

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

