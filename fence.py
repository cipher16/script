#!/usr/bin/python

import SocketServer
import re

status="down"
class FenceHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	global status
        self.data = self.request.recv(4096)
	re_get_name = re.compile("GET /api/vms/\?search=name%3D(.*) HTTP/1.1",re.IGNORECASE)	
	result_name = re_get_name.search(self.data)

	#If there is no Get, it's a posted action
	if result_name == None:
		self.request.send("HTTP/1.1 200 OK\r\nContent-Type: application/xml\r\n\r\n<action />\r\n")
		status="up"
		return

	#Else it's a normal request, answer ...
	name = "none"

	if result_name != None:
		name = result_name.group(1)
	self.request.send("HTTP/1.1 200 OK\r\nContent-Type: application/xml\r\n\r\n<vms><vm id=\"id\" href=\"osef\"><name>"+name+"</name><type>server</type><status><state>"+status+"</state></status></vm></vms>\r\n")
	status = "down"

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    server = SocketServer.TCPServer((HOST, PORT), FenceHandler)
    server.serve_forever()
