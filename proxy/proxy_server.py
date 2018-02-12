"""A proxy server that implements cacheing and interacts with another higher-level server"""

import SocketServer
import SimpleHTTPServer
import httplib

PORT = 12345

class ProxyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    """To handle requests for the proxy server and return cached pages if needed"""

    def check_if_recent()

    
httpd = SocketServer.TCPServer(("", PORT), ProxyRequestHandler)

print "serving at port", PORT
httpd.serve_forever()
