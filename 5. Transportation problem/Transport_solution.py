import os.path
from os import path
import numpy as np

precision = 0.000001

# Prints a bar
def print_split():
    print("--------------------------------------------------\n")


def print_pseudo_vars(pseudo_rows, pseudo_columns):
    print("Pseudo rows: ", pseudo_rows)
    print("Pseudo columns: ", pseudo_columns)
    print("\n")

def print_system(C, a, b, pseudo_rows, pseudo_columns):
    print("System matrix:")
    n = len(C)
    m = len(C[0])
    print_split()

    for i in range(n):
        for j in range(m-1):
            if (pseudo_rows[i] != pseudo_rows[-1]) or (pseudo_columns[j] != pseudo_columns[-1]):
                print("*")
            else:
                print(C[i, j])
            print(" ")
        if (pseudo_rows[i] != pseudo_rows[-1]) or (pseudo_columns[m-1] != pseudo_columns[-1]):
            print("*")
        else:
            print(C[i, m-1])
        print("|")
        print(a[i])
    print_split()
    for j in b:
        print(j, " ")

    print("\n")



def input_vars():
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe file must be in the following format:\nN M\t\t\t\tWhere N - number of equations and M - number of variables\n\"min\" or \"max\"\t\t\tGoal function minimisation or maximisation\nC11 C12 C13 ... C1M a1\nC21 C22 C23 ... C2M a2\n................\nCN1 CN2 CN3 ... CNM aN\nb1 b2 b3 ... bM")
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
            in_C = []
            in_a = []
            in_b = []
            # print(tmp_array)
            for i in range(n):
                for j in range(m):
                    in_C.append(float(tmp_array[i][j]))
                in_a.append(float(tmp_array[i][-1]))
            for j in range(m):    
                in_b.append(float(tmp_array[-1][j]))
                

            # Converting the final list to numpy array
            in_C = np.array(in_C)
            in_C = in_C.reshape(n, m)
            in_a = np.array(in_a)
            in_b = np.array(in_b)

            return n, m, in_C, in_a, in_b


def add_pseudo_vars(C, a, b):
    n = len(C)
    m = len(C[0])

    sum_a = 0.0
    sum_b = 0.0
    for val in a:
        sum_a += val
    for val in b:
        sum_b += val

    pseudo_rows = []
    pseudo_columns = []
    difference = sum_a - sum_b
    if np.abs(difference) < 0.000001:
        return pseudo_rows, pseudo_columns
    
    pseudo_value = -np.Inf
    for i in range(n):
        for j in range(m):
            pseudo_value = np.max(pseudo_value, C[i, j])
    pseudo_value += 1000000

    if difference < 0:
        # Insert new row
        new_row = np.zeros(m, pseudo_value)
        C = np.vstack(C, new_row)
        a.append(new_row)
    else:
        # Insert new column
        C = np.hstack(C, np.full(i, pseudo_value))
        b.append(np.abs(difference))
        pseudo_columns.append(m)

    return pseudo_rows, pseudo_columns


def calculate_solution(C, base_mat, pseudo_rows, pseudo_columns):
    result = 0
    n = len(base_mat)
    m = len(base_mat[0])

    for i in range(n):
        if pseudo_rows.index(i) != pseudo_rows[-1]:
            continue
        for j in range(m):
            if pseudo_columns.index(j) != pseudo_columns[-1]:
                continue
            result += base_mat[0, i, j] * C[i, j]

    return result


def calculate_system_base_matrix(C, a, b):
    n = len(a)
    m = len(b)
    base_matrix = np.zeros((n, m, 2), dtype=float)

    # We can't use empty_rows or empty_columns because x(i, j) = a(i) or x(i, j) = b(j)
    empty_rows = set()
    empty_columns = set()
    for i in empty_rows == empty_rows[-1]:
        for j in empty_columns == empty_columns[-1]:
            min_ab = min(a[i], b[j])
            base_matrix[i, j] = (min_ab, 1)
            a[i] -= min_ab
            b[i] -= min_ab

            if np.abs(a[1]) < precision:
                empty_rows.add(i)
            elif np.abs(b[j]) < precision:
                empty_columns.add(j)
    
    return base_matrix


def main():
    print("Transportation problem")
    print_split()

    n, m, C, a, b = input_vars()
    pseudo_rows, pseudo_columns = add_pseudo_vars(C, a, b)
    print_pseudo_vars(pseudo_rows, pseudo_columns)
    print_system(C, a, b, pseudo_rows, pseudo_columns)
    # Minimal price method:
    base_matrix = calculate_system_base_matrix(C, a, b)
    print_base_matrix(base_matrix)




if __name__ == '__main__':
   main()