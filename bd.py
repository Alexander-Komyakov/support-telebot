if __name__ == "__main__":
	exit()

import sqlite3 as sql


class DataBase:
	def __init__(self):
		self.db_path = "db.db"
		self.connection = sql.connect("db.db", check_same_thread=False)
		self.cursor = self.connection.cursor()
		self.cursor.execute("pragma foreign_keys=ON")

	def __del__(self):
		self.connection.close()
	
	def getUserId(self, name):
		user_id = self.cursor.execute("SELECT id_user FROM users WHERE user_name='"+name+"'")
		return user_id.fetchall()

	def getUserName(self, id_user):
		user_name = self.cursor.execute("SELECT user_name FROM users WHERE id_user=(?)", id_user)
		return user_name.fetchall()

	def getUserInfo(self, name):
		user_info = self.cursor.execute("SELECT * FROM users WHERE user_name='"+name+"'")
		return user_info.fetchall()

	def getAllUserInfo(self):
		user_info = self.cursor.execute("SELECT * FROM users")
		return user_info.fetchall()

	def getWhiteList(self):
		users = self.cursor.execute("SELECT user_name FROM users")
		return users.fetchall()

	def getAdminList(self):
		admins = self.cursor.execute("SELECT user_name FROM admins")
		return admins.fetchall()
	
	def getQuestions(self):
		questions = self.cursor.execute("SELECT * FROM questions")
		return questions.fetchall()

	def tryExceptError(function):
		def wrapper(self):
			try:
				func = function(self)
			except:
				func = False
			return func
		return wrapper

	def addToBdDecorator(function):
		def wrapper(self, arg1, arg2=None, arg3=None, arg4=None, arg5=None):
			try:
				if arg5 != None:
					func = function(self, arg1, arg2, arg3, arg4, arg5)
				elif arg4 != None:
					func = function(self, arg1, arg2, arg3, arg4)
				elif arg3 != None:
					func = function(self, arg1, arg2, arg3)
				elif arg2 != None:
					func = function(self, arg1, arg2)
				else:
					func = function(self, arg1)
				self.commit()
				return 0
			except Exception as err:
				print("Failed database: ", err)
				return 1
			except:
				return 1
		return wrapper

	@addToBdDecorator
	def updateAdminChatId(self, admin_name, chat_id):
		add_chat_id = self.cursor.execute("UPDATE admins SET chat_id=(?) WHERE user_name=(?)",
										 (chat_id, admin_name))

	@addToBdDecorator
	def delUser(self, id_user):
		deluser = self.cursor.execute("DELETE FROM users WHERE id_user=(?)", (id_user))

	@addToBdDecorator
	def delQuestionsUser(self, user_name):
		delquest = self.cursor.execute("DELETE FROM questions WHERE user_name=(?)", (user_name))

	@addToBdDecorator
	def delQuestion(self, id_quest):
		delquest = self.cursor.execute("DELETE FROM questions WHERE id_quest=(?)", (id_quest))

	@addToBdDecorator
	def addQuestion(self, quest, user_name):
		question = self.cursor.execute("INSERT INTO questions(question,"+
										" user_name) VALUES (?, ?)", (quest, user_name))
	@addToBdDecorator
	def addUser(self, user_name, first_name, last_name, phone_number):
		users = self.cursor.execute("INSERT INTO users(user_name, first_name, last_name, phone_number) VALUES(?, ?, ?, ?)", [user_name, first_name, last_name, phone_number])

	@addToBdDecorator
	def addUserWhiteList(self, nameUser):
		users = self.cursor.execute("INSERT INTO users(user_name)"+
									" VALUES (?)", [nameUser])
	
	def commit(self):
		self.connection.commit()

	#myDb.addUserWhiteList("Vasya"))
	#myDb.addCategory("home"))
	#myDb.addCost('22.10.2022', 'coffee', 280.0)
