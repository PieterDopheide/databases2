#!/usr/bin/python

import mysql_dao

class AskDb:
	def ask_read_id(self):
		# Ask the user for a read, the input in not checked for validity!
		read_id = raw_input('Please enter the id of a read:\n')
		return read_id.rstrip()
	
	def overlap(self, read_id):
		# Shows the ID the user put in and calls mysql_dao to search the database, displaying the results
		overlap_read = mysql_dao.DAO().get_most_overlap(read_id)
		if overlap_read:
			print overlap_read
		else:
			print 'Couldn\'t get the read'
	
	def exact(self):
		# Using mysql_dao searches the database for all reads having an exact match and displays the results
		exact_matches = mysql_dao.DAO().get_exact_match()
		if exact_matches:
			for row in exact_matches:
				print row
		else:
			print 'Could\'t find a read with an exact match'
	
	def snp(self):
		# Using mysql_dao searches the database for all reads having 1 SNP and displays the results
		one_snp_reads = mysql_dao.DAO().get_one_snp()
		if one_snp_reads:
			for row in one_snp_reads:
				print one_snp_reads
		else:
			print 'Didn\'t found a read with one SNP'
	
	def main(self):
		# Asks user which question to "ask" the database and processes the inputted choice
		function = raw_input('Which function do you want to test? [overlap/exact/snp]:\n')
		function.rstrip()
		if function == 'overlap':
			read_id = self.ask_read_id()
			self.overlap(read_id)
		elif function == 'exact':
			self.exact()
		elif function == 'snp':
			self.snp()
		else:
			print 'Please type "overlap", "exact" or "snp"'

if __name__ == '__main__':
	AskDb().main()

