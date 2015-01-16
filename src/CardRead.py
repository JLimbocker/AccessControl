import LabTrak
import datetime
import getpass
from collections import namedtuple

class LabTrakCardReader:
    db = LabTrak()
    db.connect()

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
    		raise ReadError()

        return (track1, track2, track3)

    def generateUser(track1, track2, track3, debug=False):
        _userid = 0
    	_name = ""
    	_surname = ""

    	#Check card edition
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
    			raise VerificationError(_userid, check)

    	if debug:
        	print("Track 1: " + track1 + "\n")
        	print("Track 2: " + track2 + "\n")
        	print("Track 3: " + track3 + "\n")
        	print("Name   : " + _name + " " + _surname + "\n")
        	print("UserID : " + _userid)

    	User = namedtuple('User', ['name', 'surname', 'id'], verbose=False)
    	User.name = _name
    	User.surname = _surname
    	User.id = _userid
    	return User

    def allowed(user, tool_id):
        return (not (db.connected())) ? False : db.allowed(user.id, user.name, user.surname, tool_id)

    def hasToolTraining(user, tool_id):
        return (not (db.connected())) ? False : db.hasToolTraining(user.id, tool_id)

    def getUserInfo(user):
        return (not (db.connected())) ? False : db.getUserInfo(user.id)

#Exception Classes

#Base class: CardError
class CardError(Exception):
    pass

#Child classes

#ReadError: Raised when the card information is incomplete.
class ReadError(CardError):
    def __str__(self):
        return "Read Error: Could not read card, please try again."

#VerificationError: Raised when the card information is duplicated or does not
#match the given check string.
class VerificationError(CardError):
    def __init__(self, userID, check):
        self.userID = userID
        self.check = check

    def __str__(self):
        return "Verification Error: Card information did not match\n" +
        "User ID: " + self.userID + "\n" +
        "Check: " + self.check + "\n"
