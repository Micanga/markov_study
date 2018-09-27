# -*- coding: utf-8 -*-
import sys
import operator, random

class POMDP():

	def __init__(self,nrow,ncol,problem_map,terminals, actions, evidence,prob_e,gamma):
		# 0. self constants definition
		self.ROW = 0
		self.COL = 1

		# 1. def the map
		self.terminals = terminals
		self.problem_map =  problem_map
		self.map_dimension = [nrow,ncol]

		# 2. init the mdp components
		self.reward = {}
		self.ret = {}
		self.history = []
		self.states  = set()
		for x in range(self.map_dimension[self.ROW]):
			for y in range(self.map_dimension[self.COL]):
				self.reward[(x, y)] = self.problem_map[x][y]
				self.ret[(x,y)] = self.problem_map[x][y]
				if self.problem_map[x][y] is not None:
					self.states.add((x, y))
		self.actions = actions
		self.gamma = gamma
		self.t = 0

		# 3. init the pomdps components
		self.evidence =  evidence
		self.prob_e = prob_e
		self.belief = dict([(s,1.0/float((len(self.states)-len(self.terminals))) if s not in self.terminals else 0) for s in self.states])

	def T(self, state, action):
		if action == None:
			return [(0.0, state)]
		else:
			return [(0.8, self.go(state, action)),
					(0.1, self.go(state, self.turn_right(action))),
					(0.1, self.go(state, self.turn_left(action)))]

	def go(self, state, direction):
		state1 = tuple(map(operator.add, state, direction))
		if(state1 in self.states):
			return state1
		else:
			return state

	def turn_right(self,a):
		return self.actions[(self.actions.index(a)+1) % len(self.actions)]

	def turn_left(self,a):
		return self.actions[(self.actions.index(a)-1) % len(self.actions)]

	def actions(self, state):
		if state in self.terminals:
			return [None]
		else:
			return self.actions

	def R(self, state):
		return self.reward[state]

	def O(self,s1):
		return self.prob_e[self.evidence[s1[self.ROW]][s1[self.COL]]-1]

	def forward(self, action, evidence):
		new_belief = dict([(s, 0) for s in self.states])
		for s in self.states:
			for (p,s1) in self.T(s,action):
				new_belief[s1] = new_belief[s1] + (p*self.belief[s])

		sum_ = 0
		for s1 in new_belief:
			new_belief[s1] = new_belief[s1]*self.O(s1)
			sum_ = sum_ + new_belief[s1]

		for s1 in new_belief:
			new_belief[s1] = new_belief[s1]*(1.0/sum_)

		sum_ = 0
		for s1 in new_belief:
			sum_ = sum_ + new_belief[s1]

		self.history.append((self.actions.index(action),evidence))
		self.belief = new_belief
		self.t = self.t + 1
		print(self.belief)
		for s in new_belief:
			self.ret[s] = self.gamma*self.ret[s] + self.belief_reward()

	def belief_reward(self):
		sum_ = 0
		for s in self.states:
			sum_ = sum_ + (self.R(s)*self.belief[s])
		return sum_

	def V(self,state):
		return self.belief_reward() + self.ret[state]

	def print_belief(self):
		for i in range(self.map_dimension[self.ROW]):
			for j in range(self.map_dimension[self.COL]):
				if (i,j) in self.belief:
					print self.belief[(i,j)] ,
				else:
					print 'Noneeeeeeeeeee' ,
			print ""
		print ""