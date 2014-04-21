#!/usr/bin/env python2.7
import cPickle
import argparse
import numpy as np
from pylab import *


parser = argparse.ArgumentParser(description='Plot a .pkl file with default plotting parameters.')
parser.add_argument('pkl_names', nargs="+", help='The file to be plotted.')
parser.add_argument('-ylabel', type=str, default="", help='The x-axis for the plot.')
parser.add_argument('-xlabel', type=str, default="", help='The y-axis for the plot.')
parser.add_argument('-title', type=str, default="", help='The name of the plot.')
args = parser.parse_args()


plt.hold(True)
for pkl_name in args.pkl_names:
	pkl_in = open(pkl_name, 'r')
	print "Opened file " + pkl_name
	plotdat = cPickle.load(pkl_in)
	pkl_in.close()
        if plotdat[0].witherror:
	    plt.errorbar(plotdat[1], plotdat[2], yerr = plotdat[3], marker='h', markersize=3, mfc=plotdat[0].color, mew=0, c=plotdat[0].color, label=plotdat[0].title)
        else:
	    plt.plot(plotdat[1], plotdat[2], marker='h', markersize=3, mfc=plotdat[0].color, mew=0, c=plotdat[0].color, label=plotdat[0].title)
	plt.legend()
	print len(plotdat[1])

plt.xlabel(args.xlabel)
plt.ylabel(args.ylabel)
plt.title(args.title)

plt.show()
