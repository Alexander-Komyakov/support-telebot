if __name__ == "main":
	exit()

from extended_database import ExtendedDataBase


class Authenticator:
	def __init__(self):
		self.db = ExtendedDataBase()
		self.__update_all_user_name()
		self.__update_all_admin_name()

	def __update_all_user_name(self):
		self.all_user_name = self.db.get_all_user_name()

	def __update_all_admin_name(self):
		self.all_admin_name = self.db.get_all_admin()

	def authentication(self, name):
		self.__update_all_user_name()
		self.__update_all_admin_name()
		if name in self.all_user_name:
			return "user"
		elif name in self.all_admin_name:
			return "admin"
		else: 
			return "no"
