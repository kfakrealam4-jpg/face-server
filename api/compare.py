from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

FACE_KEY    = 'tyn0KUxz1KbnMFW4fLQ5vf1Zo3cnQIMZ'
FACE_SECRET = 'YKCWzdDDP6hJlLBGUMxte14856oDDXr4'

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            data   = json.loads(body)

            img1 = data.get('image1', '')
            img2 = data.get('image2', '')

            if ',' in img1: img1 = img1.split(',')[1]
            if ',' in img2: img2 = img2.split(',')[1]

            if not img1 or not img2:
                self._json({'error': 'Images missing', 'success': False, 'score': 0}, 400)
                return

            post_data = urllib.parse.urlencode({
                'api_key':        FACE_KEY,
                'api_secret':     FACE_SECRET,
                'image_base64_1': img1,
                'image_base64_2': img2,
            }).encode('utf-8')

            req = urllib.request.Request(
                'https://api-cn.faceplusplus.com/facepp/v3/compare',
                data=post_data,
                method='POST'
            )
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')

            with urllib.request.urlopen(req, timeout=20) as resp:
                result = json.loads(resp.read().decode('utf-8'))

            if 'confidence' in result:
                score = round(result['confidence'])
                self._json({'score': score, 'success': True})
            elif 'error_message' in result:
                self._json({'score': 0, 'success': False, 'error': result['error_message']})
            else:
                self._json({'score': 0, 'success': False, 'error': 'Unknown response'})

        except Exception as e:
            self._json({'error': str(e), 'score': 0, 'success': False}, 500)

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
