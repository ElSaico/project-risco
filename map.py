from pygraph.classes.graph import graph

territories  = ["Portugal","Spain","France","Germany","Belgium","Netherlands","Italy"]

class Map:
	def __init__(self):
		self.map = graph()
		gr.add_nodes(territories)
		#just an example:
		gr.add_edge(("Portugal","Spain"))