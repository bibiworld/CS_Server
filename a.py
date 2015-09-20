#encoding=utf-8
import SocketServer
import BIBIUserCheck
import BIBIODB
import re

mybibi = BIBIUserCheck.BIBIUserCheck()

class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print "{} wrote".format(self.client_address[0])
		print self.data, mybibi.isRigister(self.data), mybibi.isLogin(self.data), mybibi.isSearch(self.data)
		'''
			register 
		'''
		if (mybibi.isRigister(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			print item
			name = item[0].strip('(').strip(')')
			password = item[1].strip('(').strip(')')
			print name, password
			ok = BIBIODB.BIBIUserODB(name)
			print ok.registerAccount(password)
			ok.close()
			'''
				login
			'''
		elif (mybibi.isLogin(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			print item
			name = item[0].strip('(').strip(')')
			password = item[1].strip('(').strip(')')
			print name, password
			ok = BIBIODB.BIBIUserODB(name)
			print ok.loginAccount(password)
			ok.close()
		
		self.request.sendall(self.data.upper())
		
	

if __name__ == "__main__":
	HOST, PORT = "59.66.131.143", 1234
	
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	server.serve_forever()