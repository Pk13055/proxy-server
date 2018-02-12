import os
import time
import SocketServer
import SimpleHTTPServer

PORT = 12345

class HTTPCacheRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def send_head(self):

        """First things first- making a basic server to serve files"""
        
        if self.command == "GET" :

            filename = self.path.strip("/")

            if os.path.isfile(filename):

                    self.send_response(200)
                    self.end_headers()
                    return None

        return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

    def end_headers(self):

        filename = self.path.strip("/")

        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)


s = SocketServer.ThreadingTCPServer(("", PORT), HTTPCacheRequestHandler)

s.allow_reuse_address = True

print "Serving on port", PORT

s.serve_forever()

