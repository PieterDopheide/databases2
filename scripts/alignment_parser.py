#!/usr/bin/python

from Bio import AlignIO

import os
import re
import mysql_dao

class AlignmentParser:
	def parse_alignment(self, a, b, tmp_needle_out):
		# The the content of the alignment file in a variable
		with open(tmp_needle_out, 'r') as c:
			needle_out = c.read()
		# Make several empty lists
		header = list()
		identity = list()
		similarity = list()
		gaps = list()
		
		# Compile several regexes used for getting information out the alignment header
		p_id = re.compile('#\s+(Identity):\s+(\d+)/\d+\s+\(\s*(\d+\.\d)%\)')
		p_sim = re.compile('#\s+(Similarity):\s+(\d+)/\d+\s+\(\s*(\d+\.\d)%\)')
		p_gap = re.compile('#\s+(Gaps):\s+(\d+)/\d+\s+\(\s*(\d+\.\d)%\)')
		# Search the alignment file with the regexes
		m_id = p_id.search(needle_out)
		m_sim = p_sim.search(needle_out)
		m_gap = p_gap.search(needle_out)
		
		# Put the data found with the regexes in the correct empty lists create above
		if m_id:
			identity.append(m_id.group(2))
			identity.append(m_id.group(3))
		if m_sim:
			similarity.append(m_sim.group(2))
			similarity.append(m_sim.group(3))
		if m_gap:
			gaps.append(m_gap.group(2))
			gaps.append(m_gap.group(3))
		
		# Put the lists into one list for ease of passing the data to other functions/classes etc
		header.append(identity)
		header.append(similarity)
		header.append(gaps)
		
		# Use the Biopython parser to parse the alignment file
		alignment = AlignIO.read(tmp_needle_out, 'emboss')
		
		# Remove the (tmp) alignment file
		os.remove(tmp_needle_out)

		self.alignment2db(a, b, alignment, header)
	
	def alignment2db(self, a, b, alignment, header):
		print 'alignment2db'
		# Put alignment in db with mysql_dao.DAO()
		mysql_dao.DAO().store_alignment(a.id, b.id, alignment, header)

