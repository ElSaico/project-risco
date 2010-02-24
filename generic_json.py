from json import dumps, loads
from pygraph.classes.hypergraph import hypergraph

def write_hypergraph(hgr):
	gr = {"type": "hypergraph", "nodes": [], "hyperedges": hgr.hyperedges()}
	
	for each_node in hgr.nodes():
		gr["nodes"].append({"id": str(each_node), "links": hgr.links(each_node)})
	
	return dumps(gr, indent=4)

def read_hypergraph(string):
	hgr = hypergraph()
	
	doc = loads(string)
	for each_edge in doc["hyperedges"]:
		hgr.add_hyperedge(each_edge)
	for each_node in doc["nodes"]:
		hgr.add_node(each_node["id"])
		for each_edge in each_node["links"]:
			hgr.link(each_node["id"], each_edge)
	return hgr
