import pymongo
import tkinter as tk
from functools import partial

import commonFuncs

class FavoritesViewer:
	def __init__(self, root, favCol, itemsCol):
		self.favorites = None
		self.root = root
		self.favCol = favCol
		self.itemsCol = itemsCol

	def favoritesView(self):
			'''
			None -> None
			Creates the view for the favorites window
			'''
			self.favorites = tk.Toplevel(self.root)

			fav = self.favorites

			fav.title("Recyclopedia - Favorites")

			fav.geometry('800x600+250+150') # width x height + x_offset + y_offset
			fav.minsize(600, 600)

			favDict = self.getFavorites()
			maxName = commonFuncs.getMaxName(favDict)		# getting max name so we can have uniform cells

			rowCtr = 0
			for item in favDict.keys():
				color = "white"
				if(favDict[item][0] == "r"):
					color = "dodger blue"
				elif(favDict[item][0] == "c"):
					color = "lime green"
				elif(favDict[item][0] == "t"):
					color = "saddle brown"

				itemLabel = tk.Label(fav, relief="solid", width=maxName, bg=color, text=f'{item}')
				itemLabel.grid(column=0, row=rowCtr)

				descLabel = tk.Label(fav, relief="solid", width=20, bg=color, text=f'{favDict[item][1]}')
				descLabel.grid(column=1, row=rowCtr)

				removeFavButton = tk.Button(fav, text="Remove from Favorites", command=partial(self.removeFromFavorites, item)) #button to remove from favorites list
				removeFavButton.grid(column=2, row=rowCtr)

				rowCtr = rowCtr + 1

	def addToFavorites(self, itemName):
		if(self.favCol.find_one({"item" : itemName}) == None):
			entry = self.itemsCol.find_one({"item": itemName})
			self.favCol.insert_one(entry)

	def removeFromFavorites(self, itemName):
		entry = self.favCol.find_one({"item" : itemName})
		if(entry != None):
			self.favCol.delete_one(entry)

	def getFavorites(self):
		favDict = {}
		for doc in self.favCol.find({}):
			item_name = doc["item"]
			favDict[item_name] = [doc["disposal"], doc["instr"]]
		return favDict