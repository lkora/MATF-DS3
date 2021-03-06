import numpy as np

# Function for cannonical matrix reduction
def canonical_form(s):
    j = s.m

    # Transofrimng the problem into finding a minimum
    if s.problem == "max":
        s.problem = "min"
        s.c *= (-1)

    s.Q = np.array(range(0, s.m))

    has_equation = False
    # Transforming inequations to equations, and b >= 0
    for i in range(s.n):
        if s.sign_array[i] != "=":
            zeroes = np.zeros((s.n, 1))
            if s.sign_array[i] == ">=":
                s.B[i] *= -1
                s.A[i] *= -1
                zeroes[i][0] = 1
            elif s.sign_array[i] == "<=":
                zeroes[i][0] = 1

            s.A = np.append(s.A, zeroes, axis=1)

            
            s.sign_array[i] = "="
            s.m += 1          # Changed number of columns
            s.P = np.append(s.P, j)
            j += 1
        else:
            has_equation = True

    # If all are =
    if has_equation:
        b_index = 0
        for b_index in range(s.m-1, 0, -1):
            if s.A[0][b_index] != 0:
                break
        s.P = np.array(range(b_index, s.m))
        s.Q = np.array(range(0, b_index))


    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    if not has_equation:
        s.c = np.append(s.c, np.zeros((1, len(s.P))))
