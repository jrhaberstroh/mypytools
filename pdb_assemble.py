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
		

#def RotateAtoms(mtx, fname):
#	with open(fname) as input_file:



mtxremain = True
mtxcounter = 0
while mtxremain:
	m_mtx,m_trans = FindRotTrans(mtxcounter, args.pdb_base)
	if m_mtx == None:
		mtxremain=False
		break
	print m_mtx
	print m_trans
	mtxcounter += 1

	with open(args.pdb_base) as input_file:
		for i, line in enumerate(input_file):
			pre = line[0:6].strip()
			if (pre == "ATOM"):
				pos = np.matrix(map(float,(line.split())[6:9])).transpose()
				out = (m_mtx * pos) + m_trans
				print line[0:31], "{:6.6g}".format(out[0,0]),"{:6.6g}".format(out[1,0]),"{:6.6g}".format(out[2,0]), line[56:],
				
			#if (pre == "HETATM"):
			#	print line,


	if mtxcounter == 2:
		mtxremain = False
