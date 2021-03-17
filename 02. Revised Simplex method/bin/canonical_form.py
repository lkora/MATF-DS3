import numpy as np

# Funkcija za svodjenje na kanonski oblik
def make_canonical_form(s):
    j = s.m

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        s.problem = "min"
        s.c *= (-1)

    for i in range(s.m):
        s.Q = np.append(s.Q, i)

    # Transforming inequations to equations, and b >= 0
    for i in range(s.n):
        if s.sign_array[i] != "=":
            zeroes = np.zeros((s.n, 1))
            if s.sign_array[i] == ">=":
                s.B[i] *= -1
                s.A[i] *= 1
                zeroes[i][0] = -1
            elif s.sign_array[i] == "<=":
                zeroes[i][0] = 1

            s.A = np.append(s.A, zeroes, axis=1)

            
            s.sign_array[i] = "="
            s.m += 1          # Changed number of columns
            s.P = np.append(s.P, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    s.c = np.append(s.c, np.zeros((1, len(s.P))))
