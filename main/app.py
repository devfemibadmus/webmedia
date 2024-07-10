from flask import Flask, render_template, request, jsonify, make_response, Response, send_file
from pathlib import Path
import random, string

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, static_url_path='/static')

test_mode = True

def testMode(video_url):
    image_links = [
        'https://cdnb.artstation.com/p/assets/images/images/034/948/193/large/aniket-gawande-01.jpg?1613671560',
        'https://img.freepik.com/premium-photo/fun-cowboy-3d-illustration_183364-14701.jpg',
        'https://storage.prompt-hunt.workers.dev/clflhwtzv000ll8079q60ff0s_1',
        'https://imgv3.fotor.com/images/gallery/cartoon-character-generated-by-Fotor-ai-art-creator.jpg',
        'https://img.freepik.com/premium-photo/little-boy-cowboy-with-cartoon-style-3d-rendering_646510-2373.jpg'
    ]
    return {'media_url': "https://videocdn.cdnpk.net/videos/dfedd6d9-20e8-40b5-8e93-9303f9f31930/horizontal/previews/videvo_watermarked/large.mp4", 'thumbnail_url': random.choice(image_links)}


@app.route('/app/', methods=['POST'])
def save_media():
    video_url = request.form.get('url')
    if test_mode:
        response_data = testMode(video_url)
    elif "facebook"in video_url:
        response_data = facebook(video_url)
    elif "youtube" in video_url:
        response_data = youtube(video_url)
    elif "instagram" in video_url:
        response_data = instagram(video_url)
    elif "tiktok" in video_url:
        response_data = tiktok(video_url)

    return jsonify(response_data)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


"""
if __name__ == '__main__':
    app.run(debug=True)
"""
application = app