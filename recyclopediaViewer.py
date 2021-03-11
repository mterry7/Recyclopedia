import tkinter as tk
from functools import partial

import itemList

import pymongo

client = pymongo.MongoClient("mongodb+srv://mterry7:<PASSWORD>@cluster0.mypbz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.recyclopedia

itemsCol = db.items
favCol = db.favorites
recentCol = db.recents

class RecyclopediaViewer:
	def __init__(self):
		self.home = tk.Tk()			# home window
		self.favorites = None 		# favorites window
		self.results = None			# results window
		self.recents = None			# recents window
		self.addItem = None

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
		favoritesButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally

		addItemButton = tk.Button(home, text='Add Item', command=self.addItemView)
		addItemButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally

		recentsButton = tk.Button(home, text='Recents', command=self.recentsView)
		recentsButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally
		
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

		favDict = self.getFavorites()
		maxName = self.getMaxName(favDict)		# getting max name so we can have uniform cells

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

	def addItemView(self):
		self.addItem = tk.Toplevel()
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

		recentDict = self.getRecents()
		maxName = self.getMaxName(recentDict)		# getting max name so we can have uniform cells\

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

			addFavButton = tk.Button(rec, text="Add to Favorites", command=partial(self.addToFavorites, item)) 	#button to add to the favorites list
			addFavButton.grid(column=2, row=rowCtr)

			removeFavButton = tk.Button(rec, text="Remove from Favorites", command=partial(self.removeFromFavorites, item)) #button to remove from favorites list
			removeFavButton.grid(column=3, row=rowCtr)

			rowCtr = rowCtr + 1

	def resultsView(self, searchEntry):
		self.results = tk.Toplevel()
		res = self.results

		res.title("Recyclopedia - Search")

		res.geometry('800x600+250+150') # width x height + x_offset + y_offset
		res.minsize(600, 600)

		searchQuery = searchEntry.get()

		results = self.getSearchResults(searchQuery)
		maxName = self.getMaxName(results)		# getting max name so we can have uniform cells

		rowCtr = 0
		for item in results.keys():
			recentDict = self.getRecents()

			if len(recentDict) < 20 and (item not in recentDict.keys()):
				self.addToRecents(item)
			elif len(recentDict) >= 20:
				self.manageRecents(len(recentDict))

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
		if(favCol.find_one({"item" : itemName}) == None):
			entry = itemsCol.find_one({"item": itemName})
			favCol.insert_one(entry)

	def addToRecents(self, itemName):
		if(recentCol.find_one({"item" : itemName}) == None):
			entry = itemsCol.find_one({"item": itemName})
			recentCol.insert_one(entry)

	def removeFromFavorites(self, itemName):
		entry = favCol.find_one({"item" : itemName})
		if(entry != None):
			favCol.delete_one(entry)

	def getMaxName(self, collection):
		high = 0
		for key in collection.keys():
			if len(key) > high:
				high = len(key)
		return high

	def getFavorites(self):
		favDict = {}
		for doc in favCol.find({}):
			item_name = doc["item"]
			favDict[item_name] = [doc["disposal"], doc["instr"]]
		return favDict

	def getRecents(self):
		recentDict = {}
		for doc in recentCol.find({}):
			item_name = doc["item"]
			recentDict[item_name] = [doc["disposal"], doc["instr"]]
		return recentDict

	def getSearchResults(self, searchQuery):
		if len(searchQuery) == 0:
			return {}

		resDict = {}
		for doc in itemsCol.find({"item" : {"$regex": f"^.*{searchQuery}.*$"}}):
			item_name = doc["item"]
			resDict[item_name] = [doc["disposal"], doc["instr"]]

		return resDict

	def manageRecents(self, numberEntries):
		recents_rev = reversed(self.getRecents().keys())
		ctr = 0
		while numberEntries > 20:
			entry = itemsCol.find_one({"item": recents_rev[ctr]})
			recentCol.delete_one(entry)
			ctr += 1
			numberEntries -= 1

	def addItemToDatabase(self, entryInfo):
		item = entryInfo[0].get().lower()
		disposal = entryInfo[1].get()[0].lower()
		instr = entryInfo[2].get()

		disposalCheck = disposal == "r" or disposal == "t" or disposal == "c"

		if(itemsCol.find_one({"item": item}) == None and disposalCheck == True and len(item) > 2):
			entry = {"item": item, "disposal": disposal, "instr": instr}
			itemsCol.insert_one(entry)
			self.addItem.destroy()