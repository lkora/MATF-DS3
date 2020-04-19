import os.path
from os import path
import numpy as np



# TODO: MAKE MIN TO MAX CONVERSION.


# Prints a bar
def print_split():
    print("--------------------------------------------------\n")

def eliminate(A, b):
    print_split()

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
    
    print("Elimination:\n")
    print("I: ", I)
    print("J: ", J)
    print("K: ", K)

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

    print("New A:\n", new_A)
    print("New b:", new_b)

    # new_m = m-1 --> eliminate if new_m > 1 <=> m > 2
    if m > 2:
        return eliminate(new_A, new_b)
    else:
        return interval_intersection(new_A, new_b)

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

    print_split()
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
        print("VAR is in: " + msg)

    return left_border, right_border

# set x(index) = value and remove column(index) from inequality system
def transform(A, b, index, value):
    n = len(A)
    for p in range(n):
        b[p] -= A[p, index] * value    
    A = np.delete(A, index, axis=1)
    return A, b

    
def replace_var_with_function(A, b, c):
    n = len(A)
    m = len(A[0])
    if n == 0:
        return
    
    for i in range(n):
        for j in range(1, m, 1):
            A[i, j] -= (c[j] / c[0]) * A[i, 0]
        A[i, 0] *= (1 / c[0])
    

def input_option_1():
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\tWhere N - number of equations and M - number of variables\nA11 A12 ... A1M\nA21 A22 ... A2M\n................\nAN1 AN2 ... ANM\nb1 b2 b3 ... bN")
            print_split()
            file_name = input("Enter the file name: ")
            # Creating absolute path to the file in folder examples
            file_dir = os.path.dirname(__file__)
            rel_path = "examples/opt1/" + file_name
            abs_file_path = os.path.join(file_dir, rel_path)
            # Checking if the file exists
            if os.path.exists(abs_file_path) == False:
                # File not found, throw error
                print("The file doesn't exist!")
                raise Exception("The file didn't load because it doesn't exist")
            # File found, opening
            f = open(abs_file_path, 'r')

            # Read the dimensions and A and b
            n, m = [int(x) for x in next(f).split()] # Reads the dimensions
            tmp_array = []
            for line in f: # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close() # File not needed, all is in tmp_array

            in_A = np.zeros((n, m), dtype=float)
            in_b = np.zeros(n, dtype=float)
            # print(tmp_array)
            for i in range(n + 1):
                if i < n:   # Loading A
                    for j in range(m):
                        in_A[i, j] = (float(tmp_array[i][j]))
                else:       # Loading b
                    for j in range(n):
                        in_b[j] = (float(tmp_array[i][j]))
                    break
           
            return n, m, in_A, in_b

def input_option_2():
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\tWhere N - number of equations and M - number of variables\nA11 A12 ... A1M\nA21 A22 ... A2M\n................\nAN1 AN2 ... ANM\nb1 b2 b3 ... bN\nx1 x2 x3 ... xM")
            print_split()
            file_name = input("Enter the file name: ")
            # Creating absolute path to the file in folder examples
            file_dir = os.path.dirname(__file__)
            rel_path = "examples/opt2/" + file_name
            abs_file_path = os.path.join(file_dir, rel_path)
            #Checking if the file exists
            if os.path.exists(abs_file_path) == False:
                # File not found, throw error
                print("The file doesn't exist!")
                raise Exception("The file didn't load because it doesn't exist")
            # File found, opening
            f = open(abs_file_path, 'r')

            # Read the dimensions and A and b
            n, m = [int(x) for x in next(f).split()] # Reads the dimensions
            tmp_array = []
            for line in f: # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close() # File not needed, all is in tmp_array

            # Loading variables
            in_A = np.zeros((n, m), dtype=float)
            in_b = np.zeros(n, dtype=float)
            in_x = np.zeros(m, dtype=float)
            # print(tmp_array)
            for i in range(n + 2):
                if i < n:           # Loading A
                    for j in range(m):
                        in_A[i, j] = (float(tmp_array[i][j]))
                elif i == n:        # Loading b
                    for j in range(n):
                        in_b[j] = (float(tmp_array[i][j]))
                else:               # Loading x    
                    for j in range(m):
                        in_x[j] = (float(tmp_array[i][j]))
            
            return n, m, in_A, in_b, in_x

def input_option_3():
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tObjective function minimisation or maximisation\nc1 c2 c3 ... cM\nA11 A12 ... A1M\nA21 A22 ... A2M\n................\nAN1 AN2 ... ANM\nb1 b2 b3 ... bN")
            print_split()
            file_name = input("Enter the file name: ")
            # Creating absolute path to the file in folder examples
            file_dir = os.path.dirname(__file__)
            rel_path = "examples/opt3/" + file_name
            abs_file_path = os.path.join(file_dir, rel_path)
            # Checking if the file exists
            if os.path.exists(abs_file_path) == False:
                # File not found, throw error
                print("The file doesn't exist!")
                raise Exception("The file didn't load because it doesn't exist")
            # File found, opening
            f = open(abs_file_path, 'r')
            
            # Read the dimensions and A and b and objective function type
            n, m = [int(x) for x in next(f).split()] # Reads the dimensions
            otype = next(f).split()
            otype = str(otype[0])
            if otype != "min" and otype != "max":
                f.close()
                raise Exception("The objective function type is wrong it should be either \"min\" or \"max\"!\n")

            tmp_array = []
            for line in f: # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close() # File not needed, all is in tmp_array

            # Loading variables
            in_A = np.zeros((n, m), dtype=float)
            in_b = np.zeros(n, dtype=float)
            in_c = np.zeros(m, dtype=float)
            otype = ""
            # print(tmp_array)
            for i in range(n + 2):
                if i > 0 and i < n + 1: # Loading A
                    for j in range(m):
                        in_A[i-1, j] = -(float(tmp_array[i][j]))
                elif i == 0:            # Loading c
                    for j in range(m):
                        in_c[j] = (float(tmp_array[i][j]))
                else:                   # Loading b    
                    for j in range(n):
                        in_b[j] = -(float(tmp_array[i][j]))
            
            
            return n, m, otype, in_c, in_A, in_b



def main():
    print("Furie-Mockin method of elimination")
    print_split()
    print("Select one of the possible opions:\n\t(1) Calculate intervals (input: matrix A, vector b)\n\t(2) Check if a vertex is in solution (input: matrix A, vector b, vertex x\n\t(3) Furie-Mockin method of elimination (input: vector c, matrix A, vector b)")
    option = int(input("Option: "))

    if option == 1:
        n, m, A, b = input_option_1()
        
        value = 0.0
        it = 1
        while 1:
            result = []
            if m > 1:
                result = eliminate(A, b)
            else:
                result = interval_intersection(A, b)
                break
            if result[0] > result[1]:    # left > right
                print("The solution doesn't exist!")
                break
            value = float(input("Input value:\nX" + str(it) + " = "))
            A, b = transform(A, b, 0, value)
            m -= 1
            it += 1
        return 0

    elif option == 2:
        n, m, A, b, x = input_option_2()
        
        print_split()
        print("Input:")
        print("A:\n", A)
        print("b: ", b)
        print("x: ", x)
        print_split()

        for i in range(n):
            for j in range(m):
                b[i] -= A[i, j] * x[j]
            if b[i] > 0:
                print("Given point is not a solution!")
                return 0
        print("Given point is a solution!")
        return 0

    elif option == 3:
        n, m, otype, c, A, b = input_option_3()
        for i in range(m):
            tmp = np.zeros(m)
            tmp[i] = 1
            A = np.vstack((A, tmp))
            b = np.append(b, 0)    

        print_split()
        print("Input:")
        print("c: ", c)
        print("A:\n", A)
        print("b: ", b)
        print_split()


        replace_var_with_function(A, b, c)
        
        print("Replace variable with the objective funciton:")
        print("c: ", c)
        print("A:\n", A)
        print("b: ", b)
        print_split()

        
        interval = eliminate(A, b)
        print_split()
        if interval[0] < interval[1]:
            print("Solution: ", interval[0])
        else:
            print("The solution doesn't exist!\n")


if __name__ == '__main__':
   main()