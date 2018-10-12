import random, POAgent

def pomdp_value_iteration(poagent,epsilon,maxk):
    k = 0
    U1 = dict([(s, 0) for s in poagent.pomdp.states])

    R, T, gamma = poagent.pomdp.R, poagent.T, poagent.pomdp.gamma
    states, actions = poagent.pomdp.states, poagent.actions
    forward, O, V = poagent.forward, poagent.pomdp.O, poagent.V

    while True:
        U = U1.copy()
        delta = 0

        alpha = {}
        for s in states:
            for a in actions:
                for (p, s1) in T(s, a):
                    forward(a,poagent.pomdp.evidences[s1[0]][s1[1]])
                    alpha[s] = R(s) + gamma*(sum([p * O(s1) * V(s1)]))
                    U1[s] = alpha[s]
                    delta = max(delta, abs(U1[s] - U[s]))
        
        k = k + 1
        if delta < (epsilon * (1 - gamma) / gamma) or k == maxk:
            return U