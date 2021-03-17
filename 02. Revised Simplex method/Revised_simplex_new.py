import numpy as np
from random import seed
from random import randrange
from bin.input import *
from bin.print import *

precision = 0.0001

def swap_cols_2d(arr, frm, to):
    arr[:,[frm, to]] = arr[:,[to, frm]]

def swap(arr, frm, to):
    tmp = arr[to]
    arr[to] = arr[frm]
    arr[frm] = tmp 

def append_horizontally(A, B):
    if len(A) != len(B):
        raise Exception('The matrices must have the same height!\n')
    else:
        np.stack((A, B), axis = 1)
    return A

def get_first_negative(vec):
    vec_length = len(vec)
    for i in range(vec_length):
        if vec[i] < 0:
            return i
    return -1

def is_not_canonical(A, b, c):
    A_height = len(A)
    # Checking if b[i] > 0
    for i in range(len(b)):
        if b[i] < float(0):
            return True

    # Checking if b has canonical base
    # 1 0 0 ... 0 ...
    # 0 1 0 ... 0 ...
    # 0 0 1 ... 0 ...
    # ...............
    # 0 0 0 ... 1 

    # np.abs(A[i, j] - 1) > precision instead of A[i, j] != 1 because of precision
    # A[i, j] might be 0.99999999
    for i in range(A_height):
        if np.abs(c[i]) > precision:
            return True
        for j in range(A_height):
            if (i == j) and (np.abs((A[i, j] - 1)) > precision):
                return True
            elif (i != j) and (np.abs(A[i, j]) > precision):
                return True
    return False


def set_canonical_matrix(A, b, c):
    # Setting the seed for the random number generator
    seed(1337)
    # n - number of rows of A
    # m - number of columns of A
    n = len(A)
    m = len(A[0])
    Fo = float(0)
    
    # j - row
    # i - column
    while is_not_canonical(A, b, c):
        for i in range(n):
            if (A[i, i] * b[i] < 0):
                # If b[i] is negative then we have to pick different columns for the base
                # Finding all potential base columns:
                potential_base_columns = []
                for j in range(i+1, m, 1):
                    if A[i, j] * b[i] > 0:
                        potential_base_columns.append(j)

                # Picking random column and replacing it with current one in base:
                new_column_index = randrange(12873321) % len(potential_base_columns)
                new_column = potential_base_columns[new_column_index]
                # Swaping columns my_array[:,[0, 2]] = my_array[:,[2, 0]]
                swap_cols_2d(A, i, new_column)
                swap(c, i, new_column)

            # "clearing" i-th column
            # "clearing" - Transformation with result of i-th column having
            # 0s above and below i-th row and 1 for i-th row
            for j in range(n):
                if i == j:
                    continue
                coef = A[j, i] / A[i, i]
                for k in range(m):
                    A[j, k] -= coef * A[i, k]
                b[j] -= coef * b[i]
            coef = A[i, i]
            for k in range(m):
                A[i, k] /= coef
            b[i] /= coef

            coef = c[i] / A[i, i]
            for k in range(m):
                c[k] -= coef * A[i, k]

            Fo -= coef * b[i]
    
    # Creating P and Q
    P = []
    Q = []
    for i in range(m):
        if i < n:
            P.append(i)
        else:
            Q.append(i)
    
    return P, Q, Fo


def get_t_opt(x, y, P):
    y_length = len(y)
    t = np.Inf
    t_index = -1
    for i in range(y_length):
        val = x[P[i]] / y[i]
        if y[i] > 0 and val < t:
            t = val
            t_index = P[i]
        i += 1
    return (t, t_index)


# Starting with x: if i in P then we set next unused value of b for x(i) else x(i) = 0
def get_x(b, P, size):
    j = 0
    x = np.zeros(size)
    for p in P:
        x[p] = b[j]
        j += 1

    return x


def get_B(A, P):
    # B.shape = (len(A), 1) # Making it a column vector
    # B00  = Acol(p0)  B01  = Acol(p1)  .....  B0len(P)  = Acol(len(P)-1) 
    # B10  = Acol(p0)  B11  = Acol(p1)  .....  B1len(P)  = Acol(len(P)-1) 
    # ...  = Acol(p0)  ...  = Acol(p1)  .....  ...       = Acol(len(P)-1)
    # BAh0 = Acol(p0)  BAh1 = Acol(p1)  .....  BAhlen(P) = Acol(len(P)-1) 
    # B = Ah x len(P)
    A_height = len(A)
    P_length = len(P)
    B = np.zeros((A_height, P_length), dtype=float)
    for j in range(P_length):
        for i in range(A_height):
            B[i, j] = A[i, P[j]]

    return B

def get_Cb(c, P):
    P_length = len(P)
    Cb = np.zeros(P_length)
    for i in range(P_length):
        Cb[i] = c[P[i]]
    return Cb

def get_Kq(A, Q):
    # Kq.shape = (len(A), 1) # Making it a column vector
    # Kq00  = Acol(q0)  Kq01  = Acol(q1)  .....  Kq0len(Q)  = Acol(len(Q)-1) 
    # Kq10  = Acol(q0)  Kq11  = Acol(q1)  .....  Kq1len(Q)  = Acol(len(Q)-1) 
    # ...   = Acol(q0)  ...   = Acol(q1)  .....  ...        = Acol(len(Q)-1)
    # KqAh0 = Acol(q0)  KqAh1 = Acol(q1)  .....  KqAhlen(Q) = Acol(len(Q)-1) 
    # Kq = Ah x len(Q)
    A_height = len(A)
    Q_length = len(Q)
    Kq = np.zeros((A_height, Q_length), dtype=float)

    for j in range(Q_length):
        for i in range(A_height):
            Kq[i, j] = A[i, Q[j]]
    
    return Kq

def get_Cq(c, Q):
    Cq = np.zeros(len(Q))
    Q_length = len(Q)
    for i in range(Q_length):
        Cq[i] = c[Q[i]]
    return Cq


def update_x(x, y, l, P, t_opt):
    y_length = len(y)
    for i in range(y_length):
        index = P[i]
        x[index] -= y[i] * t_opt
        i += 1
    x[l] = t_opt

def update_P_Q(P, Q, t_index, l):
    i = 0
    for p in P:
        if p == t_index:
            P[i] = l
            break
        i += 1
    i = 0
    for q in Q:
        if q == l:
            Q[i] = t_index
            break
        i += 1

# Calculates the Revised simplex
# Step 1: Calcualte Cb
# Step 2: Calculate r
# Step 3: Calculate Kl
# Step 4: Check if y is bounded
# Step 5: Update x
def revised_simplex(A, b, c, P, Q, Fo):
    # Preprocess: Calculating x:
    x = get_x(b, P, len(c))
    
    print("Starting x value: ", x)
    it = 0
    while 1:
        print_split()
        print("Iteration " + str(it) + ":\n")
        print_split()
        it += 1

        # Cb - has values from c where c(i) is in Cb if i is in P
        # P = [1, 3, 4], C = [c1, c2, ... cN] => Cb = [c1, c3, c4]

        # Step 1: Solve u*B = Cb <=> u = Cb*B' (B' is inverse matrix of B)
        # This is equivalent to u*K(i) = c(i) for i in P which is what we need to find optimal value
        B = get_B(A, P)
        Cb = get_Cb(c, P)
        B_inv = np.linalg.inv(B)
        u = np.matmul(Cb, B_inv)
        print("Step 1: Solving system(1): uB = Cb")
        print("B:\n", B)
        print("Cb:\n", Cb)
        print("Result of u(1):", u)
        print_split()
       
        # Step 2: Calculating r
        # r(j) = c(j) - u*K(j)
        # if (r >= 0) then we found our optimal value
        # This is equivalent to (l_index == STOP) which we get from get_first_negative(r)   
        Kq = get_Kq(A, Q)
        Cq = get_Cq(c, Q)
        r = Cq - np.matmul(u, Kq)
        # K := Kq in output
        # C := Cq in output
        print("Step 2: Calculating r (r := C - uK):")
        print("C:\n", Cq)
        print("K:\n", Kq)
        print("Result(r): ", r)
        
        # If r > 0 then optimal value is found
        l_index = get_first_negative(r)
        if l_index == -1:
            print("(r > 0) is true => optimal value is found!")
            break
        l = Q[l_index]
        print("Bland's rule: first negative r(i) is r" + str(l_index))
        print_split()

        # Step 3: Solve B*y = Kl <=> y = B'Kl <=> y = B/Kl where r(l) < 0
        Kl = A[:,l] # Kl = A.col(l)
        Kl = Kl.reshape(len(A), 1) # Making it vertical
        if len(B) != len(Kl):
            raise Exception('Matrix Kl must be same height as matrix B!')
        elif len(Kl[0]) != 1:
            raise Exception('Matrix Kl must have shape nx1!')
        else:
            y = np.transpose(np.matmul(np.linalg.inv(B), Kl))
            y = y.flatten()

        print("Step 3: Solving system(2): By = K" + str(l_index))
        print("B:\n", B)
        print("K:",l,"\n", Kl)
        print("Result of y(2):", y)
        print_split()

        # Step 4: If y has all negative values, then there is no optimum value (it's not bounded)
        # Otherwise we get t_opt := min{x(i)/y(i) | y(i) > 0}
        print("Step 4: check if y <= 0:\n")
        if np.all(y <= 0):
            print("Function does not reach optimal value because (y <= 0) is true!\n")
            return (0, np.zeros(1))
        print("(y <= 0) is not true!\n")
        print("Finding optimal t:\n")
        t_opt, t_index = get_t_opt(x, y, P)
        print("Optimal t: " + str(t_opt) + "\n")
        print("Column " + str(t_index) + " leaves base (P)\n")
        print_split()

        # Step 5: With t_opt we can update our x:
        # x(i) = x_old(i) - t_opt*y(i), for i in P
        # x(i) = t_opt, for i == l
        # x(i) = 0, otherwise
        # We replace t_index in P with l and l in Q with t_index (new base P)
        print("Step 5: updating x:\n")
        print("Old x:", x)
        update_x(x, y, l, P, t_opt)
        update_P_Q(P, Q, t_index, l)
        print("New x:", x)

    print_split()
    # c*(x.transpose()) is matrix with dimension 1x1
    F = -Fo + np.ndarray.item((np.matmul(c, x.reshape(len(x), 1))))
    return (F, x)


def main():
    print("Revised simplex method")
    print_split()
    # Setting precision and notation
    np.set_printoptions(precision = 3)

    A, c, b = input_vars()
    print("Solving system(canonical form): Ax = b")
    print_current(A, b, c)
    print_split()
    
    # Revised Simplex:
    # P - column indexes of base matrix B
    # Q - other column indexes
    # Fo - base value of F where F = Fo + c*x
    # x - solution
    P, Q, Fo = set_canonical_matrix(A, b, c)

    print("Set unit matrix:")
    print_current(A, b, c)
    print("Base indexes (P):\n", P)
    print("Nonbase indexes (Q):\n", Q)
    print("Base function value (Fo):\n", Fo)
    print_split()
    
    print("Revised Simplex:\n")
    F, x = revised_simplex(A, b, c, P, Q, Fo)
    
    # if x.height() == 0 and x.width() == 0 then there is no solution (special case value)
    if len(x) == 0 and len(x[0]) == 0:
        return 0

    print("Solution:", np.round(x, 3))
    print("Optimal value: " + str(np.round(F, 3)) + "\n")

    return 0


if __name__ == '__main__':
   main()