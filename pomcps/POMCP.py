import POUCT
import commonMethods
from copy import deepcopy
from math import sqrt, log

class POMCP:

	def __init__(self,poagent, search_tree ,max_iteration = 1000, max_depth = 10):
		self.pouct = POUCT.POUCT(poagent,search_tree)
		self.poagent = poagent
		self.pomdp = poagent.pomdp
		self.max_iteration = max_iteration
		self.max_depth = max_depth

	def main_poagent_planning(self, agents_parameter_estimation):
		# 1 Taking the best action to the current agent params
		print 'Starting Planning: 3 steps\n- Step 1/3 : Searching for best movement'
		best_node,next_move = self.pomcp_planning()

		# 2. Updating the search_tree
		print '- Step 2/3 : Updating the Tree'
		self.pouct.search_tree.root.show()
		for child in self.pouct.search_tree.root.child_nodes:
			if child is not best_node:
				self.pouct.search_tree.destroy_from(child)
			else:
				child.depth = 0
				self.pouct.search_tree.update_depth_from(child)

		# 3. Killing the old root
		print('- Step 3/3 : Killing old root')
		self.pouct.search_tree.root = best_node
		self.pouct.search_tree.root.parent.child = None
		self.pouct.search_tree.root.parent = None
		self.pouct.search_tree.root.show()

		# 4. Returning the results
		return next_move#, self.pouct.search_tree

	def pomcp_planning(self):
		# 1. planning
		it, dp = 0, 0
		while it < self.max_iteration:
			if(it % 100 == 0):
				print it,'/',self.max_iteration
			# a. reinitializing the depth
			dp = 0

			# b. building a copy of main agent
			# to run the simulations
			sim_agent = deepcopy(self.poagent)

			# c. running the current simulation
			# to reach the max depth or to find
			# a terminal state
			while dp < self.max_depth and not sim_agent.in_terminal():
				# ii. running the pomcp search
				self.search(sim_agent,dp)

				# i. selecting a action and getting the new agent
				# position
				action = sim_agent.random_action()
				new_position = sim_agent.go(sim_agent.position,action)
				sim_agent.forward(action,self.pomdp.evidences[new_position[0]][new_position[1]])
				dp = dp + 1
			it = it + 1

		#2. Returning the best node/action to the poagent history
		best_node, best_action = POUCT.Node(1,-99999,0,dict(),[],0,None),'L'
		poagent_node = self.pouct.search_history(self.poagent.history)
		for b in poagent_node.child_nodes:
			if(best_node.value < b.value):
				best_node = b
				best_action = b.history[len(b.history)-1]

		return best_node, best_action

	def search(self,poagent,dp):
		# 1. Simulating
		self.simulate(poagent,dp)

		# 2. Returning the optimum/max value
		cur_node = None
		best_node, best_action = POUCT.Node(1,-99999,0,dict(),[],0,None),'L'
		for a in poagent.possible_actions():
			hb = deepcopy(poagent.history)
			hb.append(a)
			cur_node = self.pouct.search_history(hb)
			if cur_node.value > best_node.value and cur_node != self.pouct.search_tree.root:
				best_node = cur_node
				best_action = a

		return best_action,best_node

	def evaluate_rollout(self,poagent,found_node):
  		action = poagent.history[len(found_node.history)-1]
  		new_h = deepcopy(found_node.history)
  		new_h.append(action)
  		next_node = POUCT.Node(1,0,0,dict(),new_h,found_node.depth+1,None)
		return next_node

  	def evaluate_simulate(self,po,found_node):
  		tmp_agent = deepcopy(self.poagent)
		for dp in range(0,len(found_node.history)):
			action = found_node.history[dp]
			new_position = tmp_agent.go(tmp_agent.position,action)
			tmp_agent.forward(action,self.pomdp.evidences[new_position[0]][new_position[1]])

  		for a in tmp_agent.possible_actions():
  			new_h = deepcopy(found_node.history)
  			new_h.append(a)
  			found_node.add_child(1,0,0,dict(),new_h)
  		found_node = self.pouct.search_history(po.history)
		return found_node

	def simulate(self,poagent,depth):
		# 1. depth verification
		if depth > self.max_depth:
			return 0

		if poagent.in_terminal():
			return 0 #poagent.belief_reward()

		# 2. if the history doesn't exist in the search tree
		#add the history/node and bring the answer by rollout
		found_node = self.pouct.search_history(poagent.history)
		if(poagent.history != found_node.history or found_node.child_nodes == []):
			# a. adding the new possible nodes and rolling out to
			#	calculates the your value
			found_node = self.evaluate_simulate(poagent,found_node)
			return self.rollout(found_node)

		# 3. else we update our node
		c, gamma = 1, poagent.pomdp.gamma
		
		# a. taking the best action : Q-function
		# a <- argmax V(hb) + c sqrt( log(N(h)) / N(hb))
		best_action_value = -99999
		best_action = 'L'
		for hb in found_node.child_nodes:
			cur_action = hb.value + c*sqrt(log(found_node.visits))/hb.visits
			if(best_action_value == -99999 or best_action_value < cur_action):
				best_action_value = cur_action
				best_action = hb.history[len(hb.history)-1]

		# b. updating the agent belief states
		# (s',o,r) ~ G(s,a)
		tmp_agent = deepcopy(poagent)
		new_position = tmp_agent.go(tmp_agent.position,best_action)
		tmp_agent.forward(best_action,self.pomdp.evidences[new_position[0]][new_position[1]])
		next_state = tmp_agent.belief_states

		# c. calculating the reward
		# R <- r + gamma*SIMULATE(s',hao,depth+1)
		reward = tmp_agent.belief_reward() + gamma*self.simulate(tmp_agent,found_node.depth+1)

		# d. updating node info
		# N(h) <- N(h) + 1
		found_node.visits = found_node.visits + 1
		for b in found_node.child_nodes:
			if best_action == b.history[len(b.history)-1] :
				# N(ha) <- N(ha) + 1
				b.visits = b.visits + 1

				# V(ha) <- V(ha) + (R-V(ha))/N(ha)
				nha = b.visits
				vha = b.value
				b.value = vha + (reward - vha)/nha

				b.reward = reward
				break

		return reward
		

	def rollout(self,found_node):
		if(found_node.depth > self.max_depth):
			return 0

		# a. taking the next action using random policy
		tmp_agent = deepcopy(self.poagent)
		for dp in range(0,len(found_node.history)):
			action = found_node.history[dp]
			new_position = tmp_agent.go(tmp_agent.position,action)
			tmp_agent.forward(action,self.pomdp.evidences[new_position[0]][new_position[1]])

		if tmp_agent.in_terminal():
			return 0 #tmp_agent.belief_reward()

		# a ~ pi(h)
		action = tmp_agent.random_action()
		new_position = tmp_agent.go(tmp_agent.position,action)
		# (s',o,r) ~ G(s,a)
		tmp_agent.forward(action,self.pomdp.evidences[new_position[0]][new_position[1]])

		# b. adding the new node and rolling out to calculates the policy
		next_node = self.evaluate_rollout(tmp_agent,found_node)

		reward = tmp_agent.belief_reward() + tmp_agent.pomdp.gamma*self.rollout(next_node)
		found_node.reward = reward 

		return reward
	
	def show(self):
		for x in range(self.pomdp.map_dimension[0]):
			for y in range(self.pomdp.map_dimension[1]):
				if self.poagent.position != (x,y):
					print '|\t \t|',
				else:
					print '|\tM\t|',
			print '\n'