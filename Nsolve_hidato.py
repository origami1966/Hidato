#!/usr/bin/python3

# Let's try this simply: an NxN array with N^2 cells.  Each cell has a possible
# list of all N^2 numbers.  Keep whittling down that list until only the
# solution exists.
#
# This contains only the most basic of solvers, a forced chain/forced cell
# strategy.

def print_board(full=False):
	for r in range(board_size):
		for c in range(board_size):
			if( len(gameboard[r][c]) == 1 ):
				print(gameboard[r][c][0], end=' ')
			elif( full == True ):
				print(gameboard[r][c], end=' ')
			else:
				print('.', end=' ')
		print()
	print()

def init_simple():
	for r in range(board_size):
		for c in range(board_size):
			if( len(gameboard[r][c]) == 1 ):
				prune_possible(gameboard[r][c][0], r, c)

def prune_possible( v, in_r, in_c ):
	print( 'prune_possible():', v, in_r, in_c )
	for r in range(board_size):
		for c in range(board_size):
			if( r == in_r and c == in_c ):
				next
			elif( v in gameboard[r][c] ):
				gameboard[r][c].remove(v)

	print_board(full=True)
	
def prune_distant_possible( v, in_r, in_c ):
	print('prune_distant_possible():', v, in_r, in_c)
	for this_v in [v+1, v-1]:
		for r in range(board_size):
			for c in range(board_size):
				#print('prune_distant_possible(): checking ', this_v, r, c)
				if( abs(r - in_r) <= 1 and abs(c - in_c) <= 1 ):
					next
				elif( this_v in gameboard[r][c] ):
					#print('trying to remove it')
					gameboard[r][c].remove(this_v)

	print_board(full=True)
	
def prune_cell_containing( in_v ):
	print( 'prune_cell_containing()', in_v )
	for r in range(board_size):
		for c in range(board_size):
			if( in_v in gameboard[r][c] ):
				gameboard[r][c] = [in_v]
				print_board(full=True)
				return

board_size = 3

all_numbers = [x + 1 for x in range(board_size**2)]

gameboard = [ [all_numbers[:] for c in range(board_size)]
									for r in range(board_size) ]

print_board()

# Set up a simple puzzle.
gameboard[0][0] = [1]
gameboard[0][2] = [5]
gameboard[2][0] = [8]
gameboard[2][2] = [3]

print_board()

# Initialize simple: remove the fixed numbers from all possible numbers.
init_simple()

repeat = True
while( repeat == True ):
	repeat = False

	# Do neighbors 1-deep.  If a cell has a fixed value, the neighbors before
	# and after it must be next to it.  Remove the neighbors from all possible
	# value lists in all non-neighboring cells.
	for r in range(board_size):
		for c in range(board_size):
			if( len(gameboard[r][c]) == 1 ):
				fixed_v = gameboard[r][c][0]
				prune_distant_possible(fixed_v, r, c)

	# There might now be a list of possible values in a cell on the gameboard
	# with a member that appears only in that list.  If so, then that possible
	# values list should be reduced to that number.
	for v in all_numbers:
		v_count = 0
		for r in range(board_size):
			for c in range(board_size):
				if( v in gameboard[r][c] and len(gameboard[r][c]) != 1 ):
					# This test finds single definitions but bypasses
					# already fixed values by passing back a 0.
					v_count += 1

		if( v_count == 1 ):
			prune_cell_containing( v )
			repeat = True

print_board()


