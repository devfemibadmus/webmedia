import requests, re
from datetime import datetime
from platforms.tiktok import TikTok
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='website/static', template_folder='website')
application = app

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

@app.route('/webmedia/api/', methods=['POST', 'GET'])
@app.route('/api/', methods=['POST', 'GET'])
def api():
    url = request.form.get('url') if request.method == 'POST' else request.args.get('url')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    
    if not url:
        return jsonify({'error': True, 'message': 'URL is required'}), 400

    source, item_id = Validator.validate(url)
    
    if source == "Instagram":
        try:
            response = requests.get('http://35.226.151.94/instagram/', params={'item_id': item_id, 'cut': cut})
            print(response.text)
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return jsonify({'error': True, 'message': f'Yo {str(e)}'}), 500
    
    elif source == "TikTok Video":
        if item_id:
            data = TikTok.get_videos(url, item_id, cut)
            return jsonify({'success': True, 'data': data})
        else:
            return jsonify({'error': True, 'message': 'Invalid TikTok video URL'}), 400
    
    return jsonify({'error': True, 'message': 'Unsupported URL'}), 400

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)


