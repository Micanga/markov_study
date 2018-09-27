# -*- coding: utf-8 -*-
import sys
import operator, random
import pomdp, pomdpalg
from pomdp import *
from pomdpalg import *

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
    row, col = 3, 4
    grid = [[-0.04, -0.04, -0.04, -0.04], 
            [-0.04, None,  -0.04, -1], 
            [-0.04, -0.04, -0.04, +1]]
    terminals = [(1, 3), (2, 3)]
    evidence = [[2,    2, 1, 2], 
                [2, None, 1, 1], 
                [2,    2, 1, 2]]
    evidence_probability = [float(4)/float(11),float(7)/float(11)]
    LEFT,RIGHT,UP,DOWN = [0,-1], [0,1], [-1,0], [1,0]
    actions = [LEFT,UP,RIGHT,DOWN]

	# 1. init a pomdp
    pomdp = POMDP(row,col,grid,terminals,actions,evidence,evidence_probability,0.6)

    # 2. testing
    print(pomdp_value_iteration(pomdp,0.01,200))

    # . That's all folks ... :)
if __name__ == "__main__":
	main()