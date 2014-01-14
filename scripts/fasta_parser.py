#!/usr/bin/python

from Bio import SeqIO

class FastaParser:
	def parse_fasta(self, in_file):
		# Try opening the file, else give an error
		try:
			in_handle = open(in_file)
		except:
			print 'I/O error({0}): {1}'.format(errno, strerror)
		
		# Parse the content of the fasta file
		fasta_content = SeqIO.parse(in_handle, 'fasta')
		# Make a list from the content
		fasta_content = list(fasta_content)
		return fasta_content

