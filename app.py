import requests, re
from flask_limiter import Limiter
from platforms.tiktok import TikTok
from platforms.facebook import Facebook
from datetime import datetime, timedelta
from platforms.instagram import Instagram
from flask_limiter.util import get_remote_address
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='website/static', template_folder='website')

limiter = Limiter(
    get_remote_address, 
    app=app,
    default_limits=[]
)

request_timestamps = []
RATE_LIMIT = 2
RATE_LIMIT_PERIOD = timedelta(minutes=8)

instagram = None
application = app

class Validator:
    tiktok_video_pattern = r'tiktok\.com/.*/video/(\d+)'
    tiktok_photo_pattern = r'tiktok\.com/.*/photo/(\d+)'
    instagram_pattern = r'(?:https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/)([A-Za-z0-9_-]+)/?'
    facebook_pattern = r"(https?:\/\/)?(www\.|web\.)?facebook\.com\/(share\/[vr]\/\w+|[^\/]+\/videos\/\d+\/?|reel\/\d+)"

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

        if re.match(Validator.facebook_pattern, url) is not None:
            return "Facebook", "Facebook"

        return "Invalid URL", None

@app.route('/webmedia/api/', methods=['POST', 'GET'])
@app.route('/api/', methods=['POST', 'GET'])
@limiter.limit("3 per minute")
def api():
    url = request.form.get('url') if request.method == 'POST' else request.args.get('url')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    
    if not url:
        return jsonify({'error': True, 'message': 'URL is required'}), 400

    source, item_id = Validator.validate(url)

    if source == "Facebook":
        facebook =Facebook()
        data = facebook.getVideo(url)
        if "error" in data:
            return jsonify({'error': True, 'message': 'server error', 'error_message': data}), 500
        return jsonify({'success': True, 'data': data}), 200
    
    elif source == "Instagram":
        if item_id:
            data = instagram.getData(item_id, cut)
            if "error" in data or "require_login" in data:
                return jsonify({'error': True, 'message': 'server error', 'error_message': data}), 500
            return jsonify({'success': True, 'data': data}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid Instagram video URL'}), 400
    
    elif source == "TikTok Video":
        if item_id:
            data = TikTok.get_videos(url, item_id, cut)
            if "error" in data:
                return jsonify({'error': True, 'message': 'server error', 'error_message': data}), 500
            return jsonify({'success': True, 'data': data}), 200
        else:
            return jsonify({'error': True, 'message': 'Invalid TikTok video URL'}), 400
    
    elif source == "TikTok Photo":
        if item_id:
            data = TikTok.get_images(url, item_id, cut)
            if "error" in data:
                return jsonify({'error': True, 'message': 'server error', 'error_message': data}), 500
            return jsonify({'success': True, 'data': data}), 200
        else:
            return jsonify({'error': True, 'message': 'Invalid TikTok Photo URL'}), 400
    
    return jsonify({'error': True, 'message': 'Unsupported URL'}), 400

@app.route('/webmedia/sleep', methods=['GET'])
@app.route('/sleep', methods=['GET'])
def sleep():
    global request_timestamps, instagram
    now = datetime.now()
    request_timestamps = [timestamp for timestamp in request_timestamps if now - timestamp < RATE_LIMIT_PERIOD]
    
    if len(request_timestamps) >= RATE_LIMIT:
        return jsonify(success=False, error="Rate limit exceeded, try again later."), 429
    request_timestamps.append(now)
    try:
        if instagram:
            instagram.close()
            instagram = None
            return jsonify(success=True, message="Instagram instance closed and put to sleep."), 200
        else:
            return jsonify(success=False, message="No active Instagram instance to close."), 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(success=False, error="An error occurred while closing Instagram instance: {}".format(str(e))), 500

@app.before_request
def before_any_request():
    print('remote address: ', request.remote_addr)
    global instagram
    if not instagram:
        instagram = Instagram()

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({
        'error': True,
        'message': 'Too Many Requests',
        'details': 'You have exceeded the rate limit. Please wait a minute and try again.'
    }), 429

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)


