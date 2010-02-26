import re
import md5
import ConfigParser
import MySQLdb

CONFIG_PATH = './spibot.conf'

class Spibotdb:
	def __init__(self):
		self.db_info = {"host": None, "user": None,
						"pass": None, "db": None}
		self.parse_config()

	def parse_config(self):
		config = ConfigParser.ConfigParser()
		config.read(CONFIG_PATH)
		db_conf = config.items('spibotdb')

		for item in db_conf:
			key = str(item[0])
			value = str(item[1])
			self.db_info[key] = value
	
	def connect(self):
		host = self.db_info['host']
		user = self.db_info['user']
		password  = self.db_info['pass']
		db = self.db_info['db']

		db_conn = MySQLdb.connect(host,user,password,db)

		return db_conn

bot_db = Spibotdb()

def register(user,host,password):
	db = bot_db.connect()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	user = re.escape(user)
	host = re.escape(host)
	password = md5.md5(password)
	query = "INSERT INTO auth (user,host,password) VALUES ('"+user+"','"+host+"','"+password+"'"

	cursor.execute(query)
	result = cursor.fetchall()

	print result

def auth(user,host,password):
	db = bot_db.connect()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	user = re.escape(user)
	host = re.escape(host)
	password = md5.md5(password).hexdigest()
	query = "SELECT * FROM auth WHERE user='"+user+"'"

	cursor.execute(query)
	result = cursor.fetchone()

	print result

	if result:

		print password

		if password == result['password']:
			query = "UPDATE auth SET host = '"+host+"', authed = 1 WHERE user = '"+user+"'"
			cursor.execute(query)
			print "now authed"

	cursor.close()

def deauth(user):
	db = bot_db.connect()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	user = re.escape(user)

	query = "UPDATE auth SET authed = 0 WHERE user = '"+user+"'"
	cursor.execute(query)
	result = cursor.fetchone()
	print result
	cursor.close()	
	return

def is_authed(user,host):
	db = bot_db.connect()
	cursor = db.cursor(MySQLdb.cursors.DictCursor)
	user = re.escape(user)
	host = re.escape(host)
	query = "SELECT * FROM auth WHERE user='"+user+"'"

	cursor.execute(query)
	result = cursor.fetchone()

	if result:
		if result['authed']:
			return True

	return False

	cursor.close()

'''
def userRegister(owner,user,password):
  db = MySQLdb.connect(host="localhost", user="dstruct", passwd="Blah270", db="bot")
    cursor = db.cursor()
	  sqlquery = "SELECT * FROM auth WHERE user='"+owner+"' and identified='yes' and access_level='owner'"
	    cursor.execute(sqlquery)
		  result = cursor.fetchone()

		    if(str(result) != "None"):
			    sqlquery = "INSERT INTO auth (user,password,identified,access_level) VALUES ('"+user+"','"+password+"','no','admin')"
				    cursor.execute(sqlquery)
					  else:
					      s.send("PRIVMSG %s :%s" % (owner,"You are not authorized to execute that command, please identify."))
'''
