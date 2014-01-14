#!/usr/bin/python

import os
import subprocess
import tempfile

from Bio import SeqIO
from Bio.Emboss.Applications import NeedleCommandline

class Aligner:
	def run_needle(self, a, b):
		# Create several temporary files, the first one is for the output of needle, the other 2 is for the reads
		(_, tmp_out) = tempfile.mkstemp()
		(_, tmp_file1) = tempfile.mkstemp()
		(_, tmp_file2) = tempfile.mkstemp()
		# Try to open two of the tmp files to put the sequences that are going to be aligned in
		try:
			tmp_handle1 = open(tmp_file1, 'w')
			tmp_handle2 = open(tmp_file2, 'w')
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}".format(errno, strerror)
		
		# Write the sequences to the opened temp files
		SeqIO.write(a, tmp_handle1, 'fasta')
		SeqIO.write(b, tmp_handle2, 'fasta')
		# Close the temp files
		tmp_handle1.close()
		tmp_handle2.close()
		
		# Prepare needle command-line
		cline = NeedleCommandline(gapopen = 10, gapextend = .5, outfile = tmp_out,
				asequence = '%s' % (tmp_file1),
				bsequence = '%s' % (tmp_file2))
		# Run needle on the command-line with the above prepared command-line
		child = subprocess.Popen(str(cline), shell = True,)
		# Wait for needle to finish
		child.wait()
		# Remove the tmp sequences files
		os.remove(tmp_file1)
		os.remove(tmp_file2)
		
		# Return the temp alignment file containing the output from needle
		return tmp_out

