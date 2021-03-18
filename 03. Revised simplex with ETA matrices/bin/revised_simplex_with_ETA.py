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


def revised_simplex_with_ETA(s):
    # Pre solution enumeration
    s.x = np.array(list(map(int, np.append(np.zeros((1, s.m - len(s.P))), s.B))))
    print("Starting solution:", s.x)

    matB = s.A[:, s.P]
    
    iteration = 1
    while iteration < 100:
        print("Iteration :", iteration)
        matN = s.A[:, s.Q]
        coefsB_in_fun = s.c[s.P]
        coefsN_in_fun = s.c[s.Q]
        print("matB:\n", matB)
        print("matN:\n", matN)

        u_res = np.linalg.solve(matB.transpose(), coefsB_in_fun)
        print("System solution for u:\n", u_res)

        CN_prim = coefsN_in_fun - np.dot(u_res, matN)
        print("New coefficient:\n", CN_prim)

        # If all coefficients are positive the solution has been found
        if check_condition(CN_prim):
            print("\nx optimum:", s.x)
            print("Final f:", np.sum(s.c * s.x))
            exit()

        j = find_index(CN_prim, s)
        print("j: ", j)

        #print(matB, "\n", s.A[:, [j]])
        y_res = np.linalg.solve(matB, s.A[:, [j]])
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
                if y_res[tmp] > 0:
                    value = np.append(value, s.x[i] / y_res[tmp])
                tmp += 1

            t_cap = value.min()
            print("t cap:", t_cap)

            x_new = np.zeros(len(s.x))

            for i in range(len(s.x)):
                if i == j:
                    x_new[i] = t_cap
                elif i in s.P:
                    p = -1 
                    for d in range(len(s.P)):
                        if i == s.P[d]:
                            p = d
                    x_new[i] = s.x[i] - t_cap * y_res[p]
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
            P_old = np.copy(s.P)
            s.P[l_index] = s.Q[j_index]
            s.Q[j_index] = P_old[l_index]
            print("New P, Q", s.P, s.Q)

            # Creating ETA matrix
            E = np.identity(len(s.P))
            m_new = y_res
            leftEnd = E[:, :l_index]
            rightEnd = E[:, l_index+1:]
            leftEnd = np.append(leftEnd, m_new, axis=1)
            leftEnd = np.append(leftEnd, rightEnd, axis=1)
            E = leftEnd
            print("Matrix E:\n", E)

            # Creating new B matrix like B*E
            matB = np.dot(matB, E)


            iteration += 1
