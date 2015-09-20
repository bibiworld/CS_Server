#encoding=utf-8

class BIBIUserCheck(object):
	BIBI_INIT_POS = 5
	BIBI_REGISTER_BRACKETS = 3
	BIBI_LOGIN_BRACKETS = 3
	BIBI_SEARCH_BRACKETS = 1
	
	'''
		check if it is register request
	'''
	def isRigister(self, tcpData):
		if (tcpData.find('register') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_REGISTER_BRACKETS) and (tcpData.count(')') == self.BIBI_REGISTER_BRACKETS):
				return True
		return False
		
	'''
		check if it is login request
	'''
	def isLogin(self, tcpData):
		if (tcpData.find('login') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_LOGIN_BRACKETS) and (tcpData.count(')') == self.BIBI_LOGIN_BRACKETS):
				return True
		return False
		
	'''
		check if it is search request
	'''
	def isSearch(self, tcpData):
		if (tcpData.find('search') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == BIBI_SEARCH_BRACKETS) and (tcpData.count(')') == BIBI_SEARCH_BRACKETS):
				return True
		return False