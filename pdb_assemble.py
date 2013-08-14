#!/usr/bin/python2.7
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Build the molecule described by the bio-assembly instructions in the pdb file. Requires that the biomolecular assembly is specified with matrices, with the BIOMT_ command in spaces [14,19].')
parser.add_argument('pdb_base', help='The file to be expanged.')
args = parser.parse_args()




def FindRotTrans(mtx_pos, fname):
	counter = 0
	subcount = 0
	rot_mtx = np.zeros((3,3))
	trans_vec = np.zeros((3,1))
	with open(fname) as input_file:
		for i, line in enumerate(input_file):
			if (line[13:18] == "BIOMT"):
				if (counter == mtx_pos):
					rot_mtx[subcount] = (line.split())[4:7]
					trans_vec[subcount] = (line.split())[7]
				subcount += 1
				if (counter == mtx_pos and subcount == 3):
					return rot_mtx, trans_vec
				if (subcount == 3):
					subcount = 0
					counter += 1
			#if (line[0:6].strip() == "ATOM"):
			#	print line,
	return None,None
		
def PrintHeader(fname):
	with open(fname) as input_file:
		for i, line in enumerate(input_file):
			pre = line[0:6].strip()
			if (pre != "ATOM" and pre != "HETATM" and pre!= "TER" and pre!= "MASTER" and pre != "END"):
				print line,

#def RotateAtoms(mtx, fname):
#	with open(fname) as input_file:



PrintHeader(args.pdb_base)
mtxremain = True
mtxcounter = 0
while mtxremain:
	m_mtx,m_trans = FindRotTrans(mtxcounter, args.pdb_base)
	if m_mtx == None:
		mtxremain=False
		break
	mtxcounter += 1

	with open(args.pdb_base) as input_file:
		#prev_atm = 0

		for i, line in enumerate(input_file):
			pre = line[0:6].strip()
			if (pre == "ATOM"):
				subcount = int(line[5:11].strip())
				pos = np.matrix(map(float,(line.split())[6:9])).transpose()
				out = (m_mtx * pos) + m_trans
				#print line[0:4],
				#print subcount,
				#print line[11:31], 
				print line[0:29],
				for i in xrange(0,3):
					if out[i,0] <= -100:
						print "{:5.2f}".format(out[i,0]),
					elif out[i,0] <= -10: 
						print "{:6.3f}".format(out[i,0]),
					elif out[i,0] < 0: 
						print " {:6.3f}".format(out[i,0]),
					elif out[i,0] >= 100:
						print " {:5.2f}".format(out[i,0]),
					elif out[i,0] >= 10: 
						print " {:6.3f}".format(out[i,0]),
					elif out[i,0] >= 0: 
						print " {:6.3f}".format(out[i,0]),
					else:
						print "ERROR"
				print line[56:],
				
			if (pre == "TER"):
				print line,

	if mtxcounter == 1:
		mtxremain = False


print "END"
