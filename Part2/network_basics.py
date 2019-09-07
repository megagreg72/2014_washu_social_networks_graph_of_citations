import networkx as nx

def log_basics(G):
	print "\n-----------Basics------------\n"

	print "nodes in G: ", G.number_of_nodes()
	print "edges in G: ", G.number_of_edges(), "\n"

	# H = nx.DiGraph(G)
	# print "nodes in H: ", H.number_of_nodes()
	# print "edges in H: ", H.number_of_edges()

	T = nx.DiGraph()
	T.add_edges_from([(1,2),(2,1),(1,3),(1,1)])
	print "T(example graph):\t\t\t", T.edges()
	print "G(Citations):\t", "see Cit-HepPh.txt"
	print "\n----------------------------------------T-------G-------"
	Tnodes = T.number_of_nodes()
	Gnodes = G.number_of_nodes()

	Tedges = T.number_of_edges()
	Gedges = G.number_of_edges()

	Tloops = len(T.nodes_with_selfloops())
	Gloops = len(G.nodes_with_selfloops())

	print "a) nodes in graph:\t\t\t", Tnodes, "\t", Gnodes
	# print "edges in graph:\t\t\t\t", Tedges, "\t", Gedges
	print "b) selfloops in graph:\t\t\t", Tloops, "\t", Gloops
	print "c) directed edges in graph:\t\t", Tedges - Tloops, "\t", Gedges - Gloops


	#undirected version of graphs
	unT = nx.Graph(T)
	unG = nx.Graph(G)

	unTedges = unT.number_of_edges()
	unGedges = unG.number_of_edges()

	print "d) undirected edges in graph:\t\t", unTedges - Tloops, "\t", unGedges - Gloops
	print "e) reciprocated edges in graph:\t\t", Tedges - unTedges, "\t", Gedges - unGedges


	Tout_degree_values = sorted(T.out_degree().values())
	Gout_degree_values = sorted(G.out_degree().values())

	Tin_degree_values = sorted(T.in_degree().values())
	Gin_degree_values = sorted(G.in_degree().values())


	# For getting number of occurrences of one particular indegree or outdegree

	print "f) nodes in graph with out-degree 0:\t", Tout_degree_values.count(0), "\t", Gout_degree_values.count(0)
	print "g) nodes in graph with in-degree 0:\t", Tin_degree_values.count(0), "\t", Gin_degree_values.count(0)

	# The more general solution for getting numbers of occurrences of  indegrees or outdegrees

	from collections import Counter

	big = 50

	Tcounted_out = Counter(Tout_degree_values)
	Tbig_out_keys = [x for x in Tcounted_out if x>big]
	Tbig_out_values = [Tcounted_out.get(x) for x in Tbig_out_keys]
	Tbig_out_sum = sum(Tbig_out_values)
	Tcounted_in = Counter(Tin_degree_values)
	Tbig_in_keys = [x for x in Tcounted_in if x>big]
	Tbig_in_values = [Tcounted_in.get(x) for x in Tbig_in_keys]
	Tbig_in_sum = sum(Tbig_in_values)

	Tcounted_out = Counter(Tout_degree_values)
	Tsmall_out_keys = [x for x in Tcounted_out if x<big]
	Tsmall_out_values = [Tcounted_out.get(x) for x in Tsmall_out_keys]
	Tsmall_out_sum = sum(Tsmall_out_values)
	Tcounted_in = Counter(Tin_degree_values)
	Tsmall_in_keys = [x for x in Tcounted_in if x<big]
	Tsmall_in_values = [Tcounted_in.get(x) for x in Tsmall_in_keys]
	Tsmall_in_sum = sum(Tsmall_in_values)

	Gcounted_out = Counter(Gout_degree_values)
	Gbig_out_keys = [x for x in Gcounted_out if x>big]
	Gbig_out_values = [Gcounted_out.get(x) for x in Gbig_out_keys]
	Gbig_out_sum = sum(Gbig_out_values)
	Gcounted_in = Counter(Gin_degree_values)
	Gbig_in_keys = [x for x in Gcounted_in if x>big]
	Gbig_in_values = [Gcounted_in.get(x) for x in Gbig_in_keys]
	Gbig_in_sum = sum(Gbig_in_values)

	Gcounted_out = Counter(Gout_degree_values)
	Gsmall_out_keys = [x for x in Gcounted_out if x<big]
	Gsmall_out_values = [Gcounted_out.get(x) for x in Gsmall_out_keys]
	Gsmall_out_sum = sum(Gsmall_out_values)
	Gcounted_in = Counter(Gin_degree_values)
	Gsmall_in_keys = [x for x in Gcounted_in if x<big]
	Gsmall_in_values = [Gcounted_in.get(x) for x in Gsmall_in_keys]
	Gsmall_in_sum = sum(Gsmall_in_values)


	print "h) nodes in graph with out-degree >", big, ":", Tbig_out_sum, "\t", Gbig_out_sum
	print "   nodes in graph with out-degree <", big, ":", Tsmall_out_sum, "\t", Gsmall_out_sum
	print "i) nodes in graph with in-degree <", big, ":", Tsmall_in_sum, "\t", Gsmall_in_sum
	print "   nodes in graph with in-degree >", big, ":", Tbig_in_sum, "\t", Gbig_in_sum

	len_tin = len(Tin_degree_values)
	len_gin = len(Gin_degree_values)
	len_tout = len(Tout_degree_values)
	len_gout = len(Gout_degree_values)
	print "x1) median node in degree:\t\t", Tin_degree_values[len_tin/2], "\t", Gin_degree_values[len_gin/2]
	print "x2) median node out degree:\t\t", Tout_degree_values[len_tout/2], "\t", Gout_degree_values[len_gout/2]
	print "x3) mean node in/out degree:\t\t", sum(Tin_degree_values)*1.0/len_tin*1.0, "\t", sum(Gin_degree_values)*1.0/len_gin*1.0

	"""
	print "out degrees:\n", Gcounted_out
	print "in degrees:\n", Gcounted_in
	"""