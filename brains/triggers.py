import os
import sys
import pycurl

class Output:
	def __init__(self):
		self.output = {'public': True, 'msg': None}

	def set_private(self):
		self.output['public'] = False
	
	def set_output(self,output):
		self.output['msg'] = output

	def callback(self,buff):
		# Used for methods requiring a callback to retrieve stdout
		self.output['msg'] = buff

def ip(msg_dict):
	out = Output()
	out.set_private()

	c = pycurl.Curl()
	c.setopt(c.URL,'www.whatismyip.com/automation/n09230945.asp')
	c.setopt(c.WRITEFUNCTION, out.callback)
	c.perform()
	c.close()

	return out.output

# Need to find a way to format it so that a dictionary is always returned and
# does not need to be specified, specifically, in the trigger method.
# Create a decorator of sorts, that will format the output into a dictionary
# declarying the output public uless otherwise specified, accompanied with the
# output.

class Trigger:
	'''
		Establishes a set of pre-defined triggers and allows for the
		addition of new triggers.
	'''
	triggers = {'!ip': ip}

	def __init__(self,name=None,func=None):
		if name and func:
			triggers[name] = func
