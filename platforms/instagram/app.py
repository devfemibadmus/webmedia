from flask import Flask, request, abort, jsonify
from bot import Instagram

app = Flask(__name__)
ALLOWED_IPS = {'127.0.0.1', '34.123.29.121'}

instagram = None
application = app

@app.before_request
def before_any_request():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
    global instagram
    if not instagram:
        instagram = Instagram()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    item_id = request.form.get('item_id') if request.method == 'POST' else request.args.get('item_id')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    if item_id:
        data = instagram.getData(item_id, cut)
        if data['platform']:
            return jsonify({'success': True, 'data': data})
        return jsonify({'error': True, 'message': data})
    else:
        return jsonify({'success': False, 'error': 'item_id not provided'}), 404

if __name__ == '__main__':
    app.run(debug=True)
