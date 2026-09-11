import http.server
import json
import mimetypes
import os
import pathlib

PORT = 5173
PUBLIC = pathlib.Path(__file__).parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def do_GET(self):
        url = self.path.split('?')[0]
        if url == '/api/tree':
            p = PUBLIC / 'tree-data.json'
            if p.exists():
                data = p.read_text('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data.encode('utf-8'))
                return
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{}')
            return
        return super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'\n  Aeperion EVDB')
    print(f'  http://localhost:{PORT}\n')
    server.serve_forever()
