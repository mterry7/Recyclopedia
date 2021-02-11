import tkinter as tk
from functools import partial

import itemList

'''
TODO NEXT: connect with pymongo
'''

class RecyclopediaViewer:
	def __init__(self):
		self.home = tk.Tk()			# home window
		self.favorites = None 		# favorites window
		self.results = None			# results window
		self.recents = None			# recents window

		self.recentDict = {}

		self.favDict = {}

	def homeView(self):
		'''
		None -> None
		This acts as the main function for the user interface
		This creates the home screen
		'''
		# Setup home window:
		home = self.home
		home.title('Recyclopedia Homepage')
		home.geometry('400x200+200+100') 			# width x height + x_offset + y_offset
		home.minsize(400, 200)

		searchBarLabel = tk.Label(home, text="Please Enter an Item: ")
		searchBarLabel.place(x=40, y=0)
		searchBarEntry = tk.Entry(home)
		searchBarEntry.place(x=170, y=0)
		searchBarBtn = tk.Button(home, text="Search", command=partial(self.resultsView, searchBarEntry))
		searchBarBtn.place(x=300, y=0)
		
		# Create buttons:
		favoritesButton = tk.Button(home, text='Favorite Items', command=self.favoritesView)
		favoritesButton.pack(padx=60, pady=30, side=tk.LEFT) # Place buttons side by side horizontally

		recentsButton = tk.Button(home, text='Recents', command=self.recentsView)
		recentsButton.pack(padx=60, pady=30, side=tk.LEFT) # Place buttons side by side horizontally
		
		# Start screen:
		home.mainloop() # This window always exists, once closed the application will exit out of this loop

		return

	def favoritesView(self):
		'''
		None -> None
		Creates the view for the favorites window
		'''
		self.favorites = tk.Toplevel()
		fav = self.favorites

		fav.title("Recyclopedia - Favorites")

		fav.geometry('800x600+250+150') # width x height + x_offset + y_offset
		fav.minsize(600, 600)

		maxName = self.getMaxName(self.favDict.keys())		# getting max name so we can have uniform cells\

		rowCtr = 0
		for item in self.favDict:
			color = "white"
			if(self.favDict[item][0] == "r"):
				color = "dodger blue"
			elif(self.favDict[item][0] == "c"):
				color = "lime green"
			elif(self.favDict[item][0] == "t"):
				color = "saddle brown"

			itemLabel = tk.Label(fav, relief="solid", width=maxName, bg=color, text=f'{item}')
			itemLabel.grid(column=0, row=rowCtr)

			descLabel = tk.Label(fav, relief="solid", width=20, bg=color, text=f'{self.favDict[item][1]}')
			descLabel.grid(column=1, row=rowCtr)

			removeFavButton = tk.Button(fav, text="Remove from Favorites", command=partial(self.removeFromFavorites, item)) #button to remove from favorites list
			removeFavButton.grid(column=2, row=rowCtr)

			rowCtr = rowCtr + 1


	def recentsView(self):
		'''
		None -> None
		Creates the view for the recents window
		'''
		self.recents = tk.Toplevel()
		rec = self.recents

		rec.title("Recyclopedia - Recents")

		rec.geometry('800x600+250+150') # width x height + x_offset + y_offset
		rec.minsize(600, 600)

		maxName = self.getMaxName(self.recentDict.keys())		# getting max name so we can have uniform cells\

		rowCtr = 0
		for item in reversed(self.recentDict):
			color = "white"
			if(self.recentDict[item][0] == "r"):
				color = "dodger blue"
			elif(self.recentDict[item][0] == "c"):
				color = "lime green"
			elif(self.recentDict[item][0] == "t"):
				color = "saddle brown"

			itemLabel = tk.Label(rec, relief="solid", width=maxName, bg=color, text=f'{item}')
			itemLabel.grid(column=0, row=rowCtr)

			descLabel = tk.Label(rec, relief="solid", width=20, bg=color, text=f'{self.recentDict[item][1]}')
			descLabel.grid(column=1, row=rowCtr)

			rowCtr = rowCtr + 1

	def resultsView(self, searchBtn):
		self.results = tk.Toplevel()
		res = self.results

		res.title("Recyclopedia - Search")

		res.geometry('800x600+250+150') # width x height + x_offset + y_offset
		res.minsize(600, 600)

		searchQuery = searchBtn.get()

		results = self.getSearchResults(searchQuery)
		maxName = self.getMaxName(results.keys())		# getting max name so we can have uniform cells

		rowCtr = 0
		for item in results.keys():

			if len(self.recentDict) < 20 and (item not in self.recentDict.keys()):
				self.recentDict[item] = results[item]
			elif len(self.recentDict) >= 20:
				self.recentDict = {}

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

			addFavButton = tk.Button(res, text="Add to Favorites", command=partial(self.addToFavorites, item)) 	#button to add to the favorites list
			addFavButton.grid(column=2, row=rowCtr)

			removeFavButton = tk.Button(res, text="Remove from Favorites", command=partial(self.removeFromFavorites, item)) #button to remove from favorites list
			removeFavButton.grid(column=3, row=rowCtr)

			rowCtr += 1

		res.update()

	def addToFavorites(self, itemName):
		if itemName not in self.favDict:
			self.favDict[itemName] = itemList.items[itemName]
		print(self.favDict)

	def removeFromFavorites(self, itemName):
		if itemName in self.favDict:
			self.favDict.pop(itemName)
		print(self.favDict)

	def getMaxName(self, nameList):
		high = 0
		for name in nameList:
			if len(name) > high:
				high = len(name)
		return high

	def getSearchResults(self, searchQuery):
		if len(searchQuery) == 0:
			return {}
		items = itemList.items
		resDict = {}
		for item in items.keys():
			if(searchQuery in item):
				resDict[item] = items[item]
		return resDict