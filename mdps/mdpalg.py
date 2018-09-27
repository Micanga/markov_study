from utils import *
import random

def value_iteration(mdp, epsilon,maxk):
    "Solving an MDP by value iteration. [Fig. 17.4]"
    k = 0
    U1 = dict([(s, 0) for s in mdp.states])

    R, T, gamma = mdp.R, mdp.T, mdp.gamma

    while True:
        U = U1.copy()
        delta = 0

        for s in mdp.states:
            U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)]) for a in mdp.actions(s)])
            delta = max(delta, abs(U1[s] - U[s]))
        
        k = k + 1
        if delta < (epsilon * (1 - gamma) / gamma) or k == maxk:
            return U

def best_policy(mdp, U):
    "Given an MDP and a utility function U, determine the best policy, as a mapping from state to action. (Equation 17.4)"
    pi = {}
    for s in mdp.states:
        pi[s] = argmax(mdp.actions(s), lambda a:expected_utility(a, s, U, mdp))
    return pi

def expected_utility(a, s, U, mdp):
    "The expected utility of doing a in state s, according to the MDP and U."
    return sum([p * U[s1] for (p, s1) in mdp.T(s, a)])


def policy_iteration(mdp):
    "Solve an MDP by policy iteration [Fig. 17.7]"
    U = dict([(s, 0) for s in mdp.states])
    pi = dict([(s, random.choice(mdp.actions(s))) for s in mdp.states])

    while True:

        U = policy_evaluation(pi, U, mdp, 20)
        unchanged = True

        for s in mdp.states:

            a = argmax(mdp.actions(s), lambda a: expected_utility(a,s,U,mdp))
            if a != pi[s]:
                pi[s] = a
                unchanged = False

        if unchanged:
            return pi

def policy_evaluation(pi, U, mdp, k):
    "Return an updated utility mapping U from each state in the MDP to its utility, using an approximation (modified policy iteration)."
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    
    for i in range(k):
        for s in mdp.states:
            U[s] = R(s) + gamma * sum([p * U[s] for (p, s1) in T(s, pi[s])])
    return U

