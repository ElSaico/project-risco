#!/usr/bin/env python
# coding=utf-8
from servermap import ServerMap
from Tkinter import *
import tkFileDialog, tkMessageBox, tkSimpleDialog

class TkServer:
	def __init__(self, master):
		self.root = master
		self.root.title("pyWar")
		
		self.file = Menubutton(self.root, text="File")
		self.file.menu = Menu(self.file, tearoff=0)
		self.file["menu"] = self.file.menu
		self.file.menu.add_command(label="Import map", command=self.importMap)
		self.file.menu.add_command(label="Export map", command=self.exportMap)
		self.file.menu.add_separator()
		self.file.menu.add_command(label="Exit", command=self.exit)
		self.file.grid(sticky=W)
		
		self.connections = Frame(self.root)
		
		self.users = LabelFrame(self.connections, text="Online users")
		self.varUsers = StringVar()
		self.lstUsers = Listbox(self.users, listvariable=self.varUsers)
		self.bindList(self.lstUsers, self.updateCards)
		self.lstUsers.grid()
		self.scrUsers = Scrollbar(self.users, orient=VERTICAL)
		self.scrUsers.grid(row=0, column=1, sticky=N+S)
		self.lstUsers["yscrollcommand"] = self.scrUsers.set
		self.scrUsers["command"] = self.lstUsers.yview
		self.users.grid(row=0, sticky=N+S)
		
		self.cards = LabelFrame(self.connections, text="Cards")
		self.varCards = StringVar()
		self.lstCards = Listbox(self.cards, listvariable=self.varCards)
		self.lstCards.grid()
		self.cards.grid(row=1, sticky=S)
		
		self.logs = LabelFrame(self.connections, text="Logs")
		self.varLogs = StringVar()
		self.lblLogs = Label(self.logs, textvariable=self.varLogs, width=80)
		self.lblLogs.grid()
		self.scrLogs = Scrollbar(self.logs, orient=VERTICAL)
		self.scrLogs.grid(row=0, column=1, sticky=N+S)
		#self.lblLogs["yscrollcommand"] = self.scrLogs.set
		#self.scrLogs["command"] = self.lblLogs.yview
		self.logs.grid(row=0, rowspan=2, column=1, sticky=N+S)
		
		self.connections.grid(sticky=S)
	
	def bindList(self, l, f):
		l.bind("<ButtonRelease-1>", f)
		l.bind("<KeyRelease-Up>", f)
		l.bind("<KeyRelease-Down>", f)
	
	def importMap(self):
		mapfile = tkFileDialog.askopenfilename()
		# TODO: add a player selection dialog
		if mapfile:
			self.world = Map(mapfile, ("Black", "White"))
			self.updateList(self.countries, self.world.countries())
	
	def exportMap(self):
		mapfile = tkFileDialog.asksaveasfilename()
		if mapfile:
			with open(mapfile, "w") as m:
				m.write(self.map.json())
	
	def updateList(self, lvar, lst):
		lvar.set(" ".join(map('"{0}"'.format, lst)))
	
	def updateNeighbors(self, e):
		# neighbors[int(val[0])], blah blah blah... 
		print self.lstCountry.curselection()
	
	def updateCards(self, e):
		pass
	
	def exit(self):
		pass

if __name__ == '__main__':
	root = Tk()
	prog = TkServer(root)
	root.mainloop()
