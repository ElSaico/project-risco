#!/usr/bin/env python
# coding=utf-8
from map import Map
from Tix import *
import tkFileDialog, tkMessageBox, tkSimpleDialog

class pyWar:
	def __init__(self, master):
		master.title("pyWar")
		
		self.file = Menubutton(master, text="File")
		self.file.pack(anchor=W)
		self.file.menu = Menu(self.file, tearoff=0)
		self.file["menu"] = self.file.menu
		self.file.menu.add_command(label="Import map", command=self.importMap)
		self.file.menu.add_command(label="Export map", command=self.exportMap)
		self.file.menu.add_separator()
		self.file.menu.add_command(label="Exit", command=self.exit)
				
		self.country = LabelFrame(master, label="Countries")
		self.lstCountry = HList(self.country.frame)
		self.lstCountry.pack(side=LEFT, expand=YES, fill=BOTH)
		self.scrCountry = Scrollbar(self.country.frame, orient=VERTICAL)
		self.scrCountry.pack(side=LEFT, fill=Y)
		self.lstCountry["yscrollcommand"] = self.scrCountry.set
		self.scrCountry["command"] = self.lstCountry.yview
		self.country.pack(side=LEFT, fill=BOTH, padx="5m", pady="5m")
		self.country.config(background="#EEEEEE")
		
		self.neighbor = LabelFrame(master, label="Neighbors")
		self.lstNeighbor = Listbox(self.neighbor.frame)
		self.lstNeighbor.pack(side=LEFT, expand=YES, fill=BOTH)
		self.scrNeighbor = Scrollbar(self.neighbor.frame, orient=VERTICAL)
		self.scrNeighbor.pack(side=LEFT, fill=Y)
		self.lstNeighbor["yscrollcommand"] = self.scrNeighbor.set
		self.scrNeighbor["command"] = self.lstNeighbor.yview
		self.neighbor.pack(side=RIGHT, fill=BOTH, padx="5m", pady="5m")
		self.neighbor.config(background="#EEEEEE")
	
	def importMap(self):
		pass
	
	def exportMap(self):
		pass
	
	def exit(self):
		pass

if __name__ == '__main__':
	root = Tk()
	prog = pyWar(root)
	root.mainloop()
