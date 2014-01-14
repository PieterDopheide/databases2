#!/usr/bin/python

#Adapted from the code found at http://www.osmonov.com/2009/11/simple-mysql-dao-class-for-python.html

import os
import sys
import MySQLdb

class DAO:
	def __init__(self):
		"""
		Inits MySQL connection
		"""
		self._connect()
		return

	def _connect(self):
		"""
		Creates connection
		"""
		try:
			option_file = os.environ['HOME'] + '/' + '.my.cnf'
			self.connection = MySQLdb.connect(db = 'Pjmdopheide', read_default_file = option_file)
			return
		except:
			print 'Cannot connect to the db'
			sys.exit(1)

	def _get_cursor(self):
		"""
		Pings connection and returns cursor
		"""
		try:
			self.connection.ping()
		except:
			self._connect()
		return self.connection.cursor()

	def get_row(self, query):
		"""
		Fetchs one row
		"""
		cursor = self._get_cursor()
		cursor.execute(query)
		row = cursor.fetchone()
		cursor.close()
		return row

	def get_rows(self, query):
		"""
		Fetchs all rows
		"""
		cursor = self._get_cursor()
		cursor.execute(query)
		rows = cursor.fetchall()
		cursor.close()
		return rows

	def execute(self, query):  
		"""
		Executes query for update, delete
		"""
		cursor = self._get_cursor()
		cursor.execute(query)
		cursor.close()
		return
	
	def store_read(self, read):
		cursor = self._get_cursor()
		read_len = len(read.seq)
		
		query = 'CALL read2db("%s", "%s", "%s");' % (read.id, read.seq, read_len)
		try:
			self.execute(query)
		except:
			print 'Couldn\'t store the read (possibly because it is already in the database)'
		return
	
	def store_alignment(self, id1, id2, alignment, header):
		cursor = self._get_cursor()
		read1_seq = alignment[0].seq
		read2_seq = alignment[1].seq
		align_len = alignment.get_alignment_length()
		
		identity = header[0][0]
		similarity = header[1][0]
		gaps = header[2][0]
		
		query = 'CALL alignment2db("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (id1, id2, read1_seq, read2_seq, align_len, identity, similarity, gaps)
		try:
			self.execute(query)
		except:
			print 'Couldn\'t store the alignment'
		return
	
	def get_most_overlap(self, id):
		cursor = self._get_cursor()
		
		query = 'CALL GetMostOverlap("%s");' % id
		try:
			overlap = self.get_row(query)
			return overlap
		except:
			print 'Couldn\'t get the read'
			return False
	
	def get_exact_match(self):
		cursor = self._get_cursor()
		
		query = 'CALL GetExactMatch;'
		try:
			exact = self.get_rows(query)
			return exact
		except:
			print 'Could\'t find a read with an exact match'
			return False
	
	def get_one_snp(self):
		cursor = self._get_cursor()
		
		query = 'CALL GetOneSNP;'
		try:
			snps = self.get_rows(query)
			return snps
		except:
			print 'Didn\'t found a read with one SNP'
			return False

