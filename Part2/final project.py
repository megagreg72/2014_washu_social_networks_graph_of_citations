import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from histogram import *
from log_bars import log_barify
from semi_pref import *
from network_basics import log_basics
from datetime import datetime
import operator

import warnings
warnings.filterwarnings("ignore")

print "-----Social Network Analysis-----"
print "-----Washu-------Spring 2014-----"
print "----------Brian Gauch------------"
print "----------Final Project----------"

node_attributes_file = "cit-HepPh-dates.txt"
edges_file = "Cit-HepPh.txt"

G0 = nx.DiGraph()

print "Make sure", edges_file, "is in the same directory as this code"
G = nx.read_edgelist(edges_file, comments='#', delimiter=None, create_using=G0, \
nodetype=None, data=True, edgetype=None, encoding='utf-8')

print "Make sure", node_attributes_file, "is in the same directory as this code"
f = open(node_attributes_file)
dates = []
for line in f.readlines():
	strng = line.strip()
	if len(strng) > 0:
		tokens = strng.split()
		if tokens[0][0] == '#':
			pass
			# ignore
		else:
			if len(tokens) is 2:
				node_name = tokens[0]
				date = tokens[1]
				attrs = dict()
				attrs['date'] = date
				# print attrs
				# allAttrs[node_name] = attrs
				# G0.add_node(node_name, attrs)
				# print G.nodes(data=True)
				try:
					G.node[node_name]['date'] = date
					dates.append(date)
				except KeyError: # NetworkXError if node_name not in G
					# print "no node:", node_name
					pass
			else:
				print "wrong number of tokens:", tokens
f.close()

log_basics(G)

# create log-log plot
print "\n------------Part 1:------------"
print "-----------Power Law-----------\n"



fig = plt.figure()
num_test_nodes = 5000
num_connections = 1.0

ba_g = nx.barabasi_albert_graph(num_test_nodes, int(num_connections))
ba_g = ba_g.to_directed()
# preferentialness = 0.5
# ba_g = barabasi_albert_graph2(num_test_nodes, num_connections, preferentialness)
# ba_g = gn_semi_preferential(num_test_nodes, preferentialness)
#ax = fig.add_subplot(131)
ax = fig.add_subplot(231)
ax.set_title('Power Law Graph (Barabasi-Albert model)')
plotInDegrees(ba_g)


p = num_connections/num_test_nodes
ba_g = nx.fast_gnp_random_graph(num_test_nodes, p)
ba_g = ba_g.to_directed()
# preferentialness = 0.0
# ba_g = gn_semi_preferential(num_test_nodes, preferentialness)
# ax = fig.add_subplot(133)
ax = fig.add_subplot(234)
ax.set_title('Random Graph (Erdos Renyi model)')
plotInDegrees(ba_g)


preferentialness = 0.7
ba_g = gn_semi_preferential(num_test_nodes, preferentialness)
ax = fig.add_subplot(232)
title = 'Semi Preferential Graph (mix of the two models), pref =', preferentialness
ax.set_title(title)
plotInDegrees(ba_g)

preferentialness = 0.3
ba_g = gn_semi_preferential(num_test_nodes, preferentialness)
ax = fig.add_subplot(235)
title = 'Semi Preferential Graph (mix of the two models), pref =',preferentialness
ax.set_title(title)
plotInDegrees(ba_g)


ax = fig.add_subplot(233)
# ax = fig.add_subplot(132)
ax.set_title('Citation In Degrees(raw in blue, binned in red)')
plotInDegrees(G)


ax = fig.add_subplot(236)
ax.set_title('Citation Out Degrees(raw in blue, binned in red)')
plotOutDegrees(G)




print "\n------------Part 2:------------"
print "----Popularity Deterioration---\n"

diffs = []
for n1, n2 in G.edges_iter():
	try:
		date1 = G.node[n1]['date']
	except KeyError:
		date1 = None
	try:
		date2 = G.node[n2]['date']
	except KeyError:
		date2 = None
	
	if(date1 and date2):
		date_obj1 = datetime.strptime(date1, '%Y-%m-%d')
		date_obj2 = datetime.strptime(date2, '%Y-%m-%d')
		diff_obj = date_obj1 - date_obj2
		diff = diff_obj.days
		diffs.append(diff)

fig = plt.figure()
ax = fig.add_subplot(121)
ax.set_title('Real Network G')
plotDateDiffs(diffs)

rand_diffs = []
len_dates = len(dates)
for n1, n2 in G.edges_iter():
	rand1 = random.randint(0, len_dates-1)
	rand2 = random.randint(0, len_dates-1)
	date1 = dates[rand1]
	date2 = dates[rand2]
	
	if(date1 and date2):
		date_obj1 = datetime.strptime(date1, '%Y-%m-%d')
		date_obj2 = datetime.strptime(date2, '%Y-%m-%d')
		diff_obj = date_obj1 - date_obj2
		diff = diff_obj.days
		rand_diffs.append(diff)

ax = fig.add_subplot(122)
ax.set_title('Generated Random graph using dates from G')
plotDateDiffs(rand_diffs)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('G(red) and T(blue)')
doublePlotDateDiffs(diffs, rand_diffs)

print "\n------------Part 3:-----------"
print "----------Communities---------\n"
print "----------G (real data)---------\n"


unG = G.to_undirected()

k = 15
comms = list(nx.k_clique_communities(unG, k))
comm_lens = [len(comm) for comm in comms]
print str(len(comm_lens)) + " " + str(k) + "-clique communities (with size):\t" + str(comm_lens)


# comps = nx.weakly_connected_components(G)
comps = nx.connected_components(unG)
comp_lens = [len(comp) for comp in comps]
print str(len(comp_lens)) + " components (with size):\t" + str(comp_lens)

clustering = nx.average_clustering(unG)
print "average clustering:", clustering


print "----------T (generated barabasi_albert_graph)---------\n"
num_test_nodes = 34500
num_connections = 12
unT = nx.barabasi_albert_graph(num_test_nodes, num_connections)


k = 5
comms = list(nx.k_clique_communities(unT, k))
comm_lens = [len(comm) for comm in comms]
print str(len(comm_lens)) + " " + str(k) + "-clique communities (with size):\t" + str(comm_lens)


comps = nx.connected_components(unT)
comp_lens = [len(comp) for comp in comps]
print str(len(comp_lens)) + " components (with size):\t" + str(comp_lens)

clustering = nx.average_clustering(unT)
print "average clustering:", clustering


fig = plt.figure()

k = 100

ax = fig.add_subplot(211)
ax.set_title('Generated Network T')
betT = plotBetweenness(unT, k)

ax = fig.add_subplot(212)
ax.set_title('Real Network G')
betG = plotBetweenness(G, k)
len_g = len(G.nodes())
len_t = num_test_nodes

sorted_betG = sorted(betG.iteritems(), key=operator.itemgetter(1))
sorted_betT = sorted(betT.iteritems(), key=operator.itemgetter(1))
betGOnly = [b for (id, b) in sorted_betG]
betTOnly = [b for (id, b) in sorted_betT]

print "median betweenness:\tT:", betTOnly[len_t/2], "\tG:", betGOnly[len_g/2]
print "mean betweenness:\tT:", sum(betTOnly)/len_t, "\tG:", sum(betGOnly)/len_g


plt.show()