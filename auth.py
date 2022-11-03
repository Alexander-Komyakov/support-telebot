if __name__ == "main":
	exit()

from bd import DataBase


class Authenticator:
	def __init__(self):
		self.bd = DataBase()
		self.__update_white_list()
		self.__update_admin_list()
	
	def __update_white_list(self):
		self.white_list = self.bd.getWhiteList()
		self.white_list = list(map(lambda n: n[0], self.white_list))

	def __update_admin_list(self):
		self.admin_list = self.bd.getAdminList()
		self.admin_list = list(map(lambda n: n[0], self.admin_list))

	def authentication(self, name):
		self.__update_white_list()
		self.__update_admin_list()
		if name in self.white_list:
			return "user"
		elif name in self.admin_list:
			return "admin"
		else: 
			return "no"
