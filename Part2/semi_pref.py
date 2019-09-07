import random
import math
import networkx as nx
from weighted_choice import *
from networkx.generators.classic import empty_graph, path_graph, complete_graph

"""
barabasi_albert_graph, but returns a directed graph.
Unfortunately, m=1 and cannot be changed.
"""
def gn_semi_preferential(n, pref_coefficient=None, create_using=None, seed=None):
	"""Return the GN digraph with n nodes.

	The GN (growing network) graph is built by adding nodes one at a time with
	a link to one previously added node.

	The graph is always a (directed) tree.

	Parameters
	----------
	n : int
		The number of nodes for the generated graph.
	pref_coefficient : float between 0 and 1, determining how much
		an edge choice depends on prior popularity (in-degree)
	create_using : graph, optional (default DiGraph)
		Return graph of this type. The instance will be cleared.
	seed : hashable object, optional
	The seed for the random number generator.
	"""
	
	# r = random.random()
	# This kernel sometimes chooses randomly
	# and sometimes bandwagons.
	# It bandwagons with probability = pref_coefficient.
	# x-1 is the in-degree
	kernel = lambda x: (pref_coefficient * (x-1)) + (1 - pref_coefficient)
	
	# Another kernel to try
	# kernel = lambda x: x**pref_coefficient
	G = nx.gn_graph(n, kernel, create_using, seed)
	return G


"""
Failed attempt to reimplement barabasi_albert_graph entirely
"""
def barabasi_albert_graph2(n, m, pref, seed=None):
	"""Return random graph using preferential attachment model.
		
	A graph of n nodes is grown by attaching new nodes each with m
	edges that are preferentially attached to existing nodes with high
	degree.
	
	Parameters
	----------
	n : int
		Number of nodes
	m : int
		Number of edges to attach from a new node to existing nodes
	pref : float between 0 and 1, determining how much
		an edge choice depends on prior popularity (in-degree)
	seed : int, optional
		Seed for random number generator (default=None).   

	Returns
	-------
	G : Graph
		
	Notes
	-----
	The initialization is a graph with with m nodes and no edges.
	"""
	
	if m < 1 or  m >=n:
		raise nx.NetworkXError(\
			  "Barabasi-Albert network must have m>=1 and m<n, m=%d,n=%d"%(m,n))
	if seed is not None:
		random.seed(seed)    

	# Add m initial nodes (m0 in barabasi-speak) 
	G=empty_graph(m)
	G.name="barabasi_albert_graph(%s,%s)"%(n,m)
	nodes = G.nodes()
	
	base_weight = (1 - pref) 
	edge_weight = pref
	
	weights =  [base_weight]*len(nodes)
	chooser = semi_static_weighted_choice(nodes, weights)
	"""
	# Target nodes for new edges
	targets=list(range(m))
	# List of existing nodes, with nodes repeated once for each adjacent edge 
	repeated_nodes=[]     
	"""
	# Start adding the other n-m nodes. The first node is m.
	newNodeIndex=m
	while newNodeIndex < n:
		targets = []
		for i in range(m):
			chosenIndex, chosen = chooser.getRandomItem()
			targets.append(chosen)
			chooser.changeWeight(chosenIndex, edge_weight)
		chooser.addItem(newNodeIndex, base_weight)
		
		# Add edges to m nodes from the source.
		G.add_edges_from(zip([newNodeIndex]*m,targets)) 
	return G