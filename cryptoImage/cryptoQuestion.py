#!/usr/bin/env python3.5

import socketserver
import socket
import threading




class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        timeout = 10
	#self.data = self.request.recv(1024).strip()
        self.request.sendall(b"Welcome to the Crypto box. Caesar would be proud!\n")
        self.request.sendall(b'mxqj yi jxu ixyvj veh jxyi squiqh syfxuh? \n')
        self.response = self.request.recv(1024).strip()
        self.return_response = 'Your response was : {}\n'.format(self.response.decode('ascii'))
        self.request.sendall(self.return_response.encode('utf-8'))
        if self.response.decode('ascii').lower() == '10':
            self.request.sendall(b'good job. That is correct. Here is the flag {Th1s_r3@lly_w@snt_@ll_t4@t_t3rr1bl3}. Also here are the creds to this box, username alice password "nooneshouldknowthis"\n')
            return
        else:
            self.request.sendall(b'Sorry that is the wrong answer. Try again later\n')
            return 

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	timeout = 10
	allow_reuse_address = True

	def handle_timeout(self):
		print('Timeout!')
	pass



if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), MyHandler)
    #server = socketserver.TCPServer((HOST, PORT), MyHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    
    try:
        #server.serve_forever()
        server_thread = threading.Thread(target=server.serve_forever())
        server_thread.daemon = True
        server_thread.start()
        print('server started')


    except KeyboardInterrupt:
        server.close()
        server.shutdown()
