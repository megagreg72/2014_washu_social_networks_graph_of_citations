import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation
from time import sleep

def log_barify(data, scale, num_bins):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	rects = None
	if scale == 'linear-linear':
		ax.set_xscale("linear")
		ax.set_yscale("linear")
		hist, bin_edges = np.histogram(data, bins=num_bins)
		width = (max(bin_edges)-min(bin_edges))/len(bin_edges)
		rects = ax.bar(bin_edges[:-1], hist, width = width, facecolor='green')
	if scale == 'linear-log':
		ax.set_xscale("linear")
		ax.set_yscale("log")
		hist, bin_edges = np.histogram(data, bins=num_bins)
		hist = np.log10(hist)
		width = (max(bin_edges)-min(bin_edges))/len(bin_edges)
		rects = ax.bar(bin_edges[:-1], hist, width = width, facecolor='green')
	if scale == 'log-linear':
		ax.set_xscale("log")
		ax.set_yscale("linear")
		hist, bin_edges = np.histogram(data, bins=num_bins)
		bin_edges = np.log10(bin_edges)
		width = (max(bin_edges)-min(bin_edges))/len(bin_edges)
		rects = ax.bar(bin_edges[:-1], hist, width = width, facecolor='green')
	if scale == 'log-log':
		ax.set_xscale("log")
		ax.set_yscale("log")
		hist, bin_edges = np.histogram(data, bins=num_bins)
		bin_edges = np.log10(bin_edges)
		hist = np.log10(hist)
		width = (max(bin_edges)-min(bin_edges))/len(bin_edges)
		rects = ax.bar(bin_edges[:-1], hist, width = width, facecolor='green')
	return rects