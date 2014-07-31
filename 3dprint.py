import subprocess
import getpass
import sys
from collections import namedtuple
import datetime

def main():
	user = readCard()
	print("User: " + user.id + " " + user.name + " " + user.surname)
	logUser(user)
	#Execute printer software
	if user:
		printer = subprocess.Popen(["C:\Program Files\PolyPrinter\Pronterface\pronterface.exe", "-a"], close_fds=True)
		slicer = subprocess.Popen(["C:\Program Files\PolyPrinter\KISSlicer\KISSlicer64.exe"], close_fds=True)
	
		
def readCard():
	swipe = getpass.getpass("Please swipe your ID.")

	track1begin = 0
	track1end   = 0
	track2begin = 0
	track2end   = 0
	track3begin = 0
	track3end   = 0

	for ch in range(len(swipe)):
		if swipe[ch] == '%':
			track1begin = ch + 1
		elif swipe[ch] == ';':
			track2begin = ch + 1
		elif swipe[ch] == '+':
			track3begin = ch + 1
		if swipe[ch] == '?':
			if track1end == 0 and track1begin != 0:
				track1end = ch
			elif track2end == 0 and track2begin != 0:
				track2end = ch
			elif track3end == 0 and track3begin != 0:
				track3end = ch
				
	track1 = swipe[track1begin:track1end]
	track2 = swipe[track2begin:track2end]
	track3 = swipe[track3begin:track3end]
	if not (track1 or track2 or track3):
		print("Read Error")
		sys.exit()
	_userid = 0
	_name = ""
	_surname = ""
	#check card edition
	if not track3:
		_userid = track2[len(track2)-8:len(track2)+2]
	else:
		list = track3.split("=")
		_userid = list[0]
		_surname = list[1]
		_name = list[2]
		check = track2[len(track2)-8:len(track2)+2]
		#double check id number
		if _userid != check:
			print("Card Error")
			sys.exit()
	#Uncomment for Debug info
	#print("Track 1: " + track1 + "\n")
	#print("Track 2: " + track2 + "\n")
	#print("Track 3: " + track3 + "\n")
	#print("Name   : " + _name + " " + _surname)
	#print("UserID : " + _userid)

	User = namedtuple('User', ['name', 'surname', 'id'], verbose=False)
	User.name = _name
	User.surname = _surname
	User.id = _userid
	return User

def logUser(user):
	logfile = open("C:\Program Files\PolyPrinter\Logs\logs.txt", 'a')
	time = datetime.datetime.now()
	timestamp = time.strftime("%m/%d/%Y %H:%M:%S")
	logfile.write(timestamp + " " + user.id + " " + user.surname + " " + user.name)
	logfile.close()
	#This function would write the user to a text file
	
main()


#New ID format
#%0000000000000000000000000?;00000000000000000=00000000000?+00000000=LAST=FIRST=STATUS?

#Old ID
#;0000000000000000=000000000000?


