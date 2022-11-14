if __name__ == "main":
	exit()


from extended_database import ExtendedDataBase
import telebot


class Message_Sender:
	def __init__(self, bot):
		self.bot = bot
		self.exdb = ExtendedDataBase()
		self.build_keyboard()
	
	def build_keyboard(self):
		self.source_keyboards = self.exdb.get_keyboard()
		self.keyboards = {}
		for i in self.source_keyboards:
			self.keyboards[i[1]] = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
			for j in i[2]:
				self.keyboards[i[1]].add(*j)
	
	def send_photo(self, chat_id=None, photo=None, keyboard=""):
		bot_send = self.bot.send_photo(chat_id, photo, 
										reply_markup=self.keyboards[keyboard])
		return bot_send

	def send_document(self, chat_id=None, document=None, keyboard=""):
		bot_send = self.bot.send_document(chat_id, document, 
											reply_markup=self.keyboards[keyboard])
		return bot_send

	def send_message(self, chat_id=None, message=None, keyboard=""):
		bot_send = self.bot.send_message(chat_id, message, 
											reply_markup=self.keyboards[keyboard])
		return bot_send
	
	def register_next_step_handler(self, message, func):
		self.bot.register_next_step_handler(message, func)
