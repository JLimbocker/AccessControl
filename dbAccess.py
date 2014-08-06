import datetime
import mysql.connector

class dbController:

	dbConfig = {
		'user' :'labtdba',
		'password' : 'LabT6546',
		'host': 'engrwww1.seas.smu.edu',
		'database' : 'labtrackdb',
	}
	def __init__(self):
		
		self.connected = False

	def connect():
		try:
			cnx = mysql.connector.connect(**dbConfig)

		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exists")
			else:
				print(err)

		else:
			self.connected = True

	def isConnected():
		return self.connected

	def isAllowed(student_id, f_name, l_name, tool_id):
		cursor = cnx.cursor()
		 

		query = ("SELECT fname, lname FROM users WHERE id_number = %d AND verified = 1")
		cursor.execute(query, student_id)
		if cursor.rowCount == 0:
			return False
		elif cursor.rowCount > 1:
			return False
		elif cursor.rowCount == 1 and hasTraining(student_id, tool_id):
			return True
		else:
			return False

	def hasTraining(student_id, tool_id):
		cursor = cnx.cursor()

		query = ("SELECT fname, lname FROM users JOIN allowed_tools WHERE tool_id = %d AND id_number = %d")
		cursor.execute(query, (tool_id, student_id))
		if cursor.rowCount == 0:
			return False
		elif cursor.rowCount > 1:
			return False
		else:
			return True

	def getUserInfo(student_id):
		userInfo = namedtuple('user_id', 'fname', 'lname', 'email', 'hash', 'salt', 'id_number', 'grade_level', 'interests', 'balance', 'user_type', 'verified')

		cursor = cns.cursor()

		query = ("SELECT 'user_id', 'fname', 'lname', 'email', 'hash', 'salt', 'id_number', 'grade_level', 'interests', 'balance', 'user_type', 'verified' FROM users WHERE id_number = %d")
		cursor.execute(query, student_id)
		if cursor.rowCount == 1:
			return map(userInfo._make, cursor.fetchall()):





