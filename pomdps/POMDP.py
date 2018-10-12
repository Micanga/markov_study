# -*- coding: utf-8 -*-
import sys
import operator, random

class POMDP:

	global width, height
	width = 1
	height = 0

	def __init__(self,row,col,problem_map,terminals, evidences,gamma):
		# 1. def the map
		self.problem_map =  problem_map # grid with rewards
		self.terminals = terminals		# array with problem terminals
		self.map_dimension = [row,col]# size of the grid

		# 2. init the mdp components
		self.reward = {}
		self.ret = {}
		self.states  = set()
		for r in range(self.map_dimension[height]):
			for c in range(self.map_dimension[width]):
				self.reward[(r, c)] = self.problem_map[r][c]
				self.ret[(r,c)] = self.problem_map[r][c]
				if self.problem_map[r][c] is not None:
					self.states.add((r, c))

		# 3. init the pomdps components
		self.evidences =  evidences 	# grid with all evidences in each state
		self.evidences_list = {}
		for r in range(self.map_dimension[height]):
			for c in range(self.map_dimension[width]):
				if self.evidences[r][c] not in self.evidences_list:
					ne = self.count_evidence(self.evidences[r][c])
					self.evidences_list[self.evidences[r][c]] = (1.0/ne)
		self.gamma = gamma
		self.belief = dict([(s,1.0/float((len(self.states)-len(self.terminals))) if s not in self.terminals else 0) for s in self.states])

	def R(self, state):
		return self.reward[state]

	def O(self,s1):
		return self.evidences_list[self.evidences[s1[0]][s1[1]]]

	def count_evidence(self,e):
		ne = 0
		for x in range(self.map_dimension[0]):
			for y in range(self.map_dimension[1]):
				if self.evidences[x][y] == e:
					ne = ne + 1
		return float(ne)

	def show(self):
		for x in range(self.map_dimension[0]):
			for y in range(self.map_dimension[1]):
				print self.problem_map[x][y],self.evidences[x][y], '\t',
			print '\n'