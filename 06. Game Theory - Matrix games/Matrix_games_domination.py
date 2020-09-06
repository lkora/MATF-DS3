import os.path
from os import path
import numpy as np

np.set_printoptions(suppress=True, precision=3)


class FMM_Problem:
    def __init__(self, n, m, otype, c, A, b):
        self.n = n
        self.m = m
        self.otype = otype
        self.c = c
        self.A = A
        self.b = b


# Prints a bar
def print_split():
    print("--------------------------------------------------\n")

def input_vars():    
    option = 0
    while option != 1 or option != 2:
        if option == 1:
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of rows and M - number of columns\nA11 A12 ... A1M\nA21 A22 ... A2M\n.............\nAN1 AN2 ... ANM")
            print_split()

            n = int(input("Input the number of rows: "))
            m = int(input("Input the number of cols: "))
            in_A = np.empty((n, m))
            # Inputing the variables and solutions to the arrays 
            for i in range(n):
                # Input a line to a tmp variable
                tmp = input(str(i) + ": ").split()
                for j in range(m):
                    in_A[i, j] = float(tmp[j])
            
            print_split()

            break

        elif option == 2:
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of rows and M - number of columns\nA11 A12 ... A1M\nA21 A22 ... A2M\n.............\nAN1 AN2 ... ANM")
            print_split()
            print_split()
            print_split()
            file_name = input("Enter the file name: ")
            # Creating absolute path to the file in folder examples
            file_dir = os.path.dirname(__file__)
            rel_path = "examples/" + file_name

            abs_file_path = os.path.join(file_dir, rel_path)
            # Checking if the file exists
            if os.path.exists(abs_file_path) == False:
                # File not found, throw error
                print("The file doesn't exist!")
                raise Exception("The file didn't load because it doesn't exist")
            # File found, opening
            f = open(abs_file_path, 'r')

            n, m = [int(x) for x in next(f).split()]    # Reads the dimensions
            tmp_array = []
            for line in f:  # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close()       # File not needed, all is in tmp_array
            
            # Formatting the input
            in_A = []
            # print(tmp_array)
            for i in range(n):
                for j in range(m):
                    in_A.append(float(tmp_array[i][j]))
            in_A = np.resize(in_A, (n, m))

            break
                    
        else:
            option = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()

    return in_A, n, m

def print_lp_problem(game):
    n = len(game)
    m = len(game[0])
    
    print_split()
    print("I problem:\n(min) -v = (max) v")
    for i in range(n):
        for j in range(m):
            print(str(game[i, j]) + "*x" + str(j+1), end="")
            if j < m-1:
                print(" + ", end="")
        print(" >= v")
    for i in range(n):
        print("x" + str(i+1), end="")    
        if i != n-1:
            print(" + ", end="")
    print(" = 1")
    for i in range(n):
        print("x" + str(i+1), end="")    
        if i != n-1:
            print(", ", end="")
    print(" >= 0\n")

    print("II problem:\n(min) v")
    for i in range(m):
        for j in range(n):
            print(str(game[j, i]) + "*y" + str(j+1), end="")
            if j < m-1:
                print(" + ", end="")
        print(" <= v")
    for i in range(m):
        print("y" + str(i+1), end="")    
        if i != m-1:
            print(" + ", end="")
    print(" = 1")
    for i in range(m):
        print("y" + str(i+1), end="")    
        if i != m-1:
            print(", ", end="")
    print(" >= 0")

    # print_split()


def form_problem_for_fmm(game):
    n = len(game)
    m = len(game[0])

    # Dimensions
    n1 = n + 2
    m1 = m + 1
    n2 = m + 2
    m2 = n + 1

    # Loading c
    tmp_c1 = np.zeros(m1)
    tmp_c1[0] = -1
    tmp_c2 = np.zeros(m2)
    tmp_c2[0] = 1

    # Loading A
    # tmp_A1 = np.zeros((n+2, m+1))
    tmp_A1 = []
    for i in range(n):
        tmp_A1.append(1)
        for j in range(m):
            tmp_A1.append(game[i, j] * -1)
    tmp_A1.append(0)
    for i in range(m):
        tmp_A1.append(1)
    tmp_A1.append(0)
    for i in range(m):
        tmp_A1.append(-1)

    tmp_A2 = []
    for i in range(m):
        tmp_A2.append(-1)
        for j in range(n):
            tmp_A2.append(game[j, i])
    tmp_A2.append(0)
    for i in range(n):
        tmp_A2.append(1)
    tmp_A2.append(0)
    for i in range(n):
        tmp_A2.append(-1)

    tmp_A1 = np.reshape(np.array(tmp_A1, dtype=int), (n1, m1))
    tmp_A2 = np.reshape(np.array(tmp_A2, dtype=int), (n2, m2))

    # Loading b
    tmp_b1 = np.zeros(n1)
    tmp_b1[-2] = 1
    tmp_b1[-1] = -1

    tmp_b2 = np.zeros(n2)
    tmp_b2[-2] = 1
    tmp_b2[-1] = -1
    

    # Putting it to an object and preparing to return
    p1 = FMM_Problem(n1, m1, "min", tmp_c1, tmp_A1, tmp_b1)
    p2 = FMM_Problem(n2, m2, "min", tmp_c2, tmp_A2, tmp_b2)

    return p1, p2


def domination(game_matrix):
    n = len(game_matrix)
    m = len(game_matrix[0])

    row_removed = np.full(n, False, dtype=bool)
    col_removed = np.full(m, False, dtype=bool)
    
    has_changes = True
    
    while has_changes:
        has_changes = False
        # Finding dominated row
        for i in range(n):
            if row_removed[i] == True:
                continue
            
            for j in range(i+1, n, 1):
                if row_removed[j] == True:
                    continue
                i_is_dominated = True
                j_is_dominated = True
                for k in range(m):
                    if col_removed[k] == True:
                        continue
                    
                    if game_matrix[i, k] > game_matrix[j, k]:
                        i_is_dominated = False
                    if game_matrix[i, k] < game_matrix[j, k]:
                        j_is_dominated = False
                    
                    if i_is_dominated == False and j_is_dominated == False:
                        continue
                
                if j_is_dominated == True:
                    row_removed[j] = True
                    has_changes = True
                elif i_is_dominated == True:
                    row_removed[i] = True
                    has_changes = True
            
            if has_changes == True:
                continue
        if has_changes == True:
            continue

        # Finding dominated column
        for i in range(m):
            if col_removed[i] == True:
                continue
            
            for j in range(i+1, m, 1):
                if col_removed[j] == True:
                    continue
                i_is_dominated = True
                j_is_dominated = True
                for k in range(n):
                    if row_removed[k] == True:
                        continue
                    
                    if game_matrix[k, i] < game_matrix[k, j]:
                        i_is_dominated = False
                    if game_matrix[k, i] > game_matrix[k, j]:
                        j_is_dominated = False
                    
                    if i_is_dominated == False and j_is_dominated  == False:
                        continue
                
                if j_is_dominated == True:
                    col_removed[j] = True
                    has_changes = True
                elif i_is_dominated == True:
                    col_removed[i] = True
                    has_changes = True
            
            if has_changes == True:
                continue
        if has_changes == True:
            continue
    
    new_n = np.count_nonzero(row_removed == False)
    new_m = np.count_nonzero(col_removed == False)
    updated_game = np.zeros((new_n, new_m))
    
    k = 0
    for i in range(n):
        if row_removed[i]:
            continue
        l = 0
        for j in range(m):
            if col_removed[j] == False:
                updated_game[k, l] = game_matrix[i, j]
                l += 1
        k += 1

    return updated_game

def interval_intersection(A, b):
    n = len(b)
    left_border = -np.Inf
    right_border = np.Inf

    # interval_intersection is used when all variables except one are eliminated
    # current system:
    # c1*x1 > b1
    # c2*x1 > b2
    # ...
    # cK*x1 > bK
    # intersection of all inequalities returns interval

    for p in range(n):
        if A[p, 0] == 0:
            # Impossible inequality
            if b[p] > 0:
                return right_border, left_border
        
        # Division by zero
        if A[p, 0] == 0:
            # Negative Inf
            if (np.sign(b[p]) * np.sign(A[p, 0])) <= -0:
                value = -np.Inf
            # Positive Inf
            elif (np.sign(b[p]) * np.sign(A[p, 0])) >= 0:
                value = np.Inf
        # Divisor != 0
        else:
            value = b[p]/A[p, 0]
                
        
        # Observe c*x1 > b:
        # 1) if c < 0:
        #      then x1 < b/c <=> x1 is in (-INF, b/c]
        # 2) else
        #      then x1 > b/c <=> x1 is in [b/c, +INF]

        if A[p, 0] < 0:
            right_border = min(right_border, value)
        else:
            left_border = max(left_border, value)

    # print_split()
    # right < left <=> empty set
    msg = ""
    if right_border < left_border:
        print("The solution doesn't exist")
    else:
        if left_border == -np.Inf:
            msg += "(-Inf, "
        else:
            msg += "[" + str(left_border) + ", "

        if right_border == np.Inf:
            msg += "Inf)"
        else:
            msg += str(right_border) + "]"

        msg += "\n"
        # print("VAR is in: " + msg)

    return left_border, right_border


def eliminate(A, b):
    # print_split()

    n = len(A)
    m = len(A[0])

    eliminate_index = m - 1
    
    I = []
    J = []
    K = []
    for i in range(n):
        if A[i, eliminate_index] > 0:
            I.append(i)
        elif A[i, eliminate_index] < 0:
            J.append(i)
        else:
            K.append(i)
    
    # print("Elimination:\n")
    # print("I: ", I)
    # print("J: ", J)
    # print("K: ", K)

    # Inequalities from sets I and J are combined to eliminate one variable
    I_length = len(I)
    J_length = len(J)

    # Elimination of element x(m-1) produces new system
    new_A = []
    new_A = []
    new_b = []
    
    for i in range(I_length):
        for j in range(J_length):
            for p in range(m):
                if p == eliminate_index:
                    continue
                new_A.append(((A[I[i], p] / A[I[i], eliminate_index]) - (A[J[j], p] / A[J[j], eliminate_index])))
            new_b.append((b[I[i]] / A[I[i], eliminate_index]) - (b[J[j]] / A[J[j], eliminate_index]))

    # Inequalities from set K are just copied to new system (m is in K if A(m, n-1) = 0)
    K_length = len(K)
    for k in range(K_length):
        for p in range(m):
            if p == eliminate_index:
                continue
            new_A.append(A[K[k], p])
        new_b.append(b[K[k]])

    new_A = np.array(new_A)
    height = I_length * J_length + K_length
    new_A = np.reshape(new_A, (height, m-1))

    # print("New A:\n", new_A)
    # print("New b:", new_b)

    # new_m = m-1 --> eliminate if new_m > 1 <=> m > 2
    if m > 2:
        return eliminate(new_A, new_b)
    else:
        return interval_intersection(new_A, new_b)


def replace_var_with_function(A, b, c):
    n = len(A)
    m = len(A[0])
    if n == 0:
        return
    
    for i in range(n):
        for j in range(1, m, 1):
            A[i, j] -= (c[j] / c[0]) * A[i, 0]
        A[i, 0] *= (1 / c[0])
    

def Fourier_Motzkin_elimination(n, m, otype, c, A, b):
    b = -b
    A = -A
    for i in range(m):
        tmp = np.zeros(m, dtype=np.float64)
        tmp[i] = 1
        A = np.vstack((A, tmp))
        b = np.append(b, 0)    
    
    # print_split()
    # print("Input:")
    # print("c: ", c)
    # print("A:\n", A)
    # print("b: ", b)
    # print_split()
    
    replace_var_with_function(A, b, c)
    
    # print("Replace variable with the objective funciton:")
    # print("c: ", c)
    # print("A:\n", A)
    # print("b: ", b)
    # print_split()


    interval = eliminate(A, b)
    # print_split()
    if interval[0] < interval[1]:
        print("Solution: ", round(interval[0], 3))
    else:
        print("The solution doesn't exist!\n")

def main():
    game, n, m = input_vars()
    print("Initial game matrix problem:\n", game)
    game = domination(game)
    print("Game matrix after removing the dominated rows and columns:\n", game)
    print_lp_problem(game)
    if len(game) == 1 and len(game[0]) == 1:
        print_split()
        print("Solution: ", round(game[0, 0], 3))
        return 0
    print_split()
    p1, p2 = form_problem_for_fmm(game)
    p1.otype = "min"
    p2.otype = "min"
    # print("Solution for the first problem (min -v) using Fourier-Motzkin elimination method:")
    # Fourier_Motzkin_elimination(p1.n, p1.m, p1.otype, p1.c, p1.A, p1.b)
    # print("\n")
    # print("Solution for the second problem (min v) using Fourier-Motzkin elimination method:")
    Fourier_Motzkin_elimination(p2.n, p2.m, p2.otype, p2.c, p2.A, p2.b)


    return 0


if __name__ == '__main__':
   main()