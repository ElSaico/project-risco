#!/usr/bin/env python
# coding=utf-8
from map import Map
from Tkinter import *
import tkFileDialog, tkMessageBox, tkSimpleDialog

class pyWar:
	def __init__(self, master):
		self.root = master
		self.root.title("pyWar")
		
		self.file = Menubutton(self.root, text="File")
		self.file.pack(anchor=W)
		self.file.menu = Menu(self.file, tearoff=0)
		self.file["menu"] = self.file.menu
		self.file.menu.add_command(label="Import map", command=self.importMap)
		self.file.menu.add_command(label="Export map", command=self.exportMap)
		self.file.menu.add_separator()
		self.file.menu.add_command(label="Exit", command=self.exit)
		
		self.country = LabelFrame(self.root, text="Countries")
		self.countries = StringVar(self.root)
		self.lstCountry = Listbox(self.country, listvariable=self.countries)
		self.lstCountry.bind("<ButtonRelease-1>", self.updateNeighbors)
		self.lstCountry.bind("<KeyRelease-Up>", self.updateNeighbors)
		self.lstCountry.bind("<KeyRelease-Down>", self.updateNeighbors)
		self.lstCountry.pack(side=LEFT, expand=YES, fill=BOTH)
		self.scrCountry = Scrollbar(self.country, orient=VERTICAL)
		self.scrCountry.pack(side=LEFT, fill=Y)
		self.lstCountry["yscrollcommand"] = self.scrCountry.set
		self.scrCountry["command"] = self.lstCountry.yview
		self.country.pack(side=LEFT, fill=BOTH, padx="5m", pady="5m")
		
		self.neighbor = LabelFrame(self.root, text="Neighbors")
		self.neighbors = StringVar(self.root)
		self.lstNeighbor = Listbox(self.neighbor, listvariable=self.neighbors)
		self.lstNeighbor.pack(side=LEFT, expand=YES, fill=BOTH)
		self.scrNeighbor = Scrollbar(self.neighbor, orient=VERTICAL)
		self.scrNeighbor.pack(side=LEFT, fill=Y)
		self.lstNeighbor["yscrollcommand"] = self.scrNeighbor.set
		self.scrNeighbor["command"] = self.lstNeighbor.yview
		self.neighbor.pack(side=RIGHT, fill=BOTH, padx="5m", pady="5m")
	
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
	
	def exit(self):
		pass

if __name__ == '__main__':
	root = Tk()
	prog = pyWar(root)
	root.mainloop()
