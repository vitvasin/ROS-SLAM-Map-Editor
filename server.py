#!/usr/bin/env python3
import http.server
import json
import base64
import os
import signal
import subprocess
import threading

EDITOR_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.normpath(os.path.join(EDITOR_DIR, '..', 'mini_amr', 'amrROS2_ws', 'maps'))
PORT = 7070


class MapEditorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=EDITOR_DIR, **kwargs)

    def end_headers(self):
        if self.path.split('?')[0].endswith('.html'):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        if self.path == '/api/load_map':
            self._handle_load_map()
        elif self.path == '/api/load_keepout':
            self._handle_load_keepout()
        elif self.path == '/api/shutdown':
            self._handle_shutdown()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/save_keepout':
            self._handle_save_keepout()
        else:
            self.send_error(404)

    def _handle_load_map(self):
        pgm_path = os.path.join(MAPS_DIR, 'latest_map.pgm')
        yaml_path = os.path.join(MAPS_DIR, 'latest_map.yaml')

        if not os.path.exists(pgm_path) or not os.path.exists(yaml_path):
            self._json(404, {'error': 'map_not_found'})
            return

        with open(pgm_path, 'rb') as f:
            pgm_b64 = base64.b64encode(f.read()).decode()
        with open(yaml_path, 'r') as f:
            yaml_text = f.read()

        self._json(200, {
            'pgm': pgm_b64,
            'yaml': yaml_text,
            'pgm_name': 'latest_map.pgm',
            'yaml_name': 'latest_map.yaml',
        })

    def _handle_load_keepout(self):
        pgm_path = os.path.join(MAPS_DIR, 'latest_map_keepout.pgm')
        yaml_path = os.path.join(MAPS_DIR, 'latest_map_keepout.yaml')

        if not os.path.exists(pgm_path):
            self._json(404, {'error': 'keepout_not_found'})
            return

        with open(pgm_path, 'rb') as f:
            pgm_b64 = base64.b64encode(f.read()).decode()
        yaml_text = ''
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                yaml_text = f.read()

        self._json(200, {
            'pgm': pgm_b64,
            'yaml': yaml_text,
            'pgm_name': 'latest_map_keepout.pgm',
        })

    def _handle_shutdown(self):
        self._json(200, {'ok': True})
        def _kill():
            import time
            time.sleep(0.3)
            subprocess.Popen(['pkill', '-f', 'chromium'], stderr=subprocess.DEVNULL)
            os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=_kill, daemon=True).start()

    def _handle_save_keepout(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            pgm_bytes = base64.b64decode(data['pgm'])
            yaml_text = data['yaml']

            pgm_path = os.path.join(MAPS_DIR, 'latest_map_keepout.pgm')
            yaml_path = os.path.join(MAPS_DIR, 'latest_map_keepout.yaml')

            with open(pgm_path, 'wb') as f:
                f.write(pgm_bytes)
            with open(yaml_path, 'w') as f:
                f.write(yaml_text)

            self._json(200, {'ok': True})
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', PORT), MapEditorHandler)
    print(f'Map editor server on port {PORT}...')
    server.serve_forever()
