#!/usr/bin/python3


import telebot
import os
import time
from auth import Authenticator
from msg_handler import Msg_handler


bot = telebot.TeleBot(os.environ["Electronintorg"], parse_mode="HTML")
msg_handler = Msg_handler(bot)
auth = Authenticator()

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
	if auth.authentication(message.from_user.username):
		msg_handler.go_message(message)
	elif auth.authentication(message.from_user.username) == "admin":
		msg_handler.go_message_admin(message)
	else:
		msg_handler.go_message_block(message)


@bot.message_handler(content_types = ["text"])
def send_welcome(message):
	if auth.authentication(message.from_user.username) == "user":
		msg_handler.go_message(message)
	elif auth.authentication(message.from_user.username) == "admin":
		msg_handler.go_message_admin(message)
	else:
		msg_handler.go_message_block(message)


bot.polling()
