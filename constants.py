validColors = ("White", "Black", "Green", "Blue", "Red", "Yellow")
validShapes = ("Circle", "Square", "Triangle")

continents = ["South America", "North America", "Europe", "Asia", "Africa", "Australia"]
countries = {}
countries["Australia"] = ["New Guinea", "Australia", "Borneo", "Sumatra"]
countries["South America"] = ["Brazil", "Argentina", "Peru", "Venezuela"]
countries["North America"] = []
countries["Asia"] = []
countries["Africa"] = []
countries["Europe"] = []

territories  = []
for c in continents:
	territories += countries[c]

debug = True
