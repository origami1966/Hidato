#!/usr/bin/python

# The big ol' wrapper script for the hidato program suite.  From here, a
# hidato puzzle can be generated, or a puzzle can be solved.

import getopt, logging, sys
from parse_hidato_file import parse_hidato_file
from solve_hidato import *
from copy import deepcopy

def main():
	# Parse the options on the command line.
	try:
		opts, args = getopt.getopt( sys.argv[1:], "D:F:P:c:d:hr:", ["help"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	# Manage the parsed options.
	puzzle_filename = None
	difficulty = 1

	for o, a in opts :
		if o == "-D" :
			logger = logging.getLogger()
			if a in ( 'debug', 'Debug', 'DEBUG' ) :
				logger.setLevel( logging.DEBUG )
			elif a in ( 'info', 'Info', 'INFO' ) :
				logger.setLevel( logging.INFO )
		elif o == "-r" :
			rows = int( a )
		elif o == "-c" :
			columns = int( a )
		elif o == "-d" :
			difficulty = int( a )
		elif o == "-F" :
			filename = a
		elif o == "-P" :
			puzzle_filename = a
		elif o in ("-h", "--help") :
			usage()
			sys.exit()
		else:
			assert False, "unhandled option"


	# What is this a call for?
	if puzzle_filename :
		origCellsForNum, origNumsForCell = parse_hidato_file( puzzle_filename )
		cellsForNum = deepcopy( origCellsForNum )
		numsForCell = deepcopy( origNumsForCell )
		
		cellsForNum, numsForCell = solve_hidato( cellsForNum, numsForCell, \
																difficulty )
		print origCellsForNum
		print origNumsForCell
		print cellsForNum
		print numsForCell

	return

#   NAME: usage
#  INPUT: none
# OUTPUT: none
# DESCRIPTION:
#    Print a usage message, then exit with the supplied
def usage() :
#USAGE:
#        hidato [-D <severity>] [-r <row#> -c <column#>] [-d <1-5>]
#		hidato [-D <severity>] -F <filename> [-d <1-5>]
#		hidato [-D <severity>] -P <filename> [-d <1-5>]
	return

if __name__ == "__main__":
    main()

