from numpy.random import choice
import operator
import numpy as np
from numpy.random import choice
from math import sqrt

class POAgent:

	def __init__(self, x = 0, y = 0,pomdp = None):
		# 1. Agent Localization and Orientation
		self.start_position = (int(x), int(y))
		self.position = (int(x), int(y)) #used only for mapping and simulating a real
											#environment (e.g., distance calculation by sensors)
		self.pomdp = pomdp
		self.belief_states = pomdp.belief

		# 3. Agent Intelligence and Sensoring
		self.t = 0
		self.history = []

		# 4. Markov Problem Parameters
		self.actions = ['N','E','S','W']
		self.actions_probability = {'N': 0.20, 'E': 0.20, 'S': 0.20, 'W': 0.20}
		self.next_action = None
	
	####################################################
	#   GET FUNCTIONS   ################################
	####################################################
	""" get_belief_states """
	def get_belief_states(self):
		return self.belief_states

	""" get_history """
	def get_history(self):
		return self.history

	def belief_reward(self):
		sum_ = 0
		for s in self.pomdp.states:
			sum_ = sum_ + (self.pomdp.R(s)*self.belief_states[s])
		return sum_

	##########################################################
	#   AGENT MOVEMENT AND INTELLIGENCE FUNCTIONS   ##########
	##########################################################

	def in_terminal(self):
		if(self.position in self.pomdp.terminals):
			return True
		else:
			return False

	def possible_actions(self):
		possible_actions = []
		for a in self.actions:
			for (p,s) in self.T(self.position,a):
				if s != self.position:
					possible_actions.append(a)
		return possible_actions

	def random_action(self):
		possible_actions = self.possible_actions()
		return choice(possible_actions)

	def go(self,state,action):
		direction = {'N': (1,0), 'E': (0,1), 'S': (-1,0), 'W': (0,1)}
		state1 = tuple(map(operator.add, state, direction[action]))
		if(state1 in self.pomdp.states):
			return state1
		else:
			return state

	def go_for_sure(self,state,action):
		direction = {'N': (1,0), 'E': (0,1), 'S': (-1,0), 'W': (1,0)}
		state1 = tuple(map(operator.add, state, direction[action]))
		if(state1 in self.pomdp.states):
			return state1
		else:
			return state

	def turn_left(self,a):
		return self.actions[(self.actions.index(a)-1) % len(self.actions)]

	def turn_right(self,a):
		return self.actions[(self.actions.index(a)+1) % len(self.actions)]

	def T(self, state, action):
		if action == None:
			return [(0.0, state)]
		else:
			return [(0.8, self.go(state,action)),
						(0.1,self.go(state,self.turn_left(action))),
						(0.1,self.go(state,self.turn_right(action)))]

	def Pes(self,e,s1):
		if(e != self.pomdp.evidences[s1[0]][s1[1]]):
			return 0
		else:
			return 1

	def forward(self, action, evidence):
		new_belief = dict([(s, 0) for s in self.pomdp.states])

		# Sum of T(s1|s,a)*b(s) for all s -- Equation (1)
		for s in self.pomdp.states:
			for (p,s1) in self.T(s,action):
				new_belief[s1] = new_belief[s1] + (p*self.belief_states[s])

		# P(e|s')*(1)   -- Equation (2)
		sum_ = 0
		for s1 in new_belief:
			new_belief[s1] = self.Pes(evidence,s1)*new_belief[s1]
			sum_ = sum_ + new_belief[s1]

		# alpha*(2)	 -- Equation (3) - Normalization
		for s1 in new_belief:
			if(sum_ != 0):
				new_belief[s1] = new_belief[s1]*(1.0/sum_)
			else:
				new_belief[s1] = 0

		# 1. Updating agent information
		self.belief_states = new_belief
		self.t = self.t + 1
		width = self.pomdp.map_dimension[0]
		height = self.pomdp.map_dimension[1]
		self.position = self.go_for_sure(self.position,action)
		self.history.append(action)

		# 2. Updating POMDP information
		for s in new_belief:
			self.pomdp.ret[s] = self.pomdp.gamma*self.pomdp.ret[s] + self.belief_reward()

	def V(self,state):
		return self.belief_reward() + self.pomdp.ret[state]

	def print_belief(self):
		for i in range(self.pomdp.map_dimension[0]):
			for j in range(self.pomdp.map_dimension[1]):
				if (i,j) in self.belief_states:
					print self.belief_states[(i,j)] ,
				else:
					print 'Noneeeeeeeeeee' ,
			print ""
		print ""