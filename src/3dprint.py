import subprocess
import getpass
import sys
from collections import namedtuple
import datetime
#import dbAccess

def main():
	while(True):
		user = readCard()

		#Execute printer software if user exists
		if user is not "":
		#open connection to DB and check if they are allowed to use this device
			#openDB()
			#if dbCon.isConnected():
			#	allowed = dbCon.isAllowed(user.id, user.name, user.surname, tool_id) #tool_id is the id associated with the specific tool in the DB. Expected hardcode for each tool (laser, cnc ect.)
			#if allowed:
			print("User: " + user.id + " " + user.name + " " + user.surname)
			logUser(user)
			slicer = subprocess.Popen(["C:\Program Files\PolyPrinter\KISSlicer\KISSlicer64.exe"])
			printer = subprocess.Popen(["python", "C:\Users\install\Documents\GitHub\Printrun\pronterface.py"], shell = False, stdin = None, stdout = subprocess.PIPE, stderr = None)

			print "still going"


			#Debug loop becasue the for loop below wasn't working and hates us
			while printer.poll() is None:
				print "in loop"
				printer.stdout.flush()
				line = printer.stdout.readline()
				print "read stuff"
				if not line:
					print "jk read nothing"
					break
				print ">>> " + line.rstrip()

			#Should work but doesn't print realtime
#			for line in iter(printer.stdout.readline, b""):
#				if "duration" in output.readline():
#					printer.kill()
#					print "Closed"

#def openDB():
#	dbCon = dbAccess()
#	dbCon.connect()

def logUser(user):
	logfile = open("C:\Program Files\PolyPrinter\Logs\logs.txt", 'a')
	time = datetime.datetime.now()
	timestamp = time.strftime("%m/%d/%Y %H:%M:%S")
	logfile.write("\n" + timestamp + " " + user.id + " " + user.surname + " " + user.name + " ")
	logfile.close()
	#This function would write the user to a text file

main()


#New ID format
#%0000000000000000000000000?;00000000000000000=00000000000?+00000000=LAST=FIRST=STATUS?

#Old ID
#;0000000000000000=000000000000?
