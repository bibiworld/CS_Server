#!/usr/bin/python
#coding:utf-8
'''
registerAccount():
	传入两个参数，密码，提示，其中提示默认为“忘记密码”
	注册成功时返回True，失败为False，出现bug， print "Error:regAcconut"

loginAccount():
	传入一个参数，密码（字符串）
	登陆成功是返回“goodjob”， 失败为 "Error:passwd is wrong"
	
searchWord():
	查询单词，传入一个参数，单词拼写
	成功返回列表信息，失败返回列表 ["Error:no word"]
	
调用该类的函数之后务必调用类的commit函数
	
文档最后因程序安全加上了close() 函数，
如将该文件作为模块，务必将文末的cursor.close() bibi.close() 的语句注释
'''

import MySQLdb

serverIP = "localhost"


bibi = MySQLdb.connect(host = serverIP, user = "root", passwd = "unityispower",db = "bibidata");
cursor = bibi.cursor()

class BIBIUserODB:
	def __init__(self, username):
		self.userName = username
		
	def registerAccount(self, passwd, tishi = "忘记密码"):
		checkSql = "select * from bibi_admin \
		where name = '%s'" % (self.userName)
		cursor.execute(checkSql)
		checkIsOk = cursor.fetchone()
		#print checkIsOk
		if (checkIsOk == None):
			regSql = "insert into bibi_admin (name, pwd, tishi) \
			values('%s', '%s', '%s')" % (self.userName, passwd, tishi)
			#print regSql
			try:
				cursor.execute(regSql)
			except:
				print "Error:regAcconut"
			return True
		else:
			return False
		
	def loginAccount(self, passwd):
		loginSql = """select * from bibi_admin
		where name = '%s'
		""" % (self.userName)
		cursor.execute(loginSql)
		infoList = cursor.fetchone()
		if (infoList == None):
			return "Error:Name is wrong"
		elif(infoList[2] == passwd):
			return "GoodJob"
		else:
			return "Error:passwd is wrong"
			
	def searchWord(self, word):
		searchSql = """select * from bibi_word
		where spell = '%s'
		""" % (word)
		cursor.execute(searchSql)
		infoList = cursor.fetchone()
		if (infoList == None):
			return ["Error:no word"]
		else:
			return infoList
		
	def commit(self):
		bibi.commit()#*************
#user = BIBIUserODB("can")
#print user.loginAccount("can")
#print user.registerAccount("can")

#cursor.close()
#bibi.close()

'''如果函数成功调用后，不能再次从数据库中查询信息，说明数据库中并没有真正的
插入数据，这是用户没有在数据库的操作后加入commit函数所至
例如，	user.registerAccount()
		user.loginAccount()
结果发现每一次的用户登录只能先注册，在登陆，直接登陆会发现出现错误，
就是用户没有在类的函数调用最后再调用user.commit()导致
添加	user.commit()即可
'''