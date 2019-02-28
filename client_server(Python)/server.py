import socket
import sys
import os

class MySocket():
	
	HOST = ''
	PORT = 6547

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn = ""
	addr = ""
	

	def construct(self):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.bind((self.HOST, self.PORT))
			print("Waiting for Client...")
		except Exception as e:
			print(str(e))
		self.s.listen(10)
		self.conn, self.addr = self.s.accept()
		print("New Client: " + str(self.addr))

	def getData(self):
		return self.conn.recv(1024)

	def sendData(self, data):		
		self.s.listen()
		c, a = self.s.accept()
		c.sendall(data.encode())
		c.close()  
		