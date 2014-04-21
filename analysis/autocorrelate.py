#!/usr/bin/env python2.7
import shlex
import numpy as np
import argparse
import cPickle
import matplotlib.pyplot as plt
from sys import exit
import h5py

def xvg2hdf(fname):
    e_t = []
    time = []
    n = 0
    with open(fname, 'r') as f:
	for line in f:
		if (line[0] != '#' and line[0] != '@'):
			cols = shlex.split(line);
			if (float(cols[0]) > args.start_time): 
				if (istimelimit and (args.end_time <= float(cols[0]))):
					break
				e_t.append(float(cols[1]))
				time.append(float(cols[0]))
				n=n+1
                                if n%10000== 0:
				    print n
	e_t = np.array(e_t)
	time= np.array(time)
    assert len(time) == len(e_t)
    out = np.array([time, e_t])
    f = h5py.File('temp.hdf5','a')
    dset = f.create_dataset(fname, (2, len(e_t)), dtype='f')
    dset[:] = out[:]
    print "DATASET:", dset[:]
    f.close()
    return out

def hdf_load(fname):
    with h5py.File('temp.hdf5','r') as f:
        dset = f[fname]
        print "DATASET:", dset[:]
        out = np.array(dset.shape)
        out = dset[:]
    return out

parser = argparse.ArgumentParser(description='Average over many .xvg energy trajectory files to get the average E(t) and S(t).')
# Positional arguments
parser.add_argument('xvg_in', help='The gromacs energy .xvg file to run autocorrelation on')
parser.add_argument('save',  help='Add this argument to save the correlation function (as a cPickle object). This script stores the result of autocorrelation with the time axis in units (usually ps in gromacs). There is no default file extension.')
# Optional arguments
parser.add_argument('-to', dest='start_time', type=float, default=0, help='The time to start at, if part of the trajectory should be ignored. In the units from xvg_in (usually ps in gromacs).')
parser.add_argument('-tf', dest='end_time', type=float, default=0, help='The time to end at, if part of the trajectory should be ignored. In the units from xvg_in (usually ps in gromacs).')
parser.add_argument('-p', dest='lenplot', type=int, default=0, help='The number of data points to plot. Should be passed with --pklplot to allow pklplot to plot anything')
parser.add_argument('-2', dest='half', action='store_true', help='Split the data in half and plot the two halves autocorrelated separately in addition to doing the full autocorrelation (primarily for error checking purposes). Saved half-files will have appended to their file names ".1" and ".2".')

args = parser.parse_args()
istimelimit = 0;
if (args.end_time != 0):
	istimelimit = 1

# MAIN FUNCTION
e_t = None
time = None

fname = args.xvg_in
pickle_name = args.save

try:
    out = hdf_load(fname)
    time = out[0,:] 
    e_t  = out[1,:]
    print "Note: Loaded old values of e_t and time from temp.hdf5. Delete this file to re-load from your .xvg file"
except (IOError, KeyError):
    print "Note: No temp file found, loading xvg data"
    out = xvg2hdf(fname)
    time = out[0,:]
    e_t  = out[1,:] 
    print "Note: Storing xvg data as temp.hdf5, load will be faster next time!"

#if half:
#	print "Computing Halves"
#	half1 = np.array(e_t[0:len(e_t)/2])
#	half2 = np.array(e_t[len(e_t)/2:len(e_t)])
#	dhalf1= half1 - np.mean(half1)
#	dhalf2= half2 - np.mean(half2)
#	crlf1 = np.correlate(dhalf1, dhalf1, mode='full')[len(dhalf1)-1:]
#	crlf2 = np.correlate(dhalf2, dhalf2, mode='full')[len(dhalf2)-1:]
#	if (pickle_name != ""):
#		print "Pickle requested! Pickling the halves!"
#		pkl_out = open(pickle_name + ".1", 'w')
#		cPickle.dump(crlf1, pkl_out)
#		pkl_out.close()
#		pkl_out = open(pickle_name + ".2", 'w')
#		cPickle.dump(crlf2, pkl_out)
#		pkl_out.close()

N_times = min(len(e_t), 200000)
print "Computing AutoCorrelation and Error from",N_times,"values..."
de_t = e_t - np.mean(e_t)
de_t = de_t[0:N_times]
time = time[0:N_times]
desq = np.square(de_t)
desq -= np.mean(desq)


def real_autocorr(fx):
    return np.correlate( fx, fx, mode='full')[len(fx)-1:]

crlf      = real_autocorr(de_t)
crlf_err  = real_autocorr(desq)
crlf_err  = np.sqrt(np.abs(crlf_err))

print "Normalizing Correlation..."
for i in range(len(crlf)):
	crlf[i]     = crlf[i]     / (len(crlf) - i - 1)
        crlf_err[i] = crlf_err[i] / (len(crlf_err) - i -1)

print "STDEV:", crlf[0]
print "STDEV_ERR:", crlf_err[0]

normal = crlf[0]
crlf     /= normal
crlf_err /= normal


if (pickle_name != ""):
	print "Pickle requested!"
	pkl_out = open(pickle_name, 'w')
	cPickle.dump((time,crlf,crlf_err), pkl_out)
	pkl_out.close()


print len(crlf)
print len(time)
if (args.lenplot > 0):
    print "Correlation Function Preview: ", crlf
    plt.errorbar(time[0:args.lenplot], crlf[0:args.lenplot], yerr=crlf_err[0:args.lenplot])
    plt.show()


