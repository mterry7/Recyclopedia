import pymongo
import tkinter as tk
from functools import partial

import commonFuncs

class AddItemViewer:
	def __init__(self, root, itemsCol):
		self.root = root
		self.addItem = None
		self.itemsCol = itemsCol

	def addItemView(self):
		self.addItem = tk.Toplevel(self.root)
		add = self.addItem

		add.title("Recyclopedia - Add Item")

		add.geometry('300x100+125+75') # width x height + x_offset + y_offset
		add.minsize(250, 100)

		itemLabel = tk.Label(add, text="Item Name: ")
		itemLabel.grid(column = 0, row = 0)
		itemEntry = tk.Entry(add)
		itemEntry.grid(column = 1, row=0)

		disposalLabel = tk.Label(add, text="Disposal Method (T/C/R): ")
		disposalLabel.grid(column = 0, row = 1)
		disposalEntry = tk.Entry(add)
		disposalEntry.grid(column = 1, row=1)

		instrLabel = tk.Label(add, text="Instructions for Disposal: ")
		instrLabel.grid(column = 0, row = 2)
		instrEntry = tk.Entry(add)
		instrEntry.grid(column = 1, row=2)

		addItemButton = tk.Button(add, text="Add Item", command=partial(self.addItemToDatabase, [itemEntry, disposalEntry, instrEntry]))
		addItemButton.grid(column = 1, row=3)


	def addItemToDatabase(self, entryInfo):
		item = entryInfo[0].get().lower()
		disposal = entryInfo[1].get()[0].lower()
		instr = entryInfo[2].get()

		disposalCheck = disposal == "r" or disposal == "t" or disposal == "c"

		if(self.itemsCol.find_one({"item": item}) == None and disposalCheck == True and len(item) > 2):
			entry = {"item": item, "disposal": disposal, "instr": instr}
			self.itemsCol.insert_one(entry)
			self.addItem.destroy()