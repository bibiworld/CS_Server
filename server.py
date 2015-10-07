#!/usr/bin/python
#coding:utf-8

import SocketServer
import BIBIUserCheck
import BIBIODB
import re

mybibi = BIBIUserCheck.BIBIUserCheck()
curUser = BIBIODB.BIBIUserODB("未登录")

class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle_deal_request(self):
		self.data = self.request.recv(1024).strip()
		print "{} wrote".format(self.client_address[0])
		print "len: ", len(self.data)
		if (len(self.data) == 0):
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
			print item
			word = item[0].strip('(').strip(')')
			reinfo = curUser.searchWord(word)
			if (len(reinfo) == 1):
				self.request.sendall("BIBI_search((0)(0)(0)(0))")
			else:
				for i in range(4):
					if (len(reinfo[i]) == 0):
						reinfo[i] = '0'
				#print ({meaning})
				#**BUG**
				#print reinfo[2].encode("utf-8")
				#文件为utf8格式，而reinfo为unicode，在文件中不能出现，所以应该先转化为utf8格式
				self.request.sendall("BIBI_search(({words})({soundmark})({meaning})({examples}))".format(words=reinfo[0].encode("utf-8"), soundmark=reinfo[1].encode("utf-8"), meaning=reinfo[2].encode("utf-8"),examples=reinfo[3].encode("utf-8")))
		return True
		
	def handle(self):
		while (True):
			if (self.handle_deal_request() == False):
				break
		print "wokao"
				
if __name__ == "__main__":
	HOST, PORT = "59.66.131.117", 1234
	
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	
	server.serve_forever()