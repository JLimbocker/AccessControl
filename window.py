import wx
import time
import getpass
import sys
from collections import namedtuple

class VendingMachine(wx.Frame):
	# swipeSizer = wx.BoxSizer(wx.VERTICAL)
	# swipeWin = wx.Frame(None, -1, 'swipeWindow')
	# swipeTextVal = "Please Swipe ID"
	# swipeText = wx.StaticText(swipeWin, -1, swipeTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)

	# itemWin = wx.Frame(None, -1, 'itemWindow')
	# itemSizer = wx.BoxSizer(wx.VERTICAL)
	# welcomeTextVal = "Welcome "
	# welcomeText = wx.StaticText(itemWin, -1, welcomeTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)
	# itemTextVal = "Select an item:"
	# itemText = wx.StaticText(itemWin, -1, welcomeTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)

	def __init__(self, *args, **kw):
		super(VendingMachine, self).__init__(*args, **kw)
		self.initUI()
		self.cardString = ""

	def initUI(self):
		self.swipeSizer = wx.BoxSizer(wx.VERTICAL)
		self.swipeWin = wx.Frame(None, -1, 'swipeWindow')
		self.swipeTextVal = "Please Swipe ID"
		self.swipeText = wx.StaticText(self.swipeWin, -1, self.swipeTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)

		self.itemWin = wx.Frame(None, -1, 'itemWindow')
		self.itemSizer = wx.BoxSizer(wx.VERTICAL)
		self.welcomeTextVal = "Welcome "
		self.welcomeText = wx.StaticText(self.itemWin, -1, self.welcomeTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)
		self.itemTextVal = "Select an item:"
		self.itemText = wx.StaticText(self.itemWin, -1, self.itemTextVal, wx.DefaultPosition, wx.DefaultSize, wx.TEXT_ALIGNMENT_CENTER)
		self.swipeText.SetFont(wx.Font(64, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.swipeSizer.Add(self.swipeText, 1, wx.ALIGN_CENTER_VERTICAL)

		self.swipeWin.SetWindowStyleFlag(wx.BORDER_NONE)
		self.swipeWin.SetSize(wx.Size(1024,768))
		self.swipeWin.CenterOnScreen()
		self.swipeWin.SetSizer(self.swipeSizer)
		self.swipeWin.SetBackgroundColour(wx.Colour(225,80,0))
		
		self.welcomeText.SetFont(wx.Font(64, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		self.itemText.SetFont(wx.Font(48, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

		self.itemSizer.Add(self.welcomeText, 1, wx.ALIGN_CENTER)
		self.itemSizer.Add(self.itemText, 1, wx.ALIGN_CENTER)

		self.itemWin.SetWindowStyleFlag(wx.BORDER_NONE)
		self.itemWin.SetSize(wx.Size(1024,768))
		

		self.itemWin.CenterOnScreen()
		self.itemWin.SetSizer(self.itemSizer)
		self.itemWin.SetBackgroundColour(wx.Colour(255, 80, 0))

	
		
	def promptSwipe(self):
		self.swipeWin.Show()
		self.itemWin.Hide()
		self.swipeWin.Bind(wx.EVT_CHAR, self.OnSwipe)

	def promptItem(self, name):
		self.welcomeTextVal = "Welcome " + name
		self.welcomeText.SetLabel(self.welcomeTextVal)
		self.itemWin.Show()
		self.swipeWin.Hide()

	def readCard(self):
		swipe = self.cardString

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
			return
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
				return
		#Uncomment for Debug info
		#print("Track 1: " + track1 + "\n")
		#print("Track 2: " + track2 + "\n")
		#print("Track 3: " + track3 + "\n")
		#print("Name   : " + _name + " " + _surname)
		#print("UserID : " + _userid)

		self.User = namedtuple('User', ['name', 'surname', 'id'], verbose=False)
		self.User.name = _name
		self.User.surname = _surname
		self.User.id = _userid

		

	def OnSwipe(self, event):
		key = event.GetUnicodeKey()
		
		if key != 13 :
			self.cardString += str(unichr(key))
		else :
			self.readCard()
			self.cardString = ""
			self.User.name = self.User.name[0] + self.User.name[1::].lower()
			
			self.promptItem(self.User.name)


def main():
	app = wx.App()
	vm = VendingMachine(None)
	vm.promptSwipe()
	
	app.MainLoop()

if __name__ == '__main__':
	main()