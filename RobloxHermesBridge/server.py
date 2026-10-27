import http.server
import json
import urllib.parse
import threading

command_queue = []
latest_result = None

class BridgeHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        global command_queue
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        command_queue.append(data)
        print(f"[Hermes Bridge] Queued command: {data}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "queued", "command": data}).encode('utf-8'))

    def do_GET(self):
        global command_queue, latest_result
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/poll':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if command_queue:
                cmd = command_queue.pop(0)
                self.wfile.write(json.dumps(cmd).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"action": "none"}).encode('utf-8'))
        elif parsed_path.path == '/result':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                latest_result = json.loads(self.rfile.read(content_length).decode('utf-8'))
                print(f"[Roblox Studio Result] {latest_result}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "received"}')
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=5000):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, BridgeHandler)
    print(f"[Hermes Roblox Bridge] Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
