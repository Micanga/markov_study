import sys
from mdp import *
from mdpalg import *

def print_utility(U,rows,cols):
	print U
	print ""

	for i in range(rows):
		for j in range(cols):
			if (i,j) in U:
				print U[(i,j)] ,
			else :
				print None ,
		print ""
	print ""

def print_policy(P,rows,cols):
	print P
	print ""

	for i in range(rows):
		for j in range(cols):
			if (i,j) in P:
				print to_arrow(P[(i,j)]) ,
			else :
				print None ,
		print ""
	print ""

def to_arrow(a):
	if(a == (1,0)):
		return '  v '
	if(a == (-1,0)):
		return '  ^ '
	if(a == (0,1)):
		return '  > '
	if(a == (0,-1)):
		return '  < '
	return '  . '


def main():
	# 1. Game definitions [Based on Russell Reference]
    grid = [[-0.04, -0.04, -0.04, +1], 
    		[-0.04, None,  -0.04, -1], 
    		[-0.04, -0.04, -0.04, -0.04]]
    rows, cols = 3, 4
    start, terminals = (0,0), [(1, 3), (2, 3)]
    actlist = orientations = [(1,0), (0, 1), (-1, 0), (0, -1)]

    # 2. Defining the MDP model for the proposed problem
    grid = grid[::-1]
    mdp = MDP(grid,rows,cols,start,terminals,actlist,orientations,1)

    # 3. Runing the algorithms and printing the results
    print "Reversed Initial Grid"
    mdp.print_grid()
    
    U = value_iteration(mdp,0.0001,50)
    P = policy_iteration(mdp)
    bP = best_policy(mdp,U)

    print "Utily Grid"
    print_utility(U,rows,cols) 
    print ""

    print "Policy Grid"
    print_policy(P,rows,cols)
    print ""

    print "Best Policy Grid"
    print_policy(bP,rows,cols)
    print ""

    # 4. That's all folks ... :)
if __name__ == "__main__":
	main()