#!/usr/bin/env python2.7
import argparse
import cPickle
import matplotlib.pyplot as plt
import numpy as np


def plotCt(data_in, args):
	plt.xlabel(args.xlabel)
	plt.ylabel(args.ylabel)
	plt.title(args.title)

	xaxis=[]
	yaxis=[]
        yerr =[] 

        xaxis= np.array(data_in[0][:args.tf])
	yaxis= np.array(data_in[1][:args.tf])
        if args.witherror:
	    yerr= np.array(data_in[2][:args.tf])
	#except:
	#	xaxis= np.array(xrange(0, len(yplot) )) *args.xrescale
	#	yaxis= np.array(yplot)
        #        if args.error:
	#	    yaxis= np.array(data_in[1][0:args.tf])

        print xaxis.shape
        print yaxis.shape
        if args.witherror:
            plt.errorbar(xaxis, yaxis, yerr=yerr, linestyle='None',marker='h', markersize=3, markerfacecolor=args.color)
        else:
	    plt.plot(xaxis, yaxis, linestyle='None',marker='h', markersize=3, markerfacecolor=args.color)

	
	if not (args.multi == None):
		out_dat = [args,xaxis, yaxis] 
                if args.witherror:
                    out_dat.append(yerr)
		pkl_out = open(str(args.multi)+".mpt", 'w')
		print "Saved for multiplot in " + str(args.multi)+".mpt"
		cPickle.dump(out_dat, pkl_out)
		pkl_out.close()

	plt.show()
	exit()

parser = argparse.ArgumentParser(description='Average over many .xvg energy trajectory files to get the average E(t) and S(t).')
parser.add_argument('pkl_name', help='Set the path to the cPickle to plot.')
parser.add_argument('-mode', type=str, default="CT", help='The type of data being processed. Currently, the valid argument is ST (default).')
parser.add_argument('-tf', type=int, help='Set the number of datapoints to plot')
parser.add_argument('-ylabel', type=str, default="", help='The x-axis for the plot.')
parser.add_argument('-xlabel', type=str, default="", help='The y-axis for the plot.')
parser.add_argument('-xrescale', type=float, default=1, help='Factor to apply to the x-axis.')
parser.add_argument('-color', type=str, default="black", help='Color to plot in.')
parser.add_argument('-title', type=str, default="", help='The name of the plot.')
parser.add_argument('-multi', type=int, default=None, help='The multi-plot to output to.')
parser.add_argument('-witherror', action='store_true', help='Use error bars from the .pkl')
args = parser.parse_args()


pkl_in = open(args.pkl_name, 'r')
data_in = cPickle.load(pkl_in)
pkl_in.close()

if (args.mode == "CT"):
	plotCt(data_in, args)
