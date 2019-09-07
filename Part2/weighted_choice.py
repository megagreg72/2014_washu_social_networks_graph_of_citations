import itertools
import random
import math
import bisect
import networkx as nx
from networkx.generators.classic import empty_graph, path_graph, complete_graph
"""
Part of a failed attempt to reimplement NetworkX
graph generation. Nothing to see here.
"""


"""
Gets random element of list in O(n) time.
"""
class static_weighted_choice(object):
	def __init__(self, weights):
		self.totals = []
		running_total = 0

		for w in weights:
			running_total += w
			self.totals.append(running_total)

	def getRandomItem(self):
		rnd = random.random() * self.totals[-1]
		return bisect.bisect_right(self.totals, rnd)

	def __call__(self):
		return self.getRandomItem()

"""
Gets random element of list in O(n^2) time.
Allows for any number of changes to list.
"""
def dynamic_weighted_choice(weights):
	rnd = random.random() * sum(weights)
	for i, w in enumerate(weights):
		rnd -= w
		if rnd < 0:
			return i
		
"""
The idea is to select elements at random from a weighted list
while getting near-static speed using a near-static list.

Gets random element of list in O(n*lg(n)) time
if there are O(n) changes to the list.
"""
class semi_static_weighted_choice:
	def __init__(self, items, weights):
		self.items = []
		self.weights = []
		for i in range(len(items)):
			self.items.append(items[i])
			self.weights.append([i, weights[i]])
			
		self.staticTotals = []
		self.tempWeights = []
		
		running_total = 0
		for w in self.weights:
			running_total += w[1]
			self.staticTotals.append(running_total)
			
		self.upToDate = True
		self.updateThreshold = math.log(len(self.weights))

	def addItem(self, item, weight):
		self.items.append(item)
		itemIndex = len(self.items) - 1
		self.weights.append([itemIndex, weight])
		self.upToDate = False
		
		if(len(self.tempWeights) >= self.updateThreshold):
			self._update()
		return itemIndex
	
	def changeWeight(self, itemIndex, weightDiff):
		self.tempWeights.append([itemIndex, weightDiff])
		
		if(len(self.tempWeights) >= self.updateThreshold):
			self._update()
	
	def getRandomItem(self):
		# foo[-1] gets last element of foo
		rnd = random.random() * self.staticTotals[-1]
		ans = bisect.bisect_right(self.staticTotals, rnd)
		
		if not self.upToDate:
			self._update()
		
		ansIndex = bisect.bisect_right(self.staticTotals, rnd)
		
		return ansIndex, self.items[ansIndex]
	
	# empties temp weight update queue
	# and updates totals
	def _update(self):
		print "tempWeights: " + str(self.tempWeights)
		print "weights: " + str(self.tempWeights)
		print "items: " + str(self.items)
		print "totals: " + str(self.staticTotals)
		# update weights
		for w in self.tempWeights:
			index = w[0]
			weight = w[1]
			self.weights[index][1] += weight
		self.tempWeights = []
		# update totals
		self.staticTotals = []
		running_total = 0
		for w in self.weights:
			running_total += w[1]
			self.staticTotals.append(running_total)
		
		self.updateThreshold = math.log(len(self.weights))
		self.upToDate = True
	
	# semi_static_weighted_choice() == semi_static_weighted_choice.next()
	def __call__(self):
		return self.getRandomItem()
