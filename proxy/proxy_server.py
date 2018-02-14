#!/usr/bin/env python2


"""
	A proxy server that implements caching and interacts
	with another higher-level server

"""

from __future__ import print_function
import sys
import os
import time
import SocketServer
import SimpleHTTPServer
import httplib

actual = lambda x: os.path.join(os.getcwd(), 'cache', x)

try:
	MASTER_PORT = int(sys.argv[2])
except:
	MASTER_PORT = 20000

try:
	PORT = int(sys.argv[1])
except:
	PORT = 12345


class ProxyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	"""
		To handle requests for the proxy server and return cached pages if needed

	"""

	def do_GET(self):
		'''
			# current assumption: all files requested are present on server
		'''
		filename = actual(self.path.strip("/"))
		self.path = filename
		# HTTP connection object
		conn = httplib.HTTPConnection("127.0.0.1", MASTER_PORT)

		if os.path.isfile(filename) and not self.headers.get('Cache-control', None) == 'no-cache':
			filetime = time.ctime(os.path.getmtime(filename))
			print("File time : ", filetime)
			conn.request("GET", filename.rsplit('/')[-1], headers = {"If-Modified-Since" : filetime})
			response = conn.getresponse()
			if response.status != 304 :
				os.remove(filename)
				open(filename, "wb+").write(response.read())

		else :
			conn.request("GET", filename.rsplit('/')[-1])
			response = conn.getresponse()
			open(filename, "wb+").write(response.read())

		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def main():
	sock = SocketServer.ThreadingTCPServer(("", PORT), ProxyRequestHandler)
	sock.allow_reuse_address = True
	print("Server started at Port %d | %s" % (PORT, "127.0.0.1"))
	sock.serve_forever()

if __name__ == '__main__':
	main()
