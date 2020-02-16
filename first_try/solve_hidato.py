#!/usr/bin/python

import logging, sys

#   NAME: find_adj_cells
#  INPUT: cell location
# OUTPUT: list of cell locations
# DESCRIPTION:
#    Return a list of all cell locations adjacent to this one.
def find_adj_cells( numsForCell, pos ) :
	x, y = pos
	retVal = []

	logging.debug( '+++ finding all free cells adjacent to %s...', pos )

	for x2 in [ x - 1, x, x + 1 ] :
		for y2 in [ y - 1, y, y + 1 ] :
			if (x2, y2) in numsForCell.keys() and \
										len( numsForCell[(x2,y2)] ) > 1 :
				retVal.append( (x2,y2) )
				
	logging.debug( '+++ all free cells adjacent to %s: %s', pos, retVal )

	return retVal

#   NAME: fix_pair
#  INPUT: number to fix, location to fix it to
# OUTPUT: none
# DESCRIPTION:
#    Fix a number to a location.  Remove all other occurences of that
#    number in the numsForCell dictionary.  Remove all other occurences
#    of the location in the cellsForNum dictionary.
def fix_pair( numsForCell, cellsForNum, unusedCells, unusedNums, num, loc ) :

	# Fix the location to the number.
	logging.debug( '=== FIXING %s to %d...', loc, num )
	cellsForNum[num] = [ loc ]

	# Remove the number and location from their unused* dictionaries.
	if loc in unusedCells :
		logging.debug( ' == REMOVING %s from unusedCells...', loc )
		logging.debug( ' == Before: %s', unusedCells )
		unusedCells.remove( loc )
		logging.debug( ' ==  After: %s', unusedCells )
	if num in unusedNums :
		logging.debug( ' == REMOVING %d from unusedNums...', num )
		logging.debug( ' == Before: %s', unusedNums )
		unusedNums.remove( num )
		logging.debug( ' ==  After: %s', unusedNums )

	# Remove all other occurences of that location in every other
	# entry in cellsForNum.
	for n in cellsForNum.keys() :
		if n != num and loc in cellsForNum[n] :
			logging.debug( ' == REMOVING %s from cellsForNum[%d]...', loc, n )
			logging.debug( ' == Before: %s', cellsForNum[n] )
			cellsForNum[n].remove( loc )
			logging.debug( ' ==  After: %s', cellsForNum[n] )

			# Did *this* action in turn cause another fix to happen?
			if len( cellsForNum[n] ) == 1 :
				# cool!
				logging.debug( '!!! cellsForNum[%d] now fixable', n )
				fix_pair( numsForCell, cellsForNum, unusedCells, unusedNums, \
														n, cellsForNum[n][0] )

	logging.debug( '=== FIXING %d to %s...', num, loc )

	# Fix the number to the location.
	numsForCell[loc] = [ num ]

	# Remove all other occurences of that location in every other
	# entry in cellsForNum.
	for l in numsForCell.keys() :
		if l != loc and num in numsForCell[l] :
			logging.debug( ' == REMOVING %d from numsForCell[%s]...', num, l )
			logging.debug( ' == Before: %s', numsForCell[l] )
			numsForCell[l].remove( num )
			logging.debug( ' ==  After: %s', numsForCell[l] )

			# Did *this* action in turn cause another fix to happen?
			if len( numsForCell[l] ) == 1 :
				# cool!
				logging.debug( '!!! numsForCell[%s] is now fixable', l )
				fix_pair( numsForCell, cellsForNum, unusedCells, unusedNums, \
														numsForCell[l][0], l )

	return

#   NAME: is_fixed
#  INPUT: number
# OUTPUT: true/false
# DESCRIPTION:
#    Return true if the number is a key in cellsForNum and has only
#    one location associated with it, false otherwise.
def is_fixed( cellsForNum, num ) :
	return num in cellsForNum.keys() and len( cellsForNum[num] ) == 1

#   NAME: remove_possibilities
#  INPUT: number, list of cell locations
# OUTPUT: count of valid changes made
# DESCRIPTION:
#    Remove the possiblity of num <-> location from both cellsForNum and
#    numsForCell for each location in locList.
def remove_possibilities( numsForCell, cellsForNum, unusedCells, unusedNums, \
															num, locList ) :
	change_count = 0

	for loc in locList :
		if num in numsForCell[loc] and len( numsForCell[loc] ) > 1 :
			logging.debug( '*** Removing %d from numsForCell[%s]', num, loc )
			logging.debug( '  * BEFORE: %s', numsForCell[loc] )
			numsForCell[loc].remove(num)
			logging.debug( '  *  AFTER: %s', numsForCell[loc] )
			change_count += 1

		if len( numsForCell[loc] ) == 1 :
			logging.debug( 'numsForCell[%s] is now fixable', loc )
			fix_pair( numsForCell, cellsForNum, unusedCells, unusedNums, \
													numsForCell[loc][0], loc )

		if loc in cellsForNum[num] and len( cellsForNum[num] ) > 1 :
			logging.debug( '*** Removing %s from cellsForNum[%d]', loc, num )
			logging.debug( '  * BEFORE: %s', cellsForNum[num] )
			cellsForNum[num].remove(loc)
			logging.debug( '  *  AFTER: %s', cellsForNum[num] )
			change_count += 1

		if len( cellsForNum[num] ) == 1 :
			logging.debug( 'cellsForNum[%d] is now fixable', num )
			fix_pair( numsForCell, cellsForNum, unusedCells, unusedNums, \
													num, cellsForNum[num][0] )

	return change_count

#   NAME: solve_hidato
#  INPUT: cellsForNum dictionary, numsForCell dictionary, maximum difficulty
#         level for which to solve
# OUTPUT: modified cellsForNum dictionary, modified numsForCell dictionary
# DESCRIPTION:
def solve_hidato( cellsForNum, numsForCell, difficulty ) :
	# Determine the cells that are unfixed.
	unusedCells = [ c for c in numsForCell.keys() if len(numsForCell[c]) != 1 ]

	# Determine the numbers that are unfixed.
	unusedNums = [x + 1 for x in range(len(numsForCell)) if \
											x + 1 not in cellsForNum.keys() ]

	for c in unusedCells :
		# The weird slicing done here is to make a copy by value of the list
		# rather than the default copy by reference.
		numsForCell[c] = unusedNums[:]

	for n in unusedNums :
		# The weird slicing done here is to make a copy by value of the list
		# rather than the default copy by reference.
		cellsForNum[n] = unusedCells[:]

	logging.debug( 'INITIAL numsForCell: %s', numsForCell )
	logging.debug( 'INITIAL cellsForNum: %s', cellsForNum )

	# Wonderful!  Now, apply techniques until the board is solved or doesn't
	# change any more.
	changes = 1
	while changes > 0 :
		changes = 0

		# SIMPLE TECHNIQUES
		# =================

		# This is a base solving technique.  Use it at any difficulty level.

		# Look for a Single Path anywhere in the board.
		#
		# To find it:
		# - find each unfixed number
		# - construct a list of possible locations for the unfixed number
		#   based on the numbers one more and one less that it that are
		#   fixed
		# - use that list to prune the dictionaries
		for n in unusedNums :
			logging.debug( 'Examining unusedNum = %d:%s', n, cellsForNum[n] )

			if is_fixed( cellsForNum, n - 1 ) :
				logging.debug( '%d:%s is fixed', n - 1, cellsForNum[n-1] )

				adjCells = find_adj_cells( numsForCell, cellsForNum[n-1][0] )
				badLocs = [ x for x in cellsForNum[n] if x not in adjCells ]
				logging.debug( 'no longer possible for %d -> %s', n, badLocs )

				changes += remove_possibilities( numsForCell, cellsForNum, \
										unusedCells, unusedNums, n, badLocs )
			if is_fixed( cellsForNum, n + 1 ) :
				logging.debug( '%d:%s is fixed', n + 1, cellsForNum[n+1] )

				adjCells = find_adj_cells( numsForCell, cellsForNum[n+1][0] )
				badLocs = [ x for x in cellsForNum[n] if x not in adjCells ]
				logging.debug( 'no longer possible for %d -> %s', n, badLocs )
				changes += remove_possibilities( numsForCell, cellsForNum, \
										unusedCells, unusedNums, n, badLocs )

		# Use this technique if difficulty > 1
		if( difficulty > 1 ) :
			pass

		# Was there, after all that, a change?
		logging.debug( 'END OF WHILE LOOP: changes = %d', changes )

	logging.debug( 'FINAL cellsForNum: %s', cellsForNum )
	logging.debug( 'FINAL numsForCell: %s', numsForCell )

	return [ cellsForNum, numsForCell ]
