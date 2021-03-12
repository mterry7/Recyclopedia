def getMaxName(collection):
	high = 0
	for key in collection.keys():
		if len(key) > high:
			high = len(key)
	return high