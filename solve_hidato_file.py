#!/usr/bin/python3

import optparse
from Hidato import *

def main():
	# Deal with command-line arguements.
	parser = optparse.OptionParser()

	parser.set_defaults(verbose = False)
	parser.set_defaults(debug = False)

	parser.add_option("-P", "--puzzle",
					help="file, Hidato puzzle",
                    metavar="FILE", type="string", dest="puzzle_file")
	parser.add_option("-v", "--verbose",
					help="verbose",
                    action="store_true", dest="verbose")
	parser.add_option("-D", "--debug",
					help="debug",
                    action="store_true", dest="debug")

	(options, args) = parser.parse_args()

	# Validate arguements.
	if not options.puzzle_file:
		parser.error("must specify a filename for the Hidato puzzle")

	# Create the Hidato object from the filename.
	this_puzzle = Hidato(options.puzzle_file)

	this_puzzle.hidato_solve()

# Run this module.
if __name__ == "__main__":
	main()


