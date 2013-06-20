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


def Read(*args, **kwargs):
	"""
	Calls, schematically speaking, 'SELECT *args FROM table_name WHERE **kwargs'
	Pass *args for the desired columns.
	Pass **kwargs to specify WHERE options, in the simple format 'key == value'. Value can be a tuple, in which case an "or" is placed between tuple options.

	1) Checks that all **kwarg keys are in the database as columns.
	2) Formats **kwarg arguments into database properly.
	3) Checks that all *args values are in the database as columns.

	Note that table_name is still insecure.
	"""
	if db_path == None or table_name == None:
		print "You must set BOTH the table_name and the db_path namespace variables to run Read()!"
		raise ValueError

	all_cols = GetDBCols()[0];
	#all_cols = ['Col1', 'shoebox']
	for arg_col in args:
		if not any(col == arg_col for col in all_cols):
			print "Column "+arc_col+" supplied by *args not valid"
			raise ValueError
	column_str = ', '.join(args)
	
	constraints_and = []
	constraints_val_list = []
	for key, val_list in kwargs.iteritems():
		constraints_or = []
		if any(col == key for col in all_cols):
			if type(val_list) != tuple and type(val_list) != list:
				# If we were not passed a tuple or list, make a tuple so that our object is properly iterable.
				val_list = (val_list,)
			for val in val_list:
				constraints_or.append(key + "==?")
				constraints_val_list.append(val)
			constraints_and.append('(' + " OR ".join(constraints_or) + ')')

		else:
			print "Column "+key+" supplied by **kwargs not valid"
			raise ValueError
	constraints = ' AND '.join(constraints_and)
	
	command =  "SELECT " + column_str + " FROM " + table_name + " WHERE " + constraints
	print command
	print constraints_val_list

	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	x = c.execute(command, constraints_val_list)
	query = c.fetchall()
	conn.close()

	return query



#args = ['Col1', 'shoebox']
#kwargs = {'Col1': (1, 2, 23), 'shoebox' : 10}
#Read(*args, **kwargs)
