from numpy.random import choice
import position
import operator
import numpy as np
from numpy.random import choice
from math import sqrt
import parameter_estimation
import commonMethods
import sensor

class POAgent:

    def __init__(self, index='0', agent_type='l1', level = 0, x = 0, y = 0, radius = 0, angle = 0, direction = 0,pomdp = None):
        # 1. Agent Identification and Features
        self.index = index
        self.agent_type = agent_type
        self.level = float(level)

        # 2. Agent Localization and Orientation
        self.start_position = (int(x), int(y))
        self.position = (int(x), int(y)) #used only for mapping and simulating a real
                                            #environment (e.g., distance calculation by sensors)
        self.pomdp = pomdp
        self.belief_states = pomdp.belief
        self.radius = float(radius)
        self.co_radius = sqrt(pomdp.map_dimension[0] ** 2 + pomdp.map_dimension[1] ** 2)
        self.angle = float(angle)
        self.co_angle = 2 * np.pi

        if isinstance(direction, basestring):
            self.direction = self.convert_direction(direction)
        else:
            self.direction = float(direction)

        # 3. Agent Intelligence and Sensoring
        self.t = 0
        self.history = []
        self.route_actions = None
        self.visible_agents = []
        self.visible_items = []
        self.item_to_load = -1

        # 4. Markov Problem Parameters
        self.actions = ['L','N','E','S','W']
        self.actions_probability = {'L': 0.20, 'N': 0.20, 'E': 0.20, 'S': 0.20, 'W': 0.20}
        self.next_action = None
        self.state_dim = []
    
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
    #   UTILS FUNCTIONS   ####################################
    ##########################################################
    """ print_agent """
    def print_agent(self):
        print '>>>>> Agent' + ' ' + str(self.index) + ' <<<<<<'
        print '-- type and level : ' + str(self.agent_type) + ' ' + str(self.level)
        print self.get_belief_states()
        print '-- radius and angle : ' + str(self.radius) + ' ' + str(self.co_radius) + ' ' + str(self.angle) + ' ' + str(self.co_angle)
        print '-- direction : ' + str(self.direction)

        print '-- history - route act - visible ag and item - item load'
        print self.get_history()
        print self.route_actions
        print self.visible_agents
        print self.visible_items
        print self.item_to_load

        # 4. Markov Problem Parameters
        print '-- actions prob - next action - state dim'
        print self.actions_probability
        print self.next_action
        print self.state_dim

        print '>>>>>>>>>><<<<<<<<<<'

    ##########################################################
    #   AGENT MOVEMENT AND INTELLIGENCE FUNCTIONS   ##########
    ##########################################################
    def find_nearest_visible_item(self, items):
        minimum_distance = 10000
        nearest_item_index = -1
        view = visible_agents_items()

        for i in range(0, len(items)):
            if not items[i].loaded and item[i] in view:
                item = items[i]
                (xI, yI) = item.position.get_position()
                if sensor.distance(self,item) < minimum_distance:
                    minimum_distance = sensor.distance(self,item)
                    nearest_item_index = i

        return nearest_item_index

    def in_terminal(self):
        if(self.position in self.pomdp.terminals):
            return True
        else:
            return False

    def go(self,state,action):
        direction = {'L': (0,0), 'N': (0,1), 'E': (1,0), 'S': (0,-1), 'W': (-1,0)}
        state1 = tuple(map(operator.add, state, direction[action]))
        if(state1 in self.pomdp.states):
            return state1
        else:
            return state

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

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(self.actions_probability[action], self.go(state,action))]

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

        # alpha*(2)     -- Equation (3) - Normalization
        for s1 in new_belief:
            new_belief[s1] = new_belief[s1]*(1.0/sum_)

        # 1. Updating agent information
        self.belief_states = new_belief
        self.t = self.t + 1
        width = self.pomdp.map_dimension[0]
        height = self.pomdp.map_dimension[1]
        self.position = commonMethods.new_position_with_given_action(self,width,height,action)
        self.history.append(action)

        # 2. Updating POMDP information
        for s in new_belief:
            self.pomdp.ret[s] = self.pomdp.gamma*self.pomdp.ret[s] + self.belief_reward()