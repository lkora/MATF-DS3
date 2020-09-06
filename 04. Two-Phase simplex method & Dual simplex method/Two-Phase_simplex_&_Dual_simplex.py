import os.path
from os import path
import sys
import numpy as np
from random import seed
from random import randrange

# FIX: OPTIMAL SOLUTION SHOWING

precision = 0.0001

# Prints a bar
def print_split():
    print("--------------------------------------------------\n")


# Prints current vectors A, b, c
def print_current(A, b, c):
    print("c:\n", c)
    #print(c)
    print("A:\n", A)
    #print(A)
    print("b:\n", b)
    #print(b)

def print_system(A, b, c, F):
    print("c:\n", c)
    #print(c)
    print("A:\n", A)
    #print(A)
    print("b:\n", b)
    #print(b)
    print("F:\n", F)    


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

def is_non_negative(b):
    b_length = len(b)
    for i in range(b_length):
        if b[i] < 0:
            return i
    return -1

def is_non_negative_matrix_row(A, row):
    A_width = len(A[0])
    for i in range(A_width):
        if A[row, i] < 0:
            return i
    return -1

def find_pivot(c, A, row):
    pivot_index = 0
    max_value = -np.Inf
    A_width = len(A[0])
    for i in range(A_width):
        if A[row, i] < 0:
            value = c[i] / A[row, i]
            if value > max_value:
                max_value = value
                pivot_index = i
    return pivot_index

def update_system(c, A, b, F, p_row, p_col):
    n = len(A)
    m = len(A[0])
    # Row of pivot / pivot
    coef = A[p_row, p_col]
    for i in range(m):
        A[p_row, i] /= coef
    b[p_row] /= coef

    # Clearing p_col columns
    for i in range(n):
        if i == p_row:
            continue
        coef = -A[i, p_col]
        for j in range(m):
            A[i, j] += coef * A[p_row, j]
        b[i] += coef * b[p_row]
    coef = -c[p_col]
    for j in range(m):
        c[j] += coef * A[p_row, j]
    F += coef * b[p_row]

    return c, A, b, F

def input_vars(option):
    input_type = 0
    # 
    # --- Two phase simplex ---
    # 
    if option == 1:
        while input_type != 1 and input_type != 2:
            input_type = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()
        
        # --- Manual input --- 
        if input_type == 1:
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tGoal function minimisation or maximisation\nc1 c2 c3 ... cM\nA11 A12 ... A1M _ b1\nA21 A22 ... A2M _ b2\n................\nAN1 AN2 ... ANM _ bN\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<', '>' or '='\n")
            print_split()

            n = int(input("Input the number of equations: "))
            m = int(input("Input the number of variables: "))

            # Reserving and initializing space for the Objective function
            in_c = np.zeros(m, dtype=np.float64)
            # Reserving and initializing space for the coeficients
            in_A = np.zeros((n, m), dtype=np.float64)
            # Reserving and initializing space for the solution values
            in_b = np.zeros(n, dtype=np.float64)

            otype = input("Input \"min\" or \"max\" for the Objective function: ")
            if otype != "min" and otype != "max":
                print("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")
                return -1

            # Input the Objective function
            tmp = input("Objective function: ").split()
            i = 0
            for c in tmp:
                in_c[i] = float(c)
                i += 1
            # Converting the Objective function to minimise since the program is made with minimisation
            if otype == "max":
                print("Converting max to min.")
                in_c *= -1

            sign = np.empty(n, dtype=str)

            unit_columns = []
            # Inputing the variables and solutions to the arrays 
            for i in range(n):
                # Input a line to a tmp variable
                tmp = input(str(i) + ": ").split()
                for j in range(m):
                    in_A[i, j] = float(tmp[j])
                sign[i] = tmp[m]
                in_b[i] = float(tmp[m + 1])

                # No transformation required, since this program works with "<"
                # And "=" can be represented both as ">=" and "<="
                if sign[i] == "=":
                    continue
                
                # If the entered sign is ">" than we transform it to "<"
                if sign[i] == ">":
                    for j in range(m):
                        in_A[i, j] *= -1
                    in_b[i] *= -1

                unit_columns.append(i)


            # Add new variables to convert inequation to equation:
            #     x1 + x2 + x3 + ... + xn <= c
            # =>  x1 + x2 + x3 + ... + xn + x = c
            # Thus appending an identity matrix        
            unit_columns.sort()

            A_tmp = np.empty((n, 0))
            for i in unit_columns:
                A_unit = np.zeros((n, 1))
                for j in range(n):
                    if i == j:
                        A_unit[j] = 1
                A_tmp = np.hstack((A_tmp, A_unit))
                in_c = np.hstack((0, in_c))
            in_A = np.hstack((A_tmp, in_A))
        

            # Set b to be positive:
            for i in range(n):
                if(in_b[i] < 0):
                    if i in unit_columns:
                        unit_columns.remove(i)
                    in_A[i] *= -1
                    in_b[i] *= -1

        
        elif input_type == 2:
            # Read from file
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tGoal function minimisation or maximisation\nc1 c2 c3 ... cM\nA11 A12 ... A1M _ b1\nA21 A22 ... A2M _ b2\n................\nAN1 AN2 ... ANM _ bN\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<', '>' or '='\n")
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
            
            in_c = []
            # Read 2 first lines
            for i in range(3):
                if i == 0:
                    n, m = [int(x) for x in next(f).split()]    # Reads the dimensions
                if i == 1:
                    otype = next(f).split()
                    otype = otype[0]
                    if otype != "min" and otype != "max":
                        f.close()
                        raise Exception("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")
                if i == 2:
                    in_c = np.append(in_c, [float(x) for x in next(f).split()])     # Reads the Objective functiom
            
            # Converting the Objective function to minimise since the program is made with minimisation
            if otype == "max":
                print("Converting max to min.")
                in_c *= -1

            tmp_array = []
            for line in f:  # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close()       # File not needed, all is in tmp_array
            
            # Formatting the input
            in_A = []
            sign = []
            in_b = []
            unit_columns = []
            # print(tmp_array)
            for i in range(n):
                for j in range(m + 2):
                    if j < m:
                        in_A.append(float(tmp_array[i][j]))
                    elif j == m:
                        sign.append(tmp_array[i][j])
                    elif j == (m + 1):
                        in_b.append(float(tmp_array[i][j]))
                
                # No transformation required, since this program works with "<"
                # And "=" can be represented both as ">=" and "<="
                if sign[i] == "=":
                    continue

                # If the entered sign is ">" than we transform it to "<"
                if sign[i] == ">":
                    in_A_length = len(in_A)
                    for j in range(i*m, in_A_length, 1):
                        in_A[j] *= -1
                    in_b[i] *= -1

                unit_columns.append(i)

            # Converting the final list to numpy array
            in_A = np.array(in_A)
            in_A = in_A.reshape(n, m)

            # Add new variables to convert inequation to equation:
            #     x1 + x2 + x3 + ... + xn <= c
            # =>  x1 + x2 + x3 + ... + xn + x = c
            # Thus appending an identity matrix        
            unit_columns.sort()
            
            A_tmp = np.empty((n, 0))
            for i in unit_columns:
                A_unit = np.zeros((n, 1))
                for j in range(n):
                    if i == j:
                        A_unit[j] = 1
                A_tmp = np.hstack((A_tmp, A_unit))
                in_c = np.hstack((0, in_c))
            in_A = np.hstack((A_tmp, in_A))

            # Set b to be positive:
            for i in range(n):
                if(in_b[i] < 0):
                    if i in unit_columns:
                        unit_columns.remove(i)
                    in_A[i] *= -1
                    in_b[i] *= -1

        return in_A, in_c, in_b, unit_columns
    
    # 
    # --- Dual simplex ---
    # 
    elif option == 2:
        while input_type != 1 and input_type != 2:
            input_type = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()
        
        # --- Manual input --- 
        if input_type == 1:
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tGoal function minimisation or maximisation\nc1 c2 c3 ... cM\nA11 A12 ... A1M _ b1\nA21 A22 ... A2M _ b2\n................\nAN1 AN2 ... ANM _ bN\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<', '>' or '='\n")
            print_split()

            n = int(input("Input the number of equations: "))
            m = int(input("Input the number of variables: "))

            # Reserving and initializing space for the Objective function
            in_c = np.zeros(m, dtype=np.float64)
            # Reserving and initializing space for the coeficients
            in_A = np.zeros((n, m), dtype=np.float64)
            # Reserving and initializing space for the solution values
            in_b = np.zeros(n, dtype=np.float64)

            otype = input("Input \"min\" or \"max\" for the Objective function: ")
            if otype != "min" and otype != "max":
                print("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")
                return -1

            # Input the Objective function
            tmp = input("Objective function: ").split()
            i = 0
            for c in tmp:
                in_c[i] = float(c)
                i += 1
            # Converting the Objective function to minimise since the program is made with minimisation
            if otype == "max":
                print("Converting max to min.")
                in_c *= -1

            sign = np.empty(n, dtype=str)

            # Inputing the variables and solutions to the arrays 
            for i in range(n):
                # Input a line to a tmp variable
                tmp = input(str(i) + ": ").split()
                for j in range(m):
                    in_A[i, j] = float(tmp[j])
                sign[i] = tmp[m]
                in_b[i] = float(tmp[m + 1])

                # No transformation required, since this program works with "<"
                # And "=" can be represented both as ">=" and "<="
                if sign[i] == "=":
                    continue
                
                # If the entered sign is ">" than we transform it to "<"
                if sign[i] == ">":
                    for j in range(m):
                        in_A[i, j] *= -1
                    in_b[i] *= -1


            # Add new variables to convert inequation to equation:
            #     x1 + x2 + x3 + ... + xn <= c
            # =>  x1 + x2 + x3 + ... + xn + x = c
            # Thus appending an identity matrix        
            for i in range(n):
                if sign[i] == "=":
                    continue

                tmp = np.zeros(n)
                for j in range(n):
                    if i == j:
                        tmp[j] = 1
                        break
                in_A = np.c_[in_A, tmp]
                # Append 0 to the Objective function to make it the right dimension
                in_c = np.append(in_c, 0)


        elif input_type == 2:
            # Read from file
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tGoal function minimisation or maximisation\nc1 c2 c3 ... cM\nA11 A12 ... A1M _ b1\nA21 A22 ... A2M _ b2\n................\nAN1 AN2 ... ANM _ bN\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<', '>' or '='\n")
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
            
            in_c = []
            # Read 2 first lines
            for i in range(3):
                if i == 0:
                    n, m = [int(x) for x in next(f).split()]    # Reads the dimensions
                if i == 1:
                    otype = next(f).split()
                    otype = otype[0]
                    if otype != "min" and otype != "max":
                        f.close()
                        raise Exception("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")
                if i == 2:
                    in_c = np.append(in_c, [float(x) for x in next(f).split()])     # Reads the Objective functiom
            
            # Converting the Objective function to minimise since the program is made with minimisation
            if otype == "max":
                print("Converting max to min.")
                in_c *= -1

            tmp_array = []
            for line in f:  # Read the next lines
                tmp_array.append([str(x) for x in line.split()])
            f.close()       # File not needed, all is in tmp_array
            
            # Formatting the input
            in_A = []
            sign = []
            in_b = []
            # print(tmp_array)
            for i in range(n):
                for j in range(m + 2):
                    if j < m:
                        in_A.append(float(tmp_array[i][j]))
                    elif j == m:
                        sign.append(tmp_array[i][j])
                    elif j == (m + 1):
                        in_b.append(float(tmp_array[i][j]))
                
                # No transformation required, since this program works with "<"
                # And "=" can be represented both as ">=" and "<="
                if sign[i] == "=":
                    continue

                # If the entered sign is ">" than we transform it to "<"
                if sign[i] == ">":
                    in_A_length = len(in_A)
                    for j in range(i*m, in_A_length, 1):
                        in_A[j] *= -1
                    in_b[i] *= -1

            # Converting the final list to numpy array
            in_A = np.array(in_A)
            in_A = in_A.reshape(n, m)

            # Add new variables to convert inequation to equation:
            #     x1 + x2 + x3 + ... + xn <= c
            # =>  x1 + x2 + x3 + ... + xn + x = c
            # Thus appending an identity matrix                    
            for i in range(n):
                if sign[i] == "=":
                    continue

                tmp = np.zeros(n)
                for j in range(n):
                    if i == j:
                        tmp[j] = 1
                        break
                in_A = np.c_[in_A, tmp]
                # Append 0 to the Objective function to make it the right dimension
                in_c = np.append(in_c, 0)


        return in_A, in_c, in_b        
        


def two_phase_simplex(c, A, b, unit_columns):
    # --- PHASE ONE ---
    # STEP1: Creating subgoal system: 
    # (min) w1 + w2 + ... + wN
    # Ew + Ax = b
    # w, x >= 0
    # System Ax = b has solution only if the subgoal system has solution equal to zero

    A1 = np.eye(len(A))
    A1 = np.hstack((A1, A))
    c1 = np.zeros(len(A1[0]))

    for i in range(len(A)):
        c1[i] = 1

    if not is_not_canonical(A, b, c):
        for i in range(len(A1)-1, -1, -1):
            if i in unit_columns:
                A1 = np.delete(A1, i, 1)
                c1 = np.delete(c1, i)
    else:
        unit_columns.clear()

    print("A1:\n", A1)
    print("c1: ", c1)
    print("b: ", b)

    P1, Q1, Fo1 = set_canonical_matrix(A1, b, c1)
    F1, x1 = revised_simplex(A1, b, c1, P1, Q1, Fo1)

    print("F1: ", F1)
    print("x1: ", x1)
    print_split()

    if(np.abs(F1) > precision):
        print("There is no solution.")
        return 0
    
    # STEP2: Removing pseudo variables
    # STEP1a: Removing all variables that are not in base (their indexes are not in P1)
    P1_pseudo_indexes = []
    for p in range(len(P1)):
        if P1[p] >= len(A1):
            break
        if p not in unit_columns: 
            P1_pseudo_indexes.append(p)

    # First n (A1.height()) columns are pseudo variables
    # Columns are removed from right to left so new indexes for matrix variable do not have to be calculated
    # ex: if we remove column 2 then 3 becomes 2, 3 -> 4, etc but 1 stays 1
    for i in range(len(A1)-1, -1, -1):
        if i not in P1_pseudo_indexes and p not in unit_columns:
        #if (P1_pseudo_indexes[P1_pseudo_indexes.index(i)] == P1_pseudo_indexes[-1]) and (unit_columns[unit_columns.index(p)] == len(unit_columns)):
            A1 = np.delete(A1, i, 1)

    print("Pseudo indexes:\n", P1_pseudo_indexes)
    print_split()

    # pseudo variable: x(i) == w(i)
    # STEP2a: If pseudo variable x(i) is in base and there are non-zero values in row where A(row, i) == 1
    # (only one row since x(i) is in base) then we we choose one non-zero value for pivot and "clear" its column
    # "clear": set all values below and above to 0 and pivot to 1

    # STEP2b: If pseudo variable x(i) is in base and there are no non-zero values in row where A(row, i) == 1
    # then we remove k-th row and i-th column from matrix
    for p in P1_pseudo_indexes:
        row = 0
        pivot = -1
        for j in range(len(A[0])):
            if np.abs(A[j, p] - 1) < precision:
                row = j
                break
        print("A1:\n", A1)
        for j in range(len(A)):
            if (p != j) and (np.abs(A1[row, j]) > precision):
                pivot = j
                break
    
        # ~=STEP2a
        if pivot == -1:
            A1 = np.delete(A1, i, 1)    # Deletes column  i
            A1 = np.delete(A1, row, 0)  # Deletes row     row
            b = np.delete(b, row)
            print("Clears the row and column")
            continue

        # ~=STEP2b
        value = A1[row, pivot]
        A[row] /= value

        for j in range(len(A)):
            if j == row:
                continue
            else:
                value = A1[j, pivot]
                A[j] -= value

        A1 = np.delete(A1, i, 1)

    A2 = A1
    b2 = b

    print("New system:")
    print("A2:\n", A2)
    print("b2: ", b2)
    print("c: ", c)
    print_split()


    # *PHASE TWO*
    # Solve new system:
    # (min) c*x
    # Where A2*x = b2 and x >= 0
    P2, Q2, Fo2 = set_canonical_matrix(A2, b2, c)
    F2, x2 = revised_simplex(A2, b2, c, P2, Q2, Fo2)

    print("Solution: ", np.round(x2, 3))
    print("Optimal value: \nminf = " + str(np.round(F2, 3)) + "\nmaxf = " + str(np.round(-F2, 3)))

    return 0

def dual_simplex(c, A, b, F):
    it = 0
    F = 0
    while 1:
        print("Iteration " + str(it) + ":\n")
        it += 1
        # Step 1: Check if b >= 0
        # If yes then STOP, optimal value has been found
        # If no  then the optimal value exists such that b(i) < 0
        # Proceed to Step 2
        print("Step 1: Is b >= 0?")
        b_neg_idx = is_non_negative(b)
        if b_neg_idx == -1:
            print("Opimal value has been found!")
            print("Optimal value: \nminf = " + str(np.round(F, 3)) + "\nmaxf = " + str(np.round(-F, 3)))
            return 0
        else:
            print("b(" + str(b_neg_idx) + ") is negative, proceeding to Step 2...")
            print_split()
            # Step 2: Check if A(b_neg_idx) >= 0
            # If yes then STOP, the solution doesn't exist
            # If no  then j exists such that the A(b_neg_idx, j) < 0
            print("Step 2: Is A(" + str(b_neg_idx) + ") >= 0?")
            A_neg_idx = is_non_negative_matrix_row(A, b_neg_idx)
            if A_neg_idx == -1:
                print("The soludtion doesn't exist")
                return 0
            else:
                print("A(" + str(b_neg_idx) + ", " + str(A_neg_idx) + ") is negative, proceeding to Step 3...")
                print_split()
                # Step 3: Finding a maximum c(j) / A(b_neg_idx, j) such that A(b_neg_idx, j) < 0
                print("Finding a maximum c(j) / A(" + str(b_neg_idx) + ", j) such that A(" + str(b_neg_idx) + ", j) < 0")
                pivot_index = find_pivot(c, A, b_neg_idx)
                print("Pivot: A(" + str(b_neg_idx) + ", " + str(pivot_index) + ")")
                print_split()

                c, A, b, F = update_system(c, A, b, F, b_neg_idx, pivot_index)
                print_system(A, b, c, F)
            


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
    # seed(1337)
    # n - number of rows of A
    # m - number of columns of A
    n = len(A)
    m = len(A[0])
    Fo = float(0)
    
    # j - row
    # i - column
    while is_not_canonical(A, b, c):
        for i in range(n):
            if (A[i, i] * b[i] < -precision) or (np.abs(A[i, i] < precision)):
                # If b[i] is negative then we have to pick different columns for the base
                # Finding all potential base columns:
                potential_base_columns = []
                for j in range(i+1, m, 1):
                    if A[i, j] * b[i] > 0:
                        potential_base_columns.append(j)

                # Picking random column and replacing it with current one in base:
                # new_column_index = randrange(12873321) % len(potential_base_columns)
                new_column = potential_base_columns[0]
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
        val = np.float64(x[P[i]]) / y[i]
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
    Cb = c[P]
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
    option = 0    
    while option != 1 and option != 2:
        print("Select one of the possible opions:\n\t(1) Two-Phase simplex method\n\t(2) Dual simplex method")
        option = int(input("Option: "))
        print_split()

    # Setting precision and notation
    np.set_printoptions(precision = 3)
    
    if option == 1:
        # Two-Phase simplex method
        A, c, b, unit_columns = input_vars(option)
        two_phase_simplex(c, A, b, unit_columns)   
    elif option == 2:
        # Dual simplex method
        A, c, b = input_vars(option)
        # Prints begining system
        F = 0
        print_system(A, b, c, F)
        dual_simplex(c, A, b, F)

    else:
        print("How did you get here???")
    


    return 0


if __name__ == '__main__':
   main()