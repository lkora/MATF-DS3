import numpy as np
from .print_ import *

# Helper function for checking the parameter condition
def check_condition(coefs):
    for i in range(len(coefs)):
        if coefs[i] < 0:
            return False
    return True

# Helper function for finding indexes
def find_index(coefs, s):
    for i in range(len(coefs)):
        if coefs[i] < 0:
            return s.Q[i]


def revised_simplex(s):
    # Pre solution enumeration
    s.x = np.array(list(map(int, np.append(np.zeros((1, s.br_kolona - len(s.P))), s.matricaB))))
    print("Starting solution:", s.x)

    iteration = 1
    while iteration < 100:
        print("Iteration :", iteration)
        matB = s.matricaA[:, s.P]
        matN = s.matricaA[:, s.Q]
        coefsB_in_fun = s.koefs_problema[s.P]
        coefsN_in_fun = s.koefs_problema[s.Q]
        print("matB:\n", matB)
        print("matN:\n", matN)

        u_res = np.linalg.solve(matB.transpose(), coefsB_in_fun)
        print("System solution for u:\n", u_res)

        CN_prim = coefsN_in_fun - np.dot(u_res, matN)
        print("New coefficient:\n", CN_prim)

        # If all coefficients are positive the solution has been found
        if check_condition(CN_prim):
            print("\nx optimum:", s.x)

            print("Final f:", np.sum(s.koefs_problema * s.x))
            exit()

        j = find_index(CN_prim, s)
        print("j:", j)

        #print(matB, "\n", s.matricaA[:, [j]])
        y_res = np.linalg.solve(matB, s.matricaA[:, [j]])
        print("System solution for y:\n", y_res)

        # Unbounded problem check
        num_neg = 0
        for i in range(len(y_res)):
            if y_res[i] <= 0:
                num_neg += 1

        if num_neg == len(y_res):
            print("STOP: Problem is unbounded!")
            exit()

        else:
            value = np.array([])
            tmp = 0
            for i in s.P:
                if y_res[tmp] > 0.00001:
                    value = np.append(value, s.x[i] / y_res[tmp])
                tmp += 1

            t_cap = value.min()
            print("t cap:", t_cap)

            x_new = np.zeros(len(s.x))
            tmp = 0

            for i in range(len(s.x)):
                if i == j:
                    x_new[i] = t_cap
                elif i in s.P:
                    x_new[i] = s.x[i] - t_cap * y_res[tmp]
                    tmp += 1
                elif i in s.Q:
                    x_new[i] = 0

            print("New x:", x_new)
            s.x = x_new

            l = -1
            for i in s.P:
                if s.x[i] == 0:
                    l = i
            print("l:", l)

            l_index = -1
            j_index = -1
            for i in range(len(s.P)):
                if s.P[i] == l:
                    l_index = i
            for i in range(len(s.Q)):
                if s.Q[i] == j:
                    j_index = i
            if j_index == -1 or l_index == -1:
                raise "Error, one of the indexes j or l has not been found!"

            # Creating new P and Q
            P_old = s.P
            s.P = np.delete(s.P, l_index)
            s.P = np.sort(np.append(s.P, s.Q[j_index]))
            s.Q = np.delete(s.Q, j_index)
            s.Q = np.sort(np.append(s.Q, P_old[l_index]))
            print("New P, Q", s.P, s.Q)

            iteration += 1
