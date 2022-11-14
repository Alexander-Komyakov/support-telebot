if __name__ == "main":
	exit()


from database import DataBase
import io


class ExtendedDataBase:
	def __init__(self):
		self.db = DataBase()
	
	#проверка существования id пользователя
	#реализовать через запросы к бд в database.py
	#по возврату из бд определять есть или нет
	def find_id_user(self, id_user):
		if not (self.db.get_user_name(id_user) in [1, []]):
			return True
		else:
			return False
	
	#аналогично find_id_user
	def find_id_question(self, id_question):
		if not (self.db.get_user_name_question(id_question) in [1, []]):
			return True
		else:
			return False
	
	def get_instruction(self):
		instruction_source = list(self.db.get_instruction())
		instruction = {}
		for i in range(0, len(instruction_source)):
			name = instruction_source[i][1]
			docx_bin = io.BytesIO(instruction_source[i][2])
			docx_bin.name = name+".html"
			html_bin = io.BytesIO(instruction_source[i][3])
			html_bin.name = name+".docx"
			instruction[name] = [docx_bin, html_bin]
		return instruction

	def get_keyboard(self):
		#преобразовываем в ИЗМЕНЯЕМЫЙ list
		keyboard_source = list(self.db.get_keyboard())
		keyboard_source = list(map(list, keyboard_source))
		#разбиваем строку с клавишами на двумерный массив
		for i in range(len(keyboard_source)):
			keyboard_source[i][2] = keyboard_source[i][2].split(";")
			for j in range(len(keyboard_source[i][2])):
				keyboard_source[i][2][j] = keyboard_source[i][2][j].split("'")
		return keyboard_source

	def get_all_user_name(self):
		all_user_name = self.db.get_all_user_name()
		try:
			for i in range(0, len(all_user_name)):
				all_user_name[i] = all_user_name[i][0]
			return all_user_name
		except:
			print("get_all_user_name_error")
		#return list(map(lambda n: n[0], self.db.get_all_user_name()))
		return 1

	def get_all_admin(self):
		return list(map(lambda n: n[0], self.db.get_all_admin()))

	def get_contacts(self):
		return self.db.get_contacts()

	def get_all_questions(self):
		return self.db.get_all_questions()
	
	def find_user_name(self, user_name):
		#получить все имена пользователей и найти среди них user_name
		user_name_all = self.get_all_user_name()
		if user_name in user_name_all:
			return True
		else:
			return False
	
	def delete_user(self, id_user=None, user_name=None):
		#удаление всех вопросов пользователей
		#без него не удалится пользователь
		if not (user_name := self.db.get_user_name(id_user)) in [1, []]:
			user_name = user_name[0]
			self.db.delete_questions_user(user_name)
			self.db.delete_user(id_user)
			return True
		else:
			return False
	
	def delete_question(self, id_question):
		if self.find_id_question(id_question):
			self.db.delete_question(id_question)
			return True
		else:
			return False

	def get_all_user_full(self):
		return self.db.get_all_user_full()

	def add_user(self, *argv):
		self.db.add_user(*argv)
	
	def add_question(self, question, user_name):
		self.db.add_question(question, user_name)
	
	def update_admin_chat_id(self, *argv):
		self.db.update_admin_chat_id(*argv)
