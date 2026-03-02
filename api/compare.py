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
            img1 = data.get('image1', '').split(',')[-1]
            img2 = data.get('image2', '').split(',')[-1]
            if not img1 or not img2:
                self._json({'error': 'Images missing'}, 400)
                return
            post_data = urllib.parse.urlencode({
                'api_key':        FACE_KEY,
                'api_secret':     FACE_SECRET,
                'image_base64_1': img1,
                'image_base64_2': img2,
            }).encode()
            req = urllib.request.Request(
                'https://api-us.faceplusplus.com/facepp/v3/compare',
                data=post_data
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
            confidence = result.get('confidence', 0)
            self._json({'score': round(confidence), 'success': True})
        except Exception as e:
            self._json({'error': str(e), 'score': 0, 'success': False}, 500)

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
