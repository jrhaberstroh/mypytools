#!/usr/bin/env python2.7
import sqlite3
import os

db_path = None
table_name = None

"""
Module DBAddData:

A light wrapper for adding data to a sqlite database using python dicts.
Variable db_path: sets the path to the desired database.
Variable table_name: sets the name of the table to be modified in the database.

Call PrintDBCols() to get a list of the columns names in the table & indexes, sorted by whether or not they are required fields.
GetDBCols() is available to avoid typographical errors.
AddToDB(**kwargs) is the function to add data to the database.
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
	
def AddToDB(**kwargs):
	"""
	Setup local variables db_path and table_name first.
	Pass required kwargs & corresponding data, as specified by PrintDBCols(), as key::value pairs.
	Because sqlite is vulnerable to certaint strings, this function generates the sqlite command in a mostly secure way:
	1) It checks that all keys passed to it are present in the database before trying to put them in, and raises a ValueError if there is a mismatch
	2) It puts data into the arguments through the c.execute() function [http://docs.python.org/2/library/sqlite3.html]

	It can raise any excpetions that sqlite3 can raise.
	It returns the command to SQL and the argument list passed to c.execute().
	"""

	all_cols = GetDBCols()[0];
	db_args = []
	arg_list = []
	for key, val in kwargs.iteritems():
		if any(col == key for col in all_cols):
			db_args.append(key)
			arg_list.append(val)
		else:
			print 'AddToResultDB(**kwargs): ERROR: Key "'+key+'" was present in **kwargs. "'+key+'" is not a valid column name'
			print 
			raise ValueError
	str_db_args = ", ".join(db_args)
	str_qmarks  = ",".join( ['?'] * len(db_args) )

	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	command = ("INSERT INTO " + table_name + "(" + str_db_args + ") "
			'VALUES ('+str_qmarks+');' )
	#print command
	#print arg_list
	c.execute(command, arg_list)
	#print c.fetchone()
	conn.commit()
	conn.close() 
	return [command, arg_list]



