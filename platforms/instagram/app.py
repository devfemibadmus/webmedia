from flask import Flask, request, abort, jsonify
from bot import Instagram

app = Flask(__name__)
ALLOWED_IPS = {'34.45.139.151'}

instagram = None
application = app

@app.before_request
def before_any_request():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
    print('remote address: ', request.remote_addr)
    global instagram
    if not instagram:
        instagram = Instagram()

@app.route('/', methods=['GET', 'POST'])
def nigga():
    item_id = request.form.get('item_id') if request.method == 'POST' else request.args.get('item_id')
    cut = request.form.get('cut') if request.method == 'POST' else request.args.get('cut')
    if item_id:
        data = instagram.getData(item_id, cut)
        if isinstance(data, dict):  # Check if data is a dictionary
            if 'platform' in data:  # Check if 'platform' key exists in data
                return jsonify({'success': True, 'data': data})
            else:
                return jsonify({'error': True, 'message': 'Platform not found in data', 'data': data})
        else:
            return jsonify({'error': True, 'message': 'Invalid data format', 'data': data})
    else:
        return jsonify({'success': False, 'error': 'item_id not provided'}), 404

if __name__ == '__main__':
    app.run(debug=True)
