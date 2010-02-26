#!/usr/bin/env python

import os
import sys
import ConfigParser

from client import Client

from brains import commands
from brains import triggers
from brains import auth

CONFIG_PATH = './spibot.conf'

class Spibot:
	def __init__(self):
		self.connection = None
		self.bot = {}
	
	def parse_privmsg(self,msg):
		parsed_msg = {}

		# remove : from user/host combo
		msg[0] = msg[0][1:]
		user_host = msg[0].split('!')

		parsed_msg['user'] = user_host[0]
		parsed_msg['host'] = user_host[1]
		parsed_msg['channel'] = msg[2]

		# remove : from actual message
		actual_msg = msg[3:]
		actual_msg[0] = actual_msg[0][1:]

		parsed_msg['msg'] = actual_msg

		self.handle_msg(parsed_msg)

	def handle_msg(self,msg_dict):
		# auth.auth(msg_dict['user'],msg_dict['host'],'Blah270')
		if msg_dict['msg'][0][0] == '!':
			trigger = msg_dict['msg'][0][1:]
			if hasattr(triggers,trigger):
				method = getattr(triggers,trigger)
				output = method(msg_dict)
				if output['msg']:
					if output['public']:
						print "SENDING PUBLIC"
						self.privmsg(msg_dict['channel'],output['msg'])
					else:
						print "SENDING PRIVATE"
						self.notice(msg_dict['user'],output['msg'])
				else:
					print "NO MSG RETURNED"
		elif self.bot['nick'] in msg_dict['msg']:
			if msg_dict['msg'][0] == self.bot['nick']:
				command = msg_dict['msg'][1]
				if hasattr(commands,command):
					method = getattr(commands,command)
					output = method(msg_dict)
					print "OUTPUT: ", output
				else:
					# proceed as if being spoken to and not requested of
			else:
				#talk randomly or just ignore or store the info, etc
				pass
		elif auth.is_authed(msg_dict['user'],msg_dict['host']):
			if 'join' in msg_dict['msg']:
				self.join(msg_dict['msg'][1])
			if 'reload' in msg_dict['msg']:
				self.reload(msg_dict['channel'])
			elif 'disconnect' in msg_dict['msg']:
				self.disconnect()

	def privmsg(self,channel,msg):
		self.connection.send("PRIVMSG %s :%s\r\n" % (channel,msg))

	def notice(self,person,msg):
		self.connection.send('NOTICE %s :%s\r\n' % (person,msg))

	def join(self,channel):
		self.connection.send('JOIN %s\r\n' % channel)

	def add_connection(self,socket):
		self.connection = socket
	
	def reload(self,channel):
		import_str = "from brains import *"
		exec import_str
		self.privmsg(channel,"Reloading complete")
	
	def disconnect(self):
		self.connection.send("QUIT :%s\r\n" % "Stalk you guys later!")
		exit(0)

	def parse_config(self):
		settings_dict = {}
		config = ConfigParser.ConfigParser()
		config.read(CONFIG_PATH)
		conf_settings = config.items('spibot')

		for item in conf_settings:
			key = str(item[0])
			if key == 'channels':
				value = list(item[1].split())
				settings_dict[key] = value
				continue
			value = str(item[1])
			settings_dict[key] = value

		self.bot = settings_dict

		return settings_dict

def main():
	bot = Spibot()
	# bot.db_connect()
	conf = bot.parse_config()
	
	client = Client(conf)	
	client.add_handler(bot)

	bot.add_connection(client.get_socket())
	client.connect()

if __name__ == "__main__":
    main()
