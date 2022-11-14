if __name__ == "main":
	exit()


import time


class Message_Queue:
	def __init__(self):
		self.queue = []
	
	def add_to_queue(self, *message):
		print("добавляю в очередь сообщение")
		self.queue.append(message)
	
	def send_message(self, message):
		print("отправляю сообщение из очереди")
	
	def queue_loop(self):
		print("запущен бесконечный цикл отправки сообщений из очереди")
		while True:
			if self.queue != []:
				print("очередь не пуста")
				for i in self.queue[:30]:
					self.send_message(i)
			else:
				print("очередь пуста")
			print("удаляю из очереди последний 30 сообщение")
			print(self.queue[:30])
			self.queue = self.queue[30:]
			time.sleep(1)
