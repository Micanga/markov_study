# -*- coding: utf-8 -*-
import sys
import operator, random
import POMDP, POAgent, POMDPAlg
from POMDP import *
from POAgent import *
from POMDPAlg import *

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

	# 1. init a pomdp
    pomdp = POMDP(row,col,grid,terminals,evidence,0.6)
    poagent = POAgent.POAgent(0,0,pomdp)

    # 2. testing
    print(pomdp_value_iteration(poagent,0.01,200))

    # . That's all folks ... :)
if __name__ == "__main__":
	main()