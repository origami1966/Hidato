#!/usr/bin/python

from string import split
import re

# parse_hidato_file
#  INPUT: text file representing hidato board
# OUTPUT: list containing cellsForNum dictionary and numsForCell dictionary
# DESCRIPTION:
#   Read in the description file and use it to initialize the two dictionaries
#   that will be used for solving the board.
def parse_hidato_file( filename ):
	rows = columns = 0;
	r = c = 0;
	numsForCell = {}
	cellsForNum = {}

	fptr = open( filename, 'r' )

	for line in fptr :
		# FIX ME; remove comments from input file?

		for elem in split( line ) :
			# The plan is to do these steps in this order:
			# - If row hasn't yet been set, set it.
			# - If column hasn't yet been set, set it.
			# - If it's a "number+", fix it in cellsForNum and numsForCell.
			# - If it's a "number", put a blank list into numsForCell.
			#   (That's to make sure we know all the valid cells for this
			#   gameboard.)
			# - Skip it otherwise.
			# After all that, increment the counters for current row/column.
			if rows == 0 :
				rows = int( elem )
				continue
			elif columns == 0 :
				columns = int( elem )
				continue
			elif re.match( r"\d+\+$", elem ) :
				num = int( re.match(r"(\d+)\+$", elem).group(1) )
				cellsForNum[num] = [ (r, c) ]
				numsForCell[ (r,c) ] = [ num ]
			elif re.match( r"\d+$", elem ) or re.match( r"\.+$", elem ) :
				numsForCell[ (r,c) ] = []
			else :
				# If the execution made it down to here, something
				# was hit that wasn't a number or a number hint.
				# Without installing complicated error checking,
				# assume it's one of the black/blank cells and
				# move along.
				pass

			# Update the row/column counters.
			c = (c + 1) % columns
			if c == 0 :
				r = r + 1

	return [ cellsForNum, numsForCell ]


