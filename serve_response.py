from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/response.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Serving response.html at http://localhost:{port}")
    print("Press Ctrl+C to stop the server.")
    httpd.serve_forever()

if __name__ == "__main__":
    # Change directory to where response.html is located
    os.chdir('/Users/ssohoni/workspace_project')
    run_server()
