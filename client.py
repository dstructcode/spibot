#!/usr/bin/python
import sys
import socket
import string
import time
import MySQLdb

class Client:
	def __init__(self,conf):
		self.irc_client = {'network': '', 'port': '', 'nick': '', 'ident': '', 
						   'password': '', 'real_name': '', 'owner': '', 
						   'channels': [], 'server': '', 'host': ''}
		self.handlers = []
		self.irc_client = conf
		self.irc_socket = self.create_socket()

	def setup_client(self,settings):
		self.irc_client = settings
	
		return

	def create_socket(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		return sock

	def get_socket(self):
		return self.irc_socket

	def connect(self):
		init = True

		self.irc_socket.connect((self.irc_client['network'],int(self.irc_client['port'])))

		read_buffer = ''
		chan_str = ''

		print self.irc_socket.recv(4096)

		self.irc_socket.send('NICK %s\r\n' % self.irc_client['nick'])
		# <username> <hostname> <servername> <realname>
		self.irc_socket.send('USER %s %s %s %s\r\n' % (self.irc_client['ident'],self.irc_client['host'],self.irc_client['server'],self.irc_client['real_name']))
		
		for chan in self.irc_client['channels']:
			chan_str += chan + ','

		while True:
			read_buffer += self.irc_socket.recv(4096)
			buffer_list = string.split(read_buffer, '\r\n')
			read_buffer = buffer_list.pop()

			for line in buffer_list:
				line = line.rstrip().split()

				# Formatting of line needs to be done here.
				# Then a check for server messages.
				# Somehow the cleaned and parsed line needs to be sent
				# to a listener that is checking for commands or learning
				# capability.

				print line

				if line[0] == 'PING':
					self.irc_socket.send("PONG %s\r\n" % line[1])
				# Need to parse all PRIVMSGs
				elif line[1] == 'PRIVMSG' and line[3] == ':\x01VERSION\x01':
				 	version = '\x01VERSION siri:0.0.1:Created with python\x01'
				 	self.irc_socket.send('PRIVMSG %s :%s\r\n' % (line[2],version))
					if init:
						self.irc_socket.send('JOIN %s\r\n' % chan_str)
						print 'INITIAL JOIN ===================================================='
						init = False
				elif len(self.handlers) > 0:
					if line[1] == 'PRIVMSG':
						for handler in self.handlers:
							handler.parse_privmsg(line)

	def server_msg(self,msg):  # Determines whether the message is a server message and needs to be responded to
		pass
					
	def add_handler(self, obj):
		self.handlers.append(obj)
	

''' 
    module = __import__(module_name)
    reload(module)
    module.parsemsg(line)
'''
