# -*- coding: utf-8 -*-
import sys
import operator, random
from copy import deepcopy
import POMDP
import poagent
import POUCT
import POMCP

def main():
    # MAP
    width, height = 4, 3
    grid = [[-0.04, -0.04, -0.04], 
            [-0.04, -0.04, -0.04], 
            [-0.04, -0.04, -0.04],
            [-0.04, -1   , +1   ]]
    terminals = [(3, 1), (3, 2)]
    evidence = [[2, 1, 2], 
                [1, 0, 1], 
                [1, 0, 1],
                [2, 1, 2]]

    pomdp = POMDP.POMDP(width,height,grid,terminals,evidence,0.9)
    agent = poagent.POAgent('M','l1',10,0,0,0,0,0,pomdp)
    pomcp = POMCP.POMCP(agent,None)

    i = 0
    pomcp.show()
    while(not pomcp.poagent.in_terminal()):
        if(i != 0):
            pomcp.max_iteration = 250
        i = i + 1
        action = pomcp.main_poagent_planning(None)
        print '[ ACTION : ', action , ']'

        new_position = pomcp.poagent.go(pomcp.poagent.position,action)
        pomcp.poagent.forward(action,pomcp.pomdp.evidences[new_position[0]][new_position[1]])

        pomcp.show()
    #pomcp.pouct.print_search_tree()

if __name__ == "__main__":
	main()