#!/usr/bin/python

import fasta_parser
import aligner
import alignment_parser
import mysql_dao

class DatabasesMain:
	def ready_reads(self, fasta_content):
		len_gen = len(fasta_content)
		# For each read in the fasta file, align it to the other reads in the file except itself!
		for i in range(0, len_gen - 1):
			for j in range(i + 1, len_gen):
				a = fasta_content[i]
				b = fasta_content[j]
				tmp_needle_out = aligner.Aligner().run_needle(a, b)
				alignment_parser.AlignmentParser().parse_alignment(a, b, tmp_needle_out)
	
	def read2db(self, fasta_content):
		# Call doa function to put read id and sequence in the database
		for read in fasta_content:
			mysql_dao.DAO().store_read(read)
	
	def ask_file(self):
		# Ask user for the full path to a multifasta file
		in_file = raw_input('Please type the full path to the multifasta file you want to load:\n')
		in_file.rstrip()
		return in_file

	def main(self):
		in_file = self.ask_file()
		# Parse fasta file and get the content in a list
		fasta_content = fasta_parser.FastaParser().parse_fasta(in_file)
		# Put the sequences/reads from the fasta file in the database
		self.read2db(fasta_content)
		print 'Reads stored in the database!'
		self.ready_reads(fasta_content)

if __name__ == '__main__':	
	DatabasesMain().main(in_file)

