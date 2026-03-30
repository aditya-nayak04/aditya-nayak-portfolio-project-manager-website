import os, http.server, socketserver, sys

os.chdir('/Users/adityanayak/Documents/Claude/nayakaditya-replica')
port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 4321))
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('', port), handler) as httpd:
    print(f'Serving on port {port}')
    httpd.serve_forever()
