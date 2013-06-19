#!/usr/bin/env python2.7
import sqlite3
import os

db_path = None
table_name = None

"""
Module DBReadData:

"""

def GetDBCols():
	"""
	Reads the database table (table_name) from db_path and returns a list:
		0) Column names (unicode)
		1) Column types (unicode)
		2) Column defaults (unicode)
	Note that for default values, python will appropriately read the NULL character as None, independent of any .sqliterc settings.
	"""
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	x = c.execute("pragma table_info(" + table_name + ")")
	query = c.fetchall()
	conn.close()

	cols = []
	types = []
	req = []
	for line in query:
		cols.append(line[1])
		types.append(line[2])
		req.append(line[4])

	return [cols, types, req]

def PrintDBCols():
	"""
	Prints the database columns in a user friendly way, and specifies which entries are required vs optional.
	Also presents the user with the indexes for better using GetDBCols().
	"""

	print "PrintDBCols():"
	print "NOTE: Call GetDBCols to get the raw data."
	print "The first number on each line is the index number for that column."
	print 
	cols = GetDBCols()
	print ".........Required Arguments:"
	for ind,col in enumerate(cols[0]):
		if (cols[2][ind] == None):
			print "%d " % ind + col + " " + cols[1][ind] + "; DEFAULT = " + str(cols[2][ind])

	print
	print ".........Optional Arguments:"
	for ind,col in enumerate(cols[0]):
		if (cols[2][ind] != None):
			print "%d " % ind + col + " " + cols[1][ind] + "; DEFAULT = " + str(cols[2][ind])
	



