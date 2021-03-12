import pymongo
import tkinter as tk
from functools import partial

import commonFuncs

class ResultsViewer:
	def __init__(self, root, favorites, recents, itemsCol):
		self.root = root
		self.results = None
		self.favorites = favorites
		self.recents = recents
		self.itemsCol = itemsCol

	def resultsView(self, searchEntry):
		self.results = tk.Toplevel(self.root)
		res = self.results

		res.title("Recyclopedia - Search")

		res.geometry('800x600+250+150') # width x height + x_offset + y_offset
		res.minsize(600, 600)

		searchQuery = searchEntry.get()

		results = self.getSearchResults(searchQuery)
		maxName = commonFuncs.getMaxName(results)		# getting max name so we can have uniform cells

		rowCtr = 0
		for item in results.keys():
			recentDict = self.recents.getRecents()

			if len(recentDict) < 20 and (item not in recentDict.keys()):
				self.recents.addToRecents(item)
			elif len(recentDict) >= 20:
				self.recents.manageRecents(len(recentDict))

			color = "white"
			if(results[item][0] == "r"):
				color = "dodger blue"
			elif(results[item][0] == "c"):
				color = "lime green"
			elif(results[item][0] == "t"):
				color = "saddle brown"

			itemLabel = tk.Label(res, relief="solid", width=maxName, bg=color, text=f'{item}')
			itemLabel.grid(column=0, row=rowCtr)

			descLabel = tk.Label(res, relief="solid", width=20, bg=color, text=f'{results[item][1]}')
			descLabel.grid(column=1, row=rowCtr)

			addFavButton = tk.Button(res, text="Add to Favorites", command=partial(self.favorites.addToFavorites, item)) 	#button to add to the favorites list
			addFavButton.grid(column=2, row=rowCtr)

			removeFavButton = tk.Button(res, text="Remove from Favorites", command=partial(self.favorites.removeFromFavorites, item)) #button to remove from favorites list
			removeFavButton.grid(column=3, row=rowCtr)

			rowCtr += 1

		res.update()

	def getSearchResults(self, searchQuery):
		if len(searchQuery) == 0:
			return {}

		resDict = {}
		for doc in self.itemsCol.find({"item" : {"$regex": f"^.*{searchQuery}.*$"}}):
			item_name = doc["item"]
			resDict[item_name] = [doc["disposal"], doc["instr"]]

		return resDict