#!/usr/bin/env python2.7
""" Module dbwrap:
	Merger of DBAddData and DBReadData

A light wrapper for adding data to a sqlite database using python dicts.
Variable db_path: sets the path to the desired database.
Variable table_name: sets the name of the table to be modified in the database.
		
Call PrintDBCols() to get a list of the columns names in the table & indexes, sorted by whether or not they are required fields.
GetCols() is available to avoid typographical errors.
AddToDB(**kwargs) is the function to add data to the database.
"""

import sqlite3
import os

db_path = None
table_name = None


def CheckTable():
	if db_path == None or table_name == None:
		print "You must set BOTH the table_name and the db_path namespace variables to run Read()!"
		raise ValueError

def GetCols():
	"""
	Reads the database table (table_name) from db_path and returns a list:
		0) Column names (unicode)
		1) Column types (unicode)
		2) Column defaults (unicode)
	NOTE: table_name string formatting NOT secure...
	Note that for default values, python will appropriately read the NULL character as None, independent of any .sqliterc settings.
	"""
	CheckTable()

	#arg = table_name,
	conn = sqlite3.connect(db_path)
	with conn:
		c = conn.cursor()
		x = c.execute('PRAGMA table_info('+table_name+')')
		query = c.fetchall()

	cols = []
	types = []
	req = []
	for line in query:
		cols.append(line[1])
		types.append(line[2])
		req.append(line[4])

	return [cols, types, req]



def PrintCols():
	"""
	Prints the database columns in a user friendly way, and specifies which entries are required vs optional.
	Also presents the user with the indexes for better using GetCols().
	"""
	CheckTable()

	print "PrintDBCols():"
	print "NOTE: Call GetCols to get the raw data."
	print "The first number on each line is the index number for that column."
	print 
	cols = GetCols()
	print ".........Required Arguments:"
	for ind,col in enumerate(cols[0]):
		if (cols[2][ind] == None):
			print "%d " % ind + col + " " + cols[1][ind] + "; DEFAULT = " + str(cols[2][ind])

	print
	print ".........Optional Arguments:"
	for ind,col in enumerate(cols[0]):
		if (cols[2][ind] != None):
			print "%d " % ind + col + " " + cols[1][ind] + "; DEFAULT = " + str(cols[2][ind])
	
def AddData(**kwargs):
	"""
	Setup local variables db_path and table_name first.
	Pass required kwargs & corresponding data, as specified by PrintDBCols(), as key::value pairs.
	Because sqlite is vulnerable to certaint strings, this function generates the sqlite command in a mostly secure way:
	1) It checks that all keys passed to it are present in the database before trying to put them in, and raises a ValueError if there is a mismatch
	2) It puts data into the arguments through the c.execute() function [http://docs.python.org/2/library/sqlite3.html]
	3) table_name not checked for security

	It can raise any excpetions that sqlite3 can raise.
	It returns the command to SQL and the argument list passed to c.execute().
	"""
	CheckTable()

	all_cols = GetCols()[0];
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
	with conn:
		c = conn.cursor()
		command = ("INSERT INTO " + table_name + "(" + str_db_args + ") "
			   'VALUES ('+str_qmarks+');' )
	#print command
	#print arg_list
		c.execute(command, arg_list)
	#print c.fetchone()
	return [command, arg_list]


def ReadData(*args, **kwargs):
	"""
	Calls, schematically speaking, 'SELECT *args FROM table_name WHERE **kwargs'
	Pass *args for the desired columns.
	Pass **kwargs to specify WHERE options, in the simple format 'key == value'. Value can be a tuple, in which case an "or" is placed between tuple options.

	1) Checks that all **kwarg keys are in the database as columns.
	2) Formats **kwarg arguments into database properly.
	3) Checks that all *args values are in the database as columns.

	Note that table_name is still insecure.
	"""
	CheckTable()

	all_cols = GetCols()[0];
	#all_cols = ['Col1', 'shoebox']
	for arg_col in args:
		if not any(col == arg_col for col in all_cols):
			print "Column "+arg_col+" supplied by *args not valid"
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
	with conn:
		c = conn.cursor()
		x = c.execute(command, constraints_val_list)
		query = c.fetchall()
	return query



def test():
	## test requires a test database...
	return True
