from json import dumps, loads
from pygraph.classes.hypergraph import hypergraph

def write_map(hgr): # insecure; look at the eval down there
	gr = {"continents": [], "borders": []}
	
	for edge in hgr.hyperedges():
		if edge[:2] == "('" and edge[-2:] == "')": # simple edge / border
			gr["borders"].append(eval(edge))
		else: # hyperedge / continent
			gr["continents"].append({"name": edge,
			                        "bonus": hgr.get_edge_properties(edge)["bonus"],
			                    "countries": hgr.links(edge)})
	
	return dumps(gr, indent=4)

def read_map(string):
	hgr = hypergraph()
	
	doc = loads(string)
	for continent in doc["continents"]:
		hgr.add_hyperedge(continent["name"])
		hgr.set_edge_properties(continent["name"], bonus=continent["bonus"])
		for country in continent["countries"]:
			hgr.add_node(country)
			hgr.link(country, continent["name"])
	hgr.add_edges(map(tuple, doc["borders"]))
	return hgr
