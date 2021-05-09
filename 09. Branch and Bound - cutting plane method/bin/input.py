import os.path
from os import path
import sys
import numpy as np
from .print_ import print_split

def input_vars():    
    sol_set = 'N'
    option = 2

    while option != 1 or option != 2:
        if option == 1:
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of rows and M - number of columns\n\"max\"\t\t\tObjective function maximisation\nc1 c2 c3 ... cM\na1 a2 a3 a4 ... aM _ b\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<=', '>=' or '='\n'x y' or 'N0'\t\tFor xi in set [x, y], or 'N0' for xi in set N0[0, +inf]")
            print_split()

            n = int(input("Input the number of constraints: "))
            m = int(input("Input the number of variables: "))

            # Reserving and initializing space for the Objective function
            in_c = np.empty(m)
            # Reserving and initializing space for the coeficients
            in_A = np.empty(m)
            # Reserving and initializing space for the solution values
            in_b = 0

            otype = input("Input \"min\" or \"max\" for the Objective function: ")
            if otype != "min" and otype != "max":
                raise Exception("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")

            # Input the Objective function
            tmp = input("Objective function: ").split()
            i = 0
            for c in tmp:
                in_c[i] = int(c)
                i += 1
            '''            
            # Converting the Objective function to minimise since the program is made with minimisation
            if otype == "max":
                print("Converting max to min.")
                in_c *= -1
            '''
            sign = ''
            # Input a line to a tmp variable
            tmp = input(str(i) + ": ").split()
            for j in range(m):
                in_A[j] = int(tmp[j])
            sign = tmp[m]
            in_b = int(tmp[m + 1])

            if sign == '>=':
                in_A *= -1
            if otype == 'min':
                in_c *= -1


            '''
                # No transformation required, since this program works with "<="
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
            # Thus appending a canonical matrix at the end
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
            '''
            print_split()

            break

        elif option == 2:
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of rows and M - number of columns\n\"max\"\t\t\tObjective function maximisation\nc1 c2 c3 ... cM\na1 a2 a3 a4 ... aM _ b\n  for x1, x2, x3, ... xM >= 0\t\tWhere '_' should be '<=', '>=' or '='\n'x y' or 'N0'\t\tFor xi in set [x, y], or 'N0' for xi in set N0[0, +inf]")
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
                    t = next(f).split()
                    n = int(t[0])    # Reads the dimensions
                    m = int(t[1])    # Reads the dimensions
                if i == 1:
                    otype = next(f).split()
                    otype = otype[0]
                    if otype != "min" and otype != "max":
                        f.close()
                        raise Exception("The Objective function type is wrong it should be either \"min\" or \"max\"!\n")
                if i == 2:
                    in_c = np.append(in_c, [int(x) for x in next(f).split()])     # Reads the Objective functiom
            
            
            # Converting the Objective function to minimise since the program is made with maximization
            # if otype == "min":
            #     print("Converting min to max.")
            #     in_c *= -1
            
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
            
            # Reading solution set
            tmp = tmp_array[-1]
            if len(tmp) == 2 and tmp[0].isdigit() and tmp[1].isdigit():
                sol_set = "cust"
                lb = int(tmp[0])
                ub = int(tmp[1])
                print(f"Solution set: [{lb}, {ub}]")

                if lb > ub or lb < 0:
                    f.close()       
                    raise Exception("Ivalid bounds!")
            elif len(tmp) == 1 and tmp[0].lower() == 'n':
                print("Solution set: [0, +inf]")
                sol_set = 'inf'
                lb = 0
                ub = 'inf'
            else:
                f.close() 
                raise Exception("Invalid solution set!")

            f.close()       
            '''    
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
            '''
            for i in range(n):
                if sign[i] == ">=":
                    in_A[i] *= -1
                    in_b[i] *= -1
                    sign[i] = "<="
                    
            # Converting the final list to numpy array
            in_A = np.array(in_A)
            in_A = in_A.reshape(n, m)
            '''
            # Add new variables to convert inequation to equation:
            #     x1 + x2 + x3 + ... + xn <= c
            # =>  x1 + x2 + x3 + ... + xn + x = c
            # Thus appending a canonical matrix at the end
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
            '''
            break
                    
        else:
            option = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()

    return n, m, otype, in_c, in_A, sign, in_b, sol_set, lb, ub
