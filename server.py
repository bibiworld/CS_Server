#!/usr/bin/python
#coding:utf-8

import SocketServer
import BIBIUserCheck
import BIBIODB
import re
import select

mybibi = BIBIUserCheck.BIBIUserCheck()
curUser = BIBIODB.BIBIUserODB("未登录")

class MyTCPHandler(SocketServer.BaseRequestHandler):
	'''
		after handle self.request(socket) will close
	'''
	def handle_deal_request(self):
		ready_to_read, ready_to_write, in_error = select.select([self.request], [self.request,], [])
		self.data = self.request.recv(1024).strip()
		if (len(ready_to_read) == 1 and len(self.data) == 0) or (self.data.count('BIBI_quit') > 0):
			return False
		
		print self.data, mybibi.isRigister(self.data), mybibi.isLogin(self.data), mybibi.isSearch(self.data)
		global curUser
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
			reinfo =  ok.registerAccount(password)
			ok.commit()
			print reinfo
			if (reinfo == True):
				self.request.sendall("BIBI_register((1))")
			elif (reinfo == False):
				self.request.sendall("BIBI_register((0))")
			else:
				self.request.sendall("error register")
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
			reinfo =  ok.loginAccount(password)	
			ok.commit()
			print reinfo
			if (reinfo.count("Error:Name is wrong") == 1):
				self.request.sendall("BIBI_login((0)(0))")
			elif (reinfo.count("Error:passwd is wrong") == 1):
				self.request.sendall("BIBI_login((1)(0))")
			elif (reinfo.count("GoodJob") == 1):
				self.request.sendall("BIBI_login((1)(1))")
				curUser = ok
			else:
				self.request.sendall("error login")
			'''
				search
			'''
		elif  (mybibi.isSearch(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			word = item[0].strip('(').strip(')')
			reinfo = curUser.searchWord(word)
			if (len(reinfo) == 1):
				self.request.sendall("BIBI_search((0)(0)(0)(0))")
			else:
				wordInfo = []
				for i in range(4):
#<<<<<<< HEAD
					si = reinfo[i]
					if (si.count('(') > 0):
						si = si.replace('(', '<*', si.count('('))
					if (reinfo[i].count(')') > 0):
						si = si.replace(')', '*>', si.count(')'))
					if (len(si) == 0):
						si = '0'
					wordInfo.append(si)
				self.request.sendall("BIBI_search(({words})({soundmark})({meaning})({examples}))".format(words=wordInfo[0].encode("utf-8"), soundmark=wordInfo[1].encode("utf-8"), meaning=wordInfo[2].encode("utf-8"),examples=wordInfo[3].encode("utf-8")))
#=======
				#	if (len(reinfo[i]) == 0):
				#		reinfo[i] = '0'
				#print ({meaning})
				#**BUG**
				#print reinfo[2].encode("utf-8")
				#文件为utf8格式，而reinfo为unicode，在文件中不能出现，所以应该先转化为utf8格式
				#self.request.sendall("BIBI_search(({words})({soundmark})({meaning})({examples}))".format(words=reinfo[0].encode("utf-8"), soundmark=reinfo[1].encode("utf-8"), meaning=reinfo[2].encode("utf-8"),examples=reinfo[3].encode("utf-8")))
#>>>>>>> 78f65e92aed4c01c3659de6b8e25392f840de5ef
		return True
		
	def handle(self):
		print "{} wrote".format(self.client_address[0])
		while (True):
			if (self.handle_deal_request() == False):
				break
		print "{} quit".format(self.client_address[0])	
				
if __name__ == "__main__":
	HOST, PORT = "59.66.131.117", 1234
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	server.serve_forever()