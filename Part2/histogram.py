"""
This example shows how to use a path patch to draw a bunch of
rectangles for an animated histogram
"""
from math import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from collections import Counter

import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation
from time import sleep

class Histifier:

	def __init__(self, data, xscale, yscale, num_bins, title, xlabel, ylabel):
		self.data = data
		self.num_bins = num_bins
		self.members = 0
		
		fig, ax = plt.subplots()
		self.fig = fig
		self.ax = ax
		
		fig.suptitle(title, fontsize=14, fontweight='bold')
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_xscale(xscale)
		ax.set_yscale(yscale)
		
		# histogram our data with numpy
		n, bins = np.histogram(self.data, self.num_bins)
		self.n = n
		self.bins = bins

		# get the corners of the rectangles for the histogram
		self.left = np.array(bins[:-1])
		self.right = np.array(bins[1:])
		self.bottom = np.zeros(len(self.left))
		self.top = self.bottom + self.n
		nrects = len(self.left)
		
		# here comes the tricky part -- we have to set up the vertex and path
		# codes arrays using moveto, lineto and closepoly
		
		# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
		# CLOSEPOLY; the vert for the closepoly is ignored but we still need
		# it to keep the codes aligned with the vertices
		nverts = nrects*(1+3+1)
		self.verts = np.zeros((nverts, 2))
		codes = np.ones(nverts, int) * path.Path.LINETO
		codes[0::5] = path.Path.MOVETO
		codes[4::5] = path.Path.CLOSEPOLY
		self.verts[0::5,0] = self.left
		self.verts[0::5,1] = self.bottom
		self.verts[1::5,0] = self.left
		self.verts[1::5,1] = self.top
		self.verts[2::5,0] = self.right
		self.verts[2::5,1] = self.top
		self.verts[3::5,0] = self.right
		self.verts[3::5,1] = self.bottom

		barpath = path.Path(self.verts, codes)
		patch = patches.PathPatch(barpath, facecolor='green', edgecolor='blue', alpha=0.7)
		self.ax.add_patch(patch)

		self.ax.set_xlim(self.left[0], self.right[-1])
		self.ax.set_ylim(self.bottom.min(), self.top.max())

	def update(self, junk):
		# simulate new data coming in
		#self.data = np.random.randn(1000)
		#self.n, self.bins = np.histogram(self.data, self.num_bins)
		self.top = self.bottom + self.n
		self.verts[1::5,1] = self.top
		self.verts[2::5,1] = self.top

	def display(self):
		num_frames = 1
		ani = animation.FuncAnimation(self.fig, self.update, num_frames, repeat=False)


def drop_zeros(a_list):
    return [i for i in a_list if i>0]

def log_binning(counter_dict, bin_count=35):

    max_x = log10(max(counter_dict.keys()))
    max_y = log10(max(counter_dict.values()))
    max_base = max([max_x, max_y])

    min_x = log10(min(drop_zeros(counter_dict.keys())))

    bins = np.logspace(min_x, max_base, num=bin_count)

    # Based off of: http://stackoverflow.com/questions/6163334/binning-data-in-python-with-scipy-numpy
    bin_means_y = (np.histogram(counter_dict.keys(), bins, weights=counter_dict.values())[0] / np.histogram(counter_dict.keys(), bins)[0])
    bin_means_x = (np.histogram(counter_dict.keys(), bins, weights=counter_dict.keys())[0] / np.histogram(counter_dict.keys(), bins)[0])

    return bin_means_x,bin_means_y

def plotInDegrees(graph):
	num_bins = 50
	ba_g = graph
	# ba_g = nx.barabasi_albert_graph(10000,2)
	ba_c = nx.in_degree_centrality(ba_g)
	# To convert normalized degrees to raw degrees
	# ba_c2 = {k:int(v*(len(ba_g)-1)) for k,v in ba_c.iteritems()}
	ba_c2 = dict(Counter(ba_c.values()))

	ba_x, ba_y = log_binning(ba_c2, num_bins)

	plt.xscale('log')
	plt.yscale('log')
	plt.scatter(ba_x,ba_y,c='r',marker='s',s=num_bins)
	plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
	plt.xlim((1e-5,1e-0))
	plt.ylim((.9,1e5))
	plt.xlabel('Connections per node (normalized by total in graph)')
	plt.ylabel('Frequency')
	
def plotOutDegrees(graph):
	num_bins = 50
	ba_g = graph
	ba_c = nx.out_degree_centrality(ba_g)
	ba_c2 = dict(Counter(ba_c.values()))

	ba_x, ba_y = log_binning(ba_c2, num_bins)

	plt.xscale('log')
	plt.yscale('log')
	plt.scatter(ba_x,ba_y,c='r',marker='s',s=num_bins)
	plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
	plt.xlim((1e-5,1e-0))
	plt.ylim((.9,1e5))
	plt.xlabel('Connections per node (normalized by total in graph)')
	plt.ylabel('Frequency')

def plotTotalDegrees(graph):
	num_bins = 50
	ba_g = graph
	ba_c = nx.degree_centrality(ba_g)
	ba_c2 = dict(Counter(ba_c.values()))

	ba_x, ba_y = log_binning(ba_c2, num_bins)

	plt.xscale('log')
	plt.yscale('log')
	plt.scatter(ba_x,ba_y,c='r',marker='s',s=num_bins)
	plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
	plt.xlim((1e-5,1e-0))
	plt.ylim((.9,1e5))
	plt.xlabel('Connections per node (normalized by total in graph)')
	plt.ylabel('Frequency')
	
def plotBetweenness(graph, k):
	num_bins = 50
	ba_g = graph
	ba_c = nx.betweenness_centrality(ba_g, k)
	ba_c2 = dict(Counter(ba_c.values()))

	ba_x, ba_y = log_binning(ba_c2, num_bins)

	plt.xscale('log')
	plt.yscale('log')
	plt.scatter(ba_x,ba_y,c='r',marker='s',s=num_bins)
	plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
	plt.xlim((1e-4,1e-0))
	plt.ylim((.9,1e4))
	plt.xlabel('Betweenness per node (normalized by total in graph)')
	plt.ylabel('Frequency')
	return ba_c

def plotDateDiffs(diffs):
	num_bins = 50
	ba_c2 = dict(Counter(diffs))

	ba_x, ba_y = log_binning(ba_c2, num_bins)

	plt.xscale('linear')
	plt.yscale('linear')
	plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
	plt.scatter(ba_x,ba_y,c='r',marker='s',s=num_bins)
	plt.xlim((0, 4000))
	plt.ylim((0, 400))
	# plt.xlim((1e-0,1e4))
	# plt.ylim((.9,1e4))
	plt.xlabel('Date diff (in days)')
	plt.ylabel('Frequency')
	
def doublePlotDateDiffs(diffs1, diffs2):
	num_bins = 50
	ba_c1 = dict(Counter(diffs1))
	ba_c2 = dict(Counter(diffs2))

	ba_x1, ba_y1 = log_binning(ba_c1, num_bins)
	ba_x2, ba_y2 = log_binning(ba_c2, num_bins)

	plt.xscale('linear')
	plt.yscale('linear')
	plt.scatter(ba_x2,ba_y2,c='b',marker='s',s=num_bins)
	plt.scatter(ba_x1,ba_y1,c='r',marker='s',s=num_bins)
	plt.xlim((0, 4000))
	plt.ylim((0, 400))
	# plt.xlim((1e-0,1e4))
	# plt.ylim((.9,1e4))
	plt.xlabel('Date diff (in days)')
	plt.ylabel('Frequency')