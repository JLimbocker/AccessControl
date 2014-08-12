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

	def getItems():
		itemDict = {}
		Item = namedtuple('Item', 'name slot cost quantity')
		cursor = cns.cursor()
		query = ("SELECT name, slot, cost, quantity FROM Vending_Machine")
		for row in cursor.execute(query):
			itemDict[row.slot] = Item(row.name, row.slot, row.cost, row.quantity)
		return itemDict

	def setItems():
		cursor = cns.cursor()
		#query = 

	def setItemBySlot(slot, name, cost, quantity):
		cursor = cns.cursor()
		#Use Transaction for Safety
		cnx.start_transaction()
		query = ("SELECT name FROM Vending_Machine WHERE slot = %d)")
		cursor.execute(query, slot)
		if cursor.rowCount is 1:
			query = ("DELETE FROM Vending_Machine WHERE slot = %d")
			cursor.execute(query, slot)

		query = ("INSERT INTO Vending_Machine (slot, name, cost, quantity) VALUES (%d, %s, %d, %d)")
		cursor.execute(query, (slot, name, cost, quantity))
		cns.commit()
		#End Transaction

	def logTransaction(user_id):
		cursor = cns.cursor()
		now = datetime.datetime.now()
		now.strftime('%Y-%m-%d %H:%M:%S')

		cnx.start_transaction()
		query = ("INSERT INTO transactions (user_id, time_stamp) VALUES (%d, %s)")
		cursor.execute(query, (user_id, now))
		cnx.commit()
		






