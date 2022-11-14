if __name__ == "main":
	exit()


from extended_database import ExtendedDataBase
from message_sender import Message_Sender
from message_queue import Message_Queue
import telebot
import threading


class Msg_handler:
	def __init__(self, bot):
		self.bot = bot
		threading.Lock()
		self.exdb = ExtendedDataBase()
		self.keyboard = self.exdb.get_keyboard()
		self.contacts = self.exdb.get_contacts()[0][1]
		self.msg_sender = Message_Sender(bot)
		self.instruction = self.exdb.get_instruction()
		self.msg_queue = Message_Queue()
		self.msg_queue_loop = threading.Thread(target=self.msg_queue.queue_loop)
		self.msg_queue_loop.start()


	def go_contact_it(self, message):
		msg_id = message.chat.id
		msg_question = message.text
		self.exdb.add_question(msg_question, message.from_user.username)
		self.msg_sender.send_message(msg_id, "Ваш вопрос принят", "user_menu")

	def add_user_step1(self, message):
		user_name = message.text
		msg_id = message.chat.id
		users = self.exdb.get_all_user_name()
		if not user_name in users:
			self.add_user_info.append(message.text)
			add_user_first_name = self.msg_sender.send_message(msg_id, "Введите имя", "user_menu")
			self.msg_sender.register_next_step_handler(add_user_first_name, self.add_user_step2)
		else:
			add_user_first_name = self.msg_sender.send_message(msg_id, "Пользователь уже добавлен", "user_menu")

	def add_user_step2(self, message):
		msg_id = message.chat.id
		self.add_user_info.append(message.text)
		add_user_last_name = self.msg_sender.send_message(msg_id, "Введите Фамилию", "user_menu")
		self.msg_sender.register_next_step_handler(add_user_last_name, self.add_user_step3)

	def add_user_step3(self, message):
		msg_id = message.chat.id
		self.add_user_info.append(message.text)
		add_user_phone_number = self.msg_sender.send_message(msg_id, "Введите Телефон", "user_menu")
		self.msg_sender.register_next_step_handler(add_user_phone_number, self.add_user_step4)

	def add_user_step4(self, message):
		msg_id = message.chat.id
		self.add_user_info.append(message.text)
		self.exdb.add_user(self.add_user_info[0], self.add_user_info[1],
						self.add_user_info[2], self.add_user_info[3])
		self.msg_sender.send_message(msg_id, "Пользователь добавлен", "user_menu")

	def delete_user(self, message):
		msg_id = message.chat.id
		if self.exdb.delete_user(message.text):
			self.msg_sender.send_message(msg_id, "Пользователь удален", "user_menu")
		else:
			self.msg_sender.send_message(msg_id, "Пользователь не найден", "user_menu")

	def delete_question(self, message):
		msg_id = message.chat.id
		if self.exdb.delete_question(message.text):
			self.msg_sender.send_message(msg_id, "Вопрос удален", "user_menu")
		else:
			self.msg_sender.send_message(msg_id, "Вопрос не найден", "user_menu")

	def go_message_block(self, message):
		msg_id = message.chat.id
		self.msg_sender.send_message(msg_id, "Вы не авторизованный пользовате."+
												" Обратитесь к администратору.",
												"user_menu")
	def go_message_admin(self, message):
		msg = message.text
		msg_id = message.chat.id
		#юзеры
		if msg == self.keyboard[0][2][0][0]:
			self.exdb.get_keyboard()
			self.msg_sender.send_message(msg_id, "Пользователи",
							"admin_menu")
			for i in self.exdb.get_all_user_full():
				i = map(str, i)
				self.msg_sender.send_message(msg_id, " ".join(i),
								"admin_menu")
		#удалить пользователя
		elif msg == self.keyboard[0][2][0][2]:
			delete_id_user = self.msg_sender.send_message(msg_id, "Введите id пользователя", "admin_menu")
			self.msg_sender.register_next_step_handler(delete_id_user, self.delete_user)
		#удалить вопрос
		elif msg == self.keyboard[0][2][1][1]:
			delete_id_question = self.msg_sender.send_message(msg_id, "Введите id вопроса", "admin_menu")
			self.msg_sender.register_next_step_handler(delete_id_question, self.delete_question)
		#рассылка
		elif msg == self.keyboard[0][2][2][0]:
			self.exdb.update_admin_chat_id(message.from_user.username, msg_id)
			self.msg_sender.send_message(msg_id, "Рассылка включена", "admin_menu")
		#отключить рассылку
		elif msg == self.keyboard[0][2][2][1]:
			self.exdb.update_admin_chat_id(message.from_user.username, "")
			self.msg_sender.send_message(msg_id, "Рассылка отключена", "admin_menu")
		#добавить пользователя
		elif msg == self.keyboard[0][2][0][1]:
			add_user_name = self.msg_sender.send_message(msg_id, "Введите телеграмм имя пользователя без @", "admin_menu")
			self.add_user_info = []
			#добавление пользователя в несколько шагов
			#сохраняем последовательно в массив введенные данные
			#на последнем шаге добавляем в базу данных пользователя
			self.msg_sender.register_next_step_handler(add_user_name, self.add_user_step1)
		#вопросы
		elif msg == self.keyboard[0][2][1][0]:
			for i in self.exdb.get_all_questions():
				i = map(str, i); i = " ".join(i)
				self.msg_sender.send_message(msg_id, "".join(i), "admin_menu")
		else:
			self.msg_sender.send_message(msg_id, "Ошибка ввода", "admin_menu")
	
	def go_message(self, message):
		msg = message.text
		msg_id = message.chat.id
		if msg == ("/start"):
			self.msg_sender.send_message(msg_id, "Приветствую! Я помогу тебе, пользователь!", "user_menu")

		#инструкции
		elif msg == self.keyboard[2][2][0][1]:
			self.msg_sender.send_message(msg_id, "Держи инструкции", "instruction")

		#контакты
		elif msg == self.keyboard[2][2][1][0]:
			#self.msg_sender.send_message(msg_id, self.contacts, "user_menu")
			self.msg_queue.add_to_queue(msg_id, self.contacts, "user_menu")
		#обращение в it отдел
		elif msg == self.keyboard[2][2][0][0]:
			question = self.msg_sender.send_message(msg_id, "Задайте свой вопрос", "user_menu")
			self.msg_sender.register_next_step_handler(question, self.go_contact_it)
		#названия инструкций
		elif msg in self.keyboard[1][2][0][0]:
			self.msg_sender.send_document(msg_id, self.instruction[msg][0], "user_menu")
			self.msg_sender.send_document(msg_id, self.instruction[msg][1], "user_menu")
		else:
			self.msg_sender.send_message(msg_id, "Попробуйте еще раз...", "user_menu")
