import tkinter as tk
from functools import partial

import pymongo

import favoritesViewer
import recentsViewer
import resultsViewer
import addItemViewer

client = pymongo.MongoClient("mongodb+srv://mterry7:<PASSWORD>@cluster0.mypbz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.recyclopedia

itemsCol = db.items
favCol = db.favorites
recentsCol = db.recents

class HomeViewer:
	def __init__(self):
		self.home = tk.Tk()			# home window
		self.favorites = favoritesViewer.FavoritesViewer(self.home, favCol, itemsCol) 		# favorites window
		self.recents = recentsViewer.RecentsViewer(self.home, self.favorites, itemsCol, recentsCol)			# recents window
		self.results = resultsViewer.ResultsViewer(self.home, self.favorites, self.recents, itemsCol)			# results window
		self.addItem = addItemViewer.AddItemViewer(self.home, itemsCol)

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
		searchBarBtn = tk.Button(home, text="Search", command=partial(self.results.resultsView, searchBarEntry))
		searchBarBtn.place(x=300, y=0)
		
		# Create buttons:
		favoritesButton = tk.Button(home, text='Favorite Items', command=self.favorites.favoritesView)
		favoritesButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally

		addItemButton = tk.Button(home, text='Add Item', command=self.addItem.addItemView)
		addItemButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally

		recentsButton = tk.Button(home, text='Recents', command=self.recents.recentsView)
		recentsButton.pack(padx=30, pady=30, side=tk.LEFT) # Place buttons side by side horizontally
		
		# Start screen:
		home.mainloop() # This window always exists, once closed the application will exit out of this loop

		return