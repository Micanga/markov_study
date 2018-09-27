# -*- coding: utf-8 -*-
import sys
import operator, random

class MDP:

    orientations = [] 

    def __init__(self, grid, rows, cols, start, terminals, actlist, orientations, gamma):
        # 1. init general variables
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.start = start
        self.terminals = terminals
        self.actlist = actlist
        self.orientations = orientations
        self.gamma = gamma
        self.reward = {}
        self.states = set()
        
        # 2. init states and rewards
        for x in range(self.rows):
            for y in range(self.cols):
                self.reward[x, y] = grid[x][y]
                if grid[x][y] is not None:
                    self.states.add((x, y))

        # 3. sorting the states and rewards
        self.states = sorted(self.states)

    def R(self, state):
        return self.reward[state]

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, self.turn_right(action))),
                    (0.1, self.go(state, self.turn_left(action)))]

    def go(self, state, direction):
        "Return the state that results from going in this direction."
        state1 = tuple(map(operator.add, state, direction))
        if(state1 in self.states):
            return state1
        else:
            return state

    def turn_right(self,orientation):
        return self.orientations[(self.orientations.index(orientation)+1) % len(self.orientations)]

    def turn_left(self,orientation):
        return self.orientations[(self.orientations.index(orientation)-1)]

    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist

    def print_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print self.grid[i][j] ,
            print ""
        print ""