if __name__ == "main":
	exit()


from instructor import Instructor
from bd import DataBase
import telebot


class Msg_handler:
	def __init__(self, bot):
		self.bot = bot
		self.instructor = Instructor()
		self.ins_name = self.instructor.get_instruction_names()
		self.bd = DataBase()
		self.build_keyboard()
		self.contacts = self.get_contacts_in_file()

	def get_contacts_in_file(self):
		pathfile = "contact.txt"
		with open(pathfile, "r", encoding="utf-8") as contactsf:
			contacts = contactsf.read()
		return contacts

	def go_contact_it(self, message):
		msg_id = message.chat.id
		msg_question = message.text
		self.bd.addQuestion(msg_question, message.from_user.username)
		self.bot.send_message(msg_id, "Ваш вопрос принят", reply_markup=self.mrkp_menu)
	
	def find_id_user(self, id_user):
		allUserInfo = self.bd.getAllUserInfo()
		for i in allUserInfo:
			if id_user == str(i[0]):
				return True
		return False

	def find_id_question(self, id_quest):
		allQuestions = self.bd.getQuestions()
		for i in allQuestions:
			if id_quest == str(i[0]):
				return True
		return False

	def get_users(self):
		users = self.bd.getWhiteList()
		users = list(map(lambda n: n[0], users))
		return users

	def add_user_step1(self, message):
		user_name = message.text
		users = self.get_users()
		if not user_name in users:
			self.add_user_info.append(message.text)
			add_user_first_name = self.bot.send_message(message.chat.id, "Введите имя",
													reply_markup=self.mrkp_admin)
			self.bot.register_next_step_handler(add_user_first_name, self.add_user_step2)
		else:
			add_user_first_name = self.bot.send_message(message.chat.id, "Пользователь уже добавлен",
													reply_markup=self.mrkp_admin)

	def add_user_step2(self, message):
		self.add_user_info.append(message.text)
		add_user_last_name = self.bot.send_message(message.chat.id, "Введите Фамилию",
												reply_markup=self.mrkp_admin)
		self.bot.register_next_step_handler(add_user_last_name, self.add_user_step3)

	def add_user_step3(self, message):
		self.add_user_info.append(message.text)
		add_user_phone_number = self.bot.send_message(message.chat.id, "Введите Телефон",
												reply_markup=self.mrkp_admin)
		self.bot.register_next_step_handler(add_user_phone_number, self.add_user_step4)

	def add_user_step4(self, message):
		self.add_user_info.append(message.text)
		self.bd.addUser(self.add_user_info[0], self.add_user_info[1],
						self.add_user_info[2], self.add_user_info[3])
		self.bot.send_message(message.chat.id, "Пользователь добавлен",
								reply_markup=self.mrkp_admin)

	def delete_user(self, message):
		msg_id = message.chat.id
		if self.find_id_user(message.text):
			user_name = self.bd.getUserName(message.text)[0]
			self.bd.delQuestionsUser(user_name)
			self.bd.delUser(message.text)
			self.bot.send_message(msg_id, "Пользователь удален", reply_markup=self.mrkp_admin)
		else:
			self.bot.send_message(msg_id, "Пользователь не найден", reply_markup=self.mrkp_admin)
	def delete_question(self, message):
		msg_id = message.chat.id
		if self.find_id_question(message.text):
			self.bd.delQuestion(message.text)
			self.bot.send_message(msg_id, "Вопрос удален", reply_markup=self.mrkp_admin)
		else:
			self.bot.send_message(msg_id, "Вопрос не найден", reply_markup=self.mrkp_admin)
	
	def build_keyboard(self):
		self.mrkp_menu = telebot.types.ReplyKeyboardMarkup(True)
		self.mrkp_menu.row("✉️ Обращение в IT отдел", "📖 Инструкции")
		self.mrkp_menu.row("📞 Контакты", "♥️ Пожелания")

		self.mrkp_admin = telebot.types.ReplyKeyboardMarkup(True)
		self.mrkp_admin.row("🤷‍♀️ Юзеры", "🤷‍♀️ Добавить", "🤷‍♀️ Удалить")
		self.mrkp_admin.row("❓ Вопросы", "❓ Удалить")
		self.mrkp_admin.row("🔔\nРассылка", "🔕\nОтключить")

		self.mrkp_ins = telebot.types.ReplyKeyboardMarkup()
		for i in self.ins_name:
			self.mrkp_ins.row(i)


	def go_message_block(self, message):
		msg_id = message.chat.id
		self.bot.send_message(msg_id, "Вы не авторизованный пользователь."+
										" Обратитесь к администратору.",
						reply_markup=self.mrkp_menu)
	def go_message_admin(self, message):
		msg = message.text
		msg_id = message.chat.id
		if msg == "🤷‍♀️ Юзеры":
			self.bot.send_message(msg_id, "Пользователи",
							reply_markup=self.mrkp_admin)
			for i in self.bd.getAllUserInfo():
				i = (i[0], "@" + i[1], i[2], i[3])
				i = map(str, i)
				i = " ".join(i)
				self.bot.send_message(msg_id, "".join(i), reply_markup=self.mrkp_admin)
		elif msg == "🤷‍♀️ Удалить":
			delete_id_user = self.bot.send_message(msg_id, "Введите id пользователя",
							reply_markup=self.mrkp_admin)
			self.bot.register_next_step_handler(delete_id_user, self.delete_user)
		elif msg == "❓ Удалить":
			delete_id_question = self.bot.send_message(msg_id, "Введите id вопроса",
							reply_markup=self.mrkp_admin)
			self.bot.register_next_step_handler(delete_id_question, self.delete_question)
		elif msg == "🔔\nРассылка":
			self.bd.updateAdminChatId(message.from_user.username, msg_id)
			self.bot.send_message(msg_id, "Рассылка включена", 
									reply_markup=self.mrkp_admin)
		elif msg == "🔕\nОтключить":
			self.bd.updateAdminChatId(message.from_user.username, "")
			self.bot.send_message(msg_id, "Рассылка отключена", 
									reply_markup=self.mrkp_admin)
		elif msg == "🤷‍♀️ Добавить":
			add_user_name = self.bot.send_message(msg_id, "Введите телеграмм имя пользователя. Пример - AlexanderKomyakov - без '@', Неправильно: @AlexanderKomyakov",
							reply_markup=self.mrkp_admin)
			self.add_user_info = []
			#добавление пользователя в несколько шагов
			#сохраняем последовательно в массив введенные данные
			#на последнем шаге добавляем в базу данных пользователя
			self.bot.register_next_step_handler(add_user_name, self.add_user_step1)
		elif msg == "❓ Вопросы":
			for i in self.bd.getQuestions(): i = map(str, i); i = " ".join(i)
				self.bot.send_message(msg_id, "".join(i), reply_markup=self.mrkp_admin)
		else:
			self.bot.send_message(msg_id, "Ошибка ввода", reply_markup=self.mrkp_admin)
	
	def go_message(self, message):
		msg = message.text
		msg_id = message.chat.id
		if msg == ("/start"):
			self.bot.send_message(msg_id, "Здесь должно быть приветствие",
							reply_markup=self.mrkp_menu)

		elif msg == "📖 Инструкции":
			self.bot.send_message(msg_id, "Держи инструкции",
							reply_markup=self.mrkp_ins)

		elif msg == "📞 Контакты":
			self.bot.send_message(msg_id, self.contacts,
							reply_markup=self.mrkp_menu)
		elif msg == "✉️ Обращение в IT отдел":
			question = self.bot.send_message(msg_id,
							"Задайте свой вопрос",
							reply_markup=self.mrkp_menu)
			self.bot.register_next_step_handler(question, self.go_contact_it)
		elif msg in self.ins_name:
			ins_text = self.instructor.get_instruction_text(msg)
			ins_photo = self.instructor.get_instruction_photo(msg)
			ins_doc = self.instructor.get_instruction_document(msg)
			for i in range(len(ins_text)):
				try:
					self.bot.send_document(msg_id, ins_doc[i],
									reply_markup=self.mrkp_menu)
				except:
					pass
				self.bot.send_message(msg_id, ins_text[i],
								reply_markup=self.mrkp_menu)
				try:
					self.bot.send_photo(msg_id, ins_photo[i],
									reply_markup=self.mrkp_menu)
				except:
					pass
			self.bot.send_message(msg_id, "В меню ->",
							reply_markup=self.mrkp_menu)
		else:
			self.bot.send_message(msg_id,
							"Попробуйте еще раз...",
							reply_markup=self.mrkp_menu)
