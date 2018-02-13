"""A proxy server that implements cacheing and interacts with another higher-level server"""

import sys
import os
import time
import SocketServer
import SimpleHTTPServer
import httplib

if len(sys.argv) >= 2:
    PORT = int(sys.argv[1])
else:
    PORT = 12345


if len(sys.argv) >= 3:
    MASTER_PORT = int(sys.argv[2])
else:
    MASTER_PORT = 20000

class ProxyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    """To handle requests for the proxy server and return cached pages if needed"""

    # current assumption: all files requested are present on server
    def do_GET(self):

        filename = self.path.strip("/")

        # HTTP connection object
        conn = httplib.HTTPConnection("127.0.0.1", MASTER_PORT)

        if os.path.isfile(filename):

            filetime = time.ctime(os.path.getmtime(filename))

            # test print
            print filetime

            conn.request("GET", filename, headers = {"If-Modified-Since" : filetime})

            response = conn.getresponse()

            if response.status != 304 :
                os.remove(filename)

                f = open(filename, "w+")
                f.write(response.read())
                f.close()

            else :
                pass

        else :

            conn.request("GET", filename)

            response = conn.getresponse()

            f = open(filename, "w+")
            f.write(response.read())
            f.close()

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


sock = SocketServer.TCPServer(("", PORT), ProxyRequestHandler)

print "serving at port", PORT
sock.serve_forever()
