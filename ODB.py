#!/usr/bin/python
#coding:utf-8
'''
registerAccount():
	�����������������룬��ʾ��������ʾĬ��Ϊ���������롱
	ע��ɹ�ʱ����True��ʧ��ΪFalse������bug�� print "Error:regAcconut"

loginAccount():
	����һ�����������루�ַ�����
	��½�ɹ��Ƿ��ء�goodjob���� ʧ��Ϊ "Error:passwd is wrong"
	
searchWord():
	��ѯ���ʣ�����һ������������ƴд
	�ɹ������б���Ϣ��ʧ�ܷ����б� ["Error:no word"]
	
���ø���ĺ���֮����ص������commit����
	
�ĵ���������ȫ������close() ������
�罫���ļ���Ϊģ�飬��ؽ���ĩ��cursor.close() bibi.close() �����ע��
'''

import MySQLdb

serverIP = "localhost"


bibi = MySQLdb.connect(host = serverIP, user = "root", passwd = "unityispower",db = "bibidata");
cursor = bibi.cursor()

class BIBIUserODB:
	def __init__(self, username):
		self.userName = username
		
	def registerAccount(self, passwd, tishi = "��������"):
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

'''��������ɹ����ú󣬲����ٴδ����ݿ��в�ѯ��Ϣ��˵�����ݿ��в�û��������
�������ݣ������û�û�������ݿ�Ĳ��������commit��������
���磬	user.registerAccount()
		user.loginAccount()
�������ÿһ�ε��û���¼ֻ����ע�ᣬ�ڵ�½��ֱ�ӵ�½�ᷢ�ֳ��ִ���
�����û�û������ĺ�����������ٵ���user.commit()����
���	user.commit()����
'''