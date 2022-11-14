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

	def getToBdDecorator(function):
		def wrapper(self, *argv):
			try:
				func = function(self, *argv)
				return func
			except Exception as err:
				print("Failed database: ", err)
				return 1
			except:
				return 1
		return wrapper
	
	def addToBdDecorator(function):
		def wrapper(self, *argv):
			try:
				func = function(self, *argv)
				self.commit()
				return 0
			except Exception as err:
				print("Failed database: ", err)
				return 1
			except:
				return 1
		return wrapper
	
	@getToBdDecorator
	def get_keyboard(self):
		keyboard = self.cursor.execute("SELECT * FROM keyboards")
		return keyboard.fetchall()

	@getToBdDecorator
	def get_instruction(self):
		instruction = self.cursor.execute("SELECT * FROM instructions")
		return instruction.fetchall()

	@getToBdDecorator
	def get_user_id(self, name):
		user_id = self.cursor.execute("SELECT id_user FROM users WHERE user_name=(?)", name)
		return user_id.fetchall()

	@getToBdDecorator
	def get_user_name(self, id_user):
		user_name = self.cursor.execute("SELECT user_name FROM users WHERE id_user=(?)", id_user)
		return user_name.fetchall()

	@getToBdDecorator
	def get_user_full(self, username):
		user_full = self.cursor.execute("SELECT * FROM users WHERE user_name=(?)", username)
		return user_full.fetchall()

	@getToBdDecorator
	def get_all_user_full(self):
		user_all_full = self.cursor.execute("SELECT * FROM users")
		return user_all_full.fetchall()

	@getToBdDecorator
	def get_all_user_name(self):
		all_user_name = self.cursor.execute("SELECT user_name FROM users")
		return all_user_name.fetchall()

	@getToBdDecorator
	def get_all_admin(self):
		all_admin = self.cursor.execute("SELECT user_name FROM admins")
		return all_admin.fetchall()
	
	@getToBdDecorator
	def get_user_name_question(self, id_quest):
		user_name = self.cursor.execute("SELECT user_name FROM questions WHERE id_quest=(?)", (id_quest))
		return user_name.fetchall()

	@getToBdDecorator
	def get_all_questions(self):
		questions = self.cursor.execute("SELECT * FROM questions")
		return questions.fetchall()

	@getToBdDecorator
	def get_contacts(self):
		contacts = self.cursor.execute("SELECT * FROM contacts")
		return contacts.fetchall()

	def tryExceptError(function):
		def wrapper(self):
			try:
				func = function(self)
			except:
				func = False
			return func
		return wrapper

	@addToBdDecorator
	def update_admin_chat_id(self, admin_name, chat_id):
		add_chat_id = self.cursor.execute("UPDATE admins SET chat_id=(?) WHERE user_name=(?)",
										 (chat_id, admin_name))

	@addToBdDecorator
	def delete_user(self, id_user):
		deluser = self.cursor.execute("DELETE FROM users WHERE id_user=(?)", (id_user))

	@addToBdDecorator
	def delete_questions_user(self, user_name):
		delete_questions = self.cursor.execute("DELETE FROM questions WHERE user_name=(?)", (user_name))

	@addToBdDecorator
	def delete_question(self, id_quest):
		delete_question = self.cursor.execute("DELETE FROM questions WHERE id_quest=(?)", (id_quest))

	@addToBdDecorator
	def add_question(self, quest, user_name):
		qustion= self.cursor.execute("INSERT INTO questions(question,"+
										" user_name) VALUES (?, ?)", (quest, user_name))
	@addToBdDecorator
	def add_user(self, user_name, first_name=None, last_name=None, phone_number=None):
		user = self.cursor.execute("INSERT INTO users(user_name, first_name, last_name, phone_number) VALUES(?, ?, ?, ?)", [user_name, first_name, last_name, phone_number])
	
	def commit(self):
		self.connection.commit()
