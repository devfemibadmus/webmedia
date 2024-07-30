from flask import Flask, request, jsonify, render_template
from platforms.instagram import get_instagram_data
from platforms.tiktok import get_tiktok_images, get_tiktok_videos
from helper import *
import re


app = Flask(__name__, static_url_path='/static')
application = app

@app.route('/webmedia/api/', methods=['POST'])
@app.route('/api/', methods=['POST'])
def api():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    tiktok_video = tiktok_video_id(url)
    tiktok_images = tiktok_photo_id(url)
    instagram_code = instagram_shortcode(url)

    if tiktok_video:
        data = get_tiktok_videos(url, tiktok_video)
    elif tiktok_images:
        data = get_tiktok_images(url, tiktok_images)
    elif instagram_code:
        data = get_instagram_data(instagram_code)
    else:
        return jsonify({'error': True, 'message': 'UNSUPPORTED URL FORMAT.'}), 400

    if not isinstance(data, dict):
        return jsonify({'error': True, 'message': data.replace('error: ', '')})
    return jsonify({'success': True, 'message': 'Successful', 'data':data})


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

