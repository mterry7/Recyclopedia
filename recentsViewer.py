import pymongo
import tkinter as tk
from functools import partial

import commonFuncs

import favoritesViewer

class RecentsViewer:
	def __init__(self, root, favorites, itemsCol, recentsCol):
		self.root = root
		self.recents = None
		self.favorites = favorites
		self.itemsCol = itemsCol
		self.recentsCol = recentsCol

	def recentsView(self):
		'''
		None -> None
		Creates the view for the recents window
		'''
		self.recents = tk.Toplevel(self.root)
		rec = self.recents

		rec.title("Recyclopedia - Recents")

		rec.geometry('800x600+250+150') # width x height + x_offset + y_offset
		rec.minsize(600, 600)

		recentDict = self.getRecents()
		maxName = commonFuncs.getMaxName(recentDict)		# getting max name so we can have uniform cells\

		rowCtr = 0
		for item in reversed(recentDict):
			color = "white"
			if(recentDict[item][0] == "r"):
				color = "dodger blue"
			elif(recentDict[item][0] == "c"):
				color = "lime green"
			elif(recentDict[item][0] == "t"):
				color = "saddle brown"

			itemLabel = tk.Label(rec, relief="solid", width=maxName, bg=color, text=f'{item}')
			itemLabel.grid(column=0, row=rowCtr)

			descLabel = tk.Label(rec, relief="solid", width=20, bg=color, text=f'{recentDict[item][1]}')
			descLabel.grid(column=1, row=rowCtr)

			addFavButton = tk.Button(rec, text="Add to Favorites", command=partial(self.favorites.addToFavorites, item)) 	#button to add to the favorites list
			addFavButton.grid(column=2, row=rowCtr)

			removeFavButton = tk.Button(rec, text="Remove from Favorites", command=partial(self.favorites.removeFromFavorites, item)) #button to remove from favorites list
			removeFavButton.grid(column=3, row=rowCtr)

			rowCtr = rowCtr + 1	

	def addToRecents(self, itemName):
		if(self.recentsCol.find_one({"item" : itemName}) == None):
			entry = self.itemsCol.find_one({"item": itemName})
			self.recentsCol.insert_one(entry)

	def getRecents(self):
		recentDict = {}
		for doc in self.recentsCol.find({}):
			item_name = doc["item"]
			recentDict[item_name] = [doc["disposal"], doc["instr"]]
		return recentDict

	def manageRecents(self, numberEntries):
		recents_rev = reversed(self.getRecents().keys())
		ctr = 0
		while numberEntries > 20:
			entry = self.itemsCol.find_one({"item": recents_rev[ctr]})
			self.recentsCol.delete_one(entry)
			ctr += 1
			numberEntries -= 1