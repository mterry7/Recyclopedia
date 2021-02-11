import tkinter as tk
from functools import partial

import itemList

'''
TODO NEXT: favoritesView, and saving favorites between sessions
'''

class RecyclopediaViewer:
	def __init__(self):
		self.home = tk.Tk()			# home window
		self.favorites = None 		# favorites window
		self.results = None			# results window
		self.recents = None			# recents window

		self.favList = []

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

	def resultsView(self, searchBtn):
		self.results = tk.Toplevel()
		res = self.results

		res.title("Recyclopedia - Search")

		res.geometry('800x600+250+150') # width x height + x_offset + y_offset
		res.minsize(600, 600)

		searchQuery = searchBtn.get()

		items = itemList.items

		rowCtr = 0
		for item in items.keys():
			if(searchQuery in item):
				if items[item][0] == "r":			#recyclable
					itemLabel = tk.Label(res, relief="solid", width=10, text=f'{item}')
					itemLabel.grid(column=0, row=rowCtr)

					descLabel = tk.Label(res, relief="solid", width=20, text=f'{items[item][1]}')
					descLabel.grid(column=1, row=rowCtr)

					addFavButton = tk.Button(res, text="Add to Favorites", command=partial(self.addToFavorites, item)) 	#button to add to the favorites list
					addFavButton.grid(column=2, row=rowCtr)

					removeFavButton = tk.Button(res, text="Remove from Favorites", command=partial(self.removeFromFavorites, item)) #button to remove from favorites list
					removeFavButton.grid(column=3, row=rowCtr)
				rowCtr += 1

		res.update()

	def addToFavorites(self, itemName):
		if itemName not in self.favList:
			self.favList.append(itemName)
		print(self.favList)

	def removeFromFavorites(self, itemName):
		if itemName in self.favList:
			self.favList.remove(itemName)
		print(self.favList)
