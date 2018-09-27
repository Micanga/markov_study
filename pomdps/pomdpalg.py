import random, pomdp

def pomdp_value_iteration(pomdp,epsilon,maxk):
    k = 0
    U1 = dict([(s, 0) for s in pomdp.states])

    R, T, gamma = pomdp.R, pomdp.T, pomdp.gamma

    while True:
        U = U1.copy()
        delta = 0

        alpha = {}
        for s in pomdp.states:
            for a in pomdp.actions:
                for (p, s1) in T(s, a):
                    pomdp.forward(a,pomdp.O(s1))
                    alpha[s] = R(s) + gamma*(sum([p * pomdp.O(s1) * pomdp.V(s1)]))
                    U1[s] = alpha[s]
                    delta = max(delta, abs(U1[s] - U[s]))
        
        k = k + 1
        if delta < (epsilon * (1 - pomdp.gamma) / pomdp.gamma) or k == maxk:
            return U