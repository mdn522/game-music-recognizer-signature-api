from io import BytesIO
import traceback
from flask import Flask, request, jsonify
from utils.shazam import get_signature
import os

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', '051953d3968f1779ff9aff278640f3ab')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 24 * 1024 * 1024))  # integer in bytes
API_KEY = os.environ.get('API_KEY')


@app.route('/')
async def home():
    return 'Game Music Recognizer Signature API'


@app.route('/welcome')
async def welcome():
    return '''
<html>
<head>
    <title>Game Music Recognizer Signature API</title>
    <style>
    html, body {
        width: 100%;
        height: 100%;
    }
    body {
        width: 100%;
        height: 100%;
        background-color:  #6c5ce7;
        color: #fff;
        font-family: Verdana;
        margin: 0;
        padding: 0;
        
    }
    </style>
</head>
<body>
    <div style="padding: 14px; background-color:  #ef5777;">
        <h1>Game Music Recognizer Signature API</h1>
    </div>
    <!-- <div style="padding: 14px;">
        Shazam Signature API URL: <input type="text" id="api-url">
        <script>
            let shazam_api_url = window.location.href
            document.getElementById('api-url').setAttribute('value', );
        </script>
    </div> -->
</body>
</html>
    '''


@app.route('/api/1.0/shazam/signature/get', methods=['GET', 'POST'])
async def api_get_audio_signature():
    if request.method == 'GET':
        resp = jsonify({
            'success': True,
            'message': 'UP'
        })
        resp.status_code = 200
        return resp

    if API_KEY:
        if 'API_KEY' not in request.form:
            resp = jsonify({
                'success': False,
                'message': 'API key missing',
                'code': 9,
            })
            resp.status_code = 400
            return resp

        if API_KEY != request.form['API_KEY']:
            resp = jsonify({
                'success': False,
                'message': 'Invalid API Key',
                'code': 10,
            })
            resp.status_code = 400
            return resp

    if 'wav_file' not in request.files:
        resp = jsonify({
            'success': False,
            'message': 'No file part in the request',
            'code': 21,
        })
        resp.status_code = 400
        return resp

    file = request.files['wav_file']
    if file.filename == '':
        resp = jsonify({
            'success': False,
            'message': 'No file selected for uploading',
            'code': 22,
        })
        resp.status_code = 400
        return resp

    if not request.content_length:
        resp = jsonify({
            'success': False,
            'message': 'No content',
            'code': 23,
        })
        resp.status_code = 400
        return resp

    data = BytesIO()
    try:
        file.save(data)
    except Exception as e:
        resp = jsonify({
            'success': False,
            'message': str(e),
            'traceback': traceback.format_exc(),
            'code': 24
        })
        resp.status_code = 500
        return resp

    try:
        signature = await get_signature(data.getvalue())
        encoded_signature = signature.encode_to_uri()
    except Exception as e:
        resp = jsonify({
            'success': False,
            'message': str(e),
            'traceback': traceback.format_exc(),
            'code': 25,
        })
        resp.status_code = 500
        return resp

    resp = jsonify({
        'success': True,
        'signature': encoded_signature
    })
    return resp


if __name__ == '__main__':
    app.run(debug=True)
